import charsetGenerators
import ast
import multiprocessing
from hash import Hash
from logger import Logger
from observer import IObserver
from twisted.internet import reactor
from view import View
from workMaster import WorkMaster
from remoteNodeInterface import RemoteNodeInterface
import internetIP

class Controller(IObserver):
    
    def __init__(self):
        IObserver.__init__(self)
        self.logger = Logger()
        self.runningBench = False
        self.runningWork = False

        self.view = None
        self.port = 55555
        self.host = ''
        self.model = ''
        self.timeRunning = 0
        self.maxTime = 0
        self.benches = {}
        self.benchQueue = multiprocessing.Queue()
        self.resultQueue = multiprocessing.Queue()
        self.updates = multiprocessing.Queue()

    def main(self):

        self.view = View(self)
        self.view.optionView()

    def setupServer(self,port=55555):
        """Sets up the server"""

        self.model = WorkMaster(self.resultQueue)
        self.model.setupServer(port)
        self.model.addLocalNode()
        self.model.registerObserver(self)

    def setupClient(self,host='localhost',port=55555):
        """Sets up the client"""

        self.model = RemoteNodeInterface()
        self.model.setupClient(host,port)

    def setPasswords(self,passwords):
        
        passwords = passwords.strip()
        passwords = passwords.encode()
        passwords = passwords.split('\n')
        
        passes = []
        
        for p in passwords:
            p = p.split(':')
            
            if len(p) > 1:
                passes.append(p[2])
            else:
                passes.append(p[0])

        self.log('Signal','Passwords to check for are: %s' % repr(passes),'setPasswords')
        
        self.model.setPasswords(passes)
        
    def setLength(self,length):
        
        self.log('Signal','Password length to check up to is: %d' % length,'setLength')
        
        self.model.setLength(length)

    def setBenchLength(self,length):

        self.log('Signal', 'Bench password length: %d' % length,'setBenchLength')

        self.model.setBenchLength(length)

    def setCharset(self,charset):
        
        char = self.determineCharset(charset)
        
        self.log('Signal','Charset to search in is: %s' % charset,'setCharset')
        
        self.model.setCharset(char.getCharset())

    def determineCharset(self,charset):

        char = ''
        upper = self.model.hashFunction == 'lanman'


        if charset == 'numeric':
                char = charsetGenerators.NumericGenerator()
        elif charset == 'alpha':
            if upper:
                char = charsetGenerators.AlphaGeneratorUpper()
            else:
                char = charsetGenerators.AlphaGenerator()
        elif charset == 'alphanumeric':
            if upper:
                char = charsetGenerators.AlphaNumericGeneratorUpper()
            else:
                char = charsetGenerators.ASCIIGenerator()
        elif charset == 'printable':
            if upper:
                char = charsetGenerators.PrintableASCIIGeneratorUpper()
            else:
                char = charsetGenerators.PrintableASCIIGenerator()
        
        elif charset == 'ascii':
            if upper:
                char = charsetGenerators.ASCIIGeneratorUpper()
            else:
                char = charsetGenerators.ASCIIGenerator()

        self.log('Signal','Determined the charset to be: %s' % repr(char),'determineCharset')
        
        return char


    def setHashFunction(self,hash):

        hashFunctions = self.getPossibleHashes()

        if hash not in hashFunctions:
            raise ValueError('Hashfunction "%s" not available' % hash)
        else:
            self.model.setHashFunction(hash)

    def getPossibleHashes(self):
        return Hash().getPossibleHashes()

    def runBenchmark(self):
        """WorkMaster method"""

        self.view.reset()
        self.timeRunning = 0
        self.runningBench = True
        self.interval()

        self.log('Signal','Running benchmark','runBenchmark')
        self.model.runBenchmark()
        self.fetchBenches()

    def fetchBenches(self):

        if self.runningBench or not self.benchQueue.empty():
            if not self.benchQueue.empty():
                try:
                    self.benches = self.benchQueue.get()
                    self.benchCallback()
                    self.log('Signal','Benchmark results found','fetchBenches')
                except:
                    pass
            reactor.callLater(1.0,self.fetchBenches)

    def benchCallback(self):

        hashSpeed = self.model.sumBenches(self.benches)

        self.runningBench = False

        self.log('Signal','Received benchmark results: %s p/s' % hashSpeed,'benchCallback')

        self.updateBenchResults(hashSpeed)

    def updateBenchResults(self,hashSpeed):

        self.view.showHashSpeed(hashSpeed)
        self.updateMaxTimeAsDate(hashSpeed)

    def runWork(self):
        """WorkMaster method"""

        self.view.reset()
        self.timeRunning = 0
        self.runningWork = True

        self.benches = {}
        self.runBenchmark()

        self.awaitWork()

    def awaitWork(self):

        if len(self.benches) > 0:
            self.log('Signal','Running work','runWork')
            self.model.runWork(self.benches)
            self.fetchResults()
        else:
            reactor.callLater(1.0,self.awaitWork)        

    def fetchResults(self):

        if (self.runningWork and not self.runningBench) or not self.resultQueue.empty():
            if not self.resultQueue.empty():
                # blocking get from queue
                passes = self.resultQueue.get()
                self.workCallback(passes)
                self.log('Signal','Password results found','fetchResults')

            reactor.callLater(1.0,self.fetchResults)
        
    def workCallback(self,results):
    
        self.view.showResults(results)

        self.log('Signal','Added results','workCallback')

    def interval(self):

#        self.updateView()
        if self.runningBench or self.runningWork:
            self.increment()
            reactor.callLater(1,self.interval)
        else:
            self.increment()
            self.view.reactivateButtons()

    def makeHash(self,hashFunction,key):

        hashFunctions = Hash().getPossibleHashFunctions()

        if hashFunction in hashFunctions:
            hashFunction = hashFunctions[hashFunction]
        else:
            raise Exception('Hashfunction "%s" not available' % hashFunction)

        hash = hashFunction(key)

        self.view.showHash(hash)

    def updateMaxTimeAsDate(self,hashSpeed):

        maxTimeAsDate = self.getMaxTimeAsDate(hashSpeed)
        self.view.showMaxTimeAsDate(maxTimeAsDate)

    def increment(self):

        self.timeRunning += 1
        
        self.updateTime()

        if self.runningWork:
            self.incrementProgress()

    def updateTime(self):

        time = self.secondsToTime(self.timeRunning)
        self.view.updateTime(time)

    def incrementProgress(self):

        self.view.incrementProgress(self.timeRunning)

    def getHashSpeed(self,seconds):
        return self.model.getHashSpeed(seconds)

    def getMaxTime(self,hashSpeed):
        """Determine max seconds to run"""

        maxTime = self.model.getMaxTime(hashSpeed)

        self.log('Signal','Maximum run time is: %ds' % maxTime,'getMaxTime')
        return maxTime

    def getMaxTimeAsDate(self,hashSpeed):
        """Determine max seconds to run, return as a readable times"""

        maxTime = self.getMaxTime(hashSpeed)

        self.view.setSliderMax(maxTime)

        maxTimeAsDate = self.secondsToTime(maxTime)

        self.log('Signal','Maximum run time: %s' % maxTimeAsDate,'getMaxTimeAsDate')

        return maxTimeAsDate

    def secondsToTime(self,seconds):

        min = 60
        hour = min * 60
        day = hour * 24
        year = day * 365
        month = year / 12

        years = seconds / year
        seconds -= years * year
        months = seconds / month
        seconds -= months * month
        days = seconds / day
        seconds -= days * day
        hours = seconds / hour
        seconds -= hours * hour
        minutes = seconds / min
        seconds -= minutes * min

        times = [['year', years], ['month',months], ['day',days],['hour',hours],['minute',minutes],['second',seconds]]
        result = ''
        for pair in times:
            label = pair[0]
            time = pair[1]
            if time > 1:
                result += " %d %s%s" % (time,label,'s')
            elif time > 0 or label == 'second':
                result += " %d %s" % (time,label)

        return result

#        return "%d years:%d months:%d days: %d hours: %d minutes: %d seconds" \
#                % (years, months, days, hours, minutes, seconds)

    def getIP(self):
        
        ip = 'localhost'
        #ip = internetIP.getIP()

        self.log('Signal','IP is: %s' % ip,'getIP')

        return ip

    def setParameters(self,length=None,benchLength=None,charset=None,hashFunction=None,passwords=None):

        """Sets the necessary parameters"""
        # controller dependency to have hashFunction set first ( for: determineCharset(charset) )
        if hashFunction is not None:
            self.setHashFunction(hashFunction)
        if charset is not None:
            self.setCharset(charset)
        if length is not None:
            self.setLength(length)
        if benchLength is not None:
            self.setBenchLength(benchLength)
        if passwords is not None:
            self.setPasswords(passwords)

    def updateView(self):

        while not self.updates.empty():
            update = self.updates.get()
            apply(update[func],update[args])
        
    def stop(self):
        """Stops the client ( if the server is local, it will be stopped aswell )"""

        if self.model != '':
            self.model.stopWork()

        self.log('Signal','Shutting down program','stop')

        reactor.callLater(0.3,reactor.stop)

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'Controller')

    def addResult(self,result):
        """Processes a result and adds it to the result Queue"""

        lit = ast.literal_eval(result)
        self.resultQueue.put(lit)

        self.log('Signal','Added result %s...' % result[:10],'addResult')

    def addBench(self,bench):

        lit = ast.literal_eval(bench)
        self.benchQueue.put(lit)

        self.log('Signal','Added bench %s...' % bench[:10],'addBench')

    def update(self,data):
        """Callbacks from model"""

        self.log('Signal','Controller was updated: %s...' % data[:15],'update')

        data = data.split(':',1)

        if data[0] == 'Benches':

            self.addBench(data[1])
#            args = self.resultQueue.get()
#            self.updates.put({'target' : self.benchCallback, 'args' : args })

        elif data[0] == 'Results':

            self.addResult(data[1])
#            args = self.resultQueue.get()
#            self.updates.put({'target' : self.workCallback, 'args' : args })
            
        elif data[0] == 'Bench':
            if data[1] == 'Done':
                self.runningBench = False
                self.log('Signal','Finished benching','update')

        elif data[0] == 'Work':
            if data[1] == 'Done':
                self.runningWork = False
                self.log('Signal','Finished working','update')
        
if __name__ == '__main__':
    
    multiprocessing.freeze_support()
    c = Controller()
    c.main()
