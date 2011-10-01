import ast
import math
import threading

from hash import Hash
from charsetGenerators import PrintableASCIIGeneratorUpper
from idGenerator import IDGenerator
from logger import Logger
from network import ServerWrapper
from node import LocalNode
from node import RemoteNode
from observer import IObserver
from observer import IServerObserver
from observer import IObserverController
from observable import IObservable
from twisted.internet import threads
from workRange import WorkRange
from multiprocessing import Queue

class WorkMaster(IServerObserver,IObserver, IObserverController, IObservable):

    """Interface for the local WorkMaster, including possible networked workSlaves"""
    
    def __init__(self,resultQueue):
        IServerObserver.__init__(self)
        IObserverController.__init__(self)
        IObserver.__init__(self)
        IObservable.__init__(self)

        self.resultQueue = resultQueue
        self.nodeBenchQueue = Queue()

        self.idGenerator = IDGenerator()
        self.server = ServerWrapper(self.idGenerator)
        self.nodes = {} 
        self.nodeId = ''
        
        self.charset = PrintableASCIIGeneratorUpper().getCharset()
        self.passwords = ['~~']
        self.length = 5
        self.benchLength = 3
        self.primer = []
        self.prefix = []
        self.hashFunction = 'lanman'
        
        self.results = Queue()
        self.runningWork = False
        self.finished = 0
        self.logger = Logger()
        
    def setPasswords(self,passwords):
        self.passwords = passwords
        
    def setLength(self,length):
        self.length = length

    def setBenchLength(self,benchLength):
        self.benchLength = benchLength
        
    def setCharset(self,charset):
        self.charset = charset

    def setHashFunction(self,hash):

        if hash in Hash().getPossibleHashes():
            self.hashFunction = hash
        else:
            raise ValueError('Hashfunction "%s" not available' % hash)
        
    def addLocalNode(self):
        self.nodeId = self.idGenerator.getID()
        self.nodes[self.nodeId] = LocalNode(self.nodeId)
        self.nodes[self.nodeId].registerObserver(self)
        
    def addNetworkedNode(self,nodeId):
        self.nodes[nodeId] = RemoteNode(nodeId)
        self.nodes[nodeId].registerObserver(self)

        self.log('Signal','Slave Node added','addNetworkedNode')

    def removeNetworkedNode(self,nodeId):
        
        if nodeId in self.nodes:
            self.nodes[nodeId].removeObserver(self)
            del self.nodes[nodeId]
            self.log('Signal','Slave Node removed','removeNetworkedNode')
    
    def setupServer(self,port=55555):
        
        self.server.setupServer(port)
        self.server.registerObserver(self)

    def runBenchmark(self):

#        callbacks = []
#        callbacks.append(self.fetchBenchResults)

        self.log('Signal','deferring runBenches to thread','runBenchmark')

#        for fetcher in fetchers:
#            threads.deferToThread(fetcher)
#            self.log('Signal','Started fetcher: %s' % repr(fetcher),'runBenchmark')

#        self.runBenches(callbacks)
        self.runBenches()

    def runWork(self,benches):
        """Starts the work on the nodes"""

        self.finished = 0

#        callbacks = []
#        callbacks.append(self.fetchBenchResults)
#        callbacks.append(self.setToWork)
#        callbacks.append(self.fetchResults)

        self.log('Signal','deferring runBenches to thread','work')

#        for fetcher in fetchers:
#            threads.deferToThread(fetcher())
#            self.log('Signal','Started fetcher: %s' % repr(fetcher),'runWork')

#        self.runBenches(callbacks)
        self.setToWork(benches)
        
    def runBenches(self,):

        self.log('Signal','Running benchmarks on %d nodes' % len(self.nodes),'runBenches')

        #determine the guess speed of each node
        for node in self.nodes.itervalues():
            threading.Thread(target=node.runBenchmark,args=(self.hashFunction,self.charset,self.benchLength)).start()
        self.log('Signal','All nodes have been set to bench','runBenches')

        threads.deferToThread(self.fetchBenchResults)

#        d = threads.deferToThread(callbacks.pop(0))
#        if len(callbacks) > 1:
#            self.log('Signal','Adding callback to method catching result of runBenches','runBenches')
#            d.addCallback(callbacks.pop(0),callbacks)
#        else:
#            d.addCallback(callbacks.pop(0))


    def fetchBenchResults(self):

        finished = 0
        benches = {}
        while finished < len(self.nodes):
            benches.update(self.nodeBenchQueue.get())
            finished += 1

        self.log('Signal','Benches have completed: %s' % repr(benches),'fetchBenchResult')

        notification = 'Benches:' + repr(benches)
        self.notifyObservers(notification)
        notification = 'Bench:Done'
        self.notifyObservers(notification)

    def setToWork(self,benches):
        
        #determine the relative speeds of the nodes
        benches = self.normalize(benches)

        self.runningWork = True
        
        #divide the work according to these relative speeds
        [primer,prefix] = self.divideWork(benches)
        
        self.log('Signal','Starting work on %d nodes' % len(self.nodes),'runWork')
        
        #start the assigned work for each node
        for nodeId,node in self.nodes.iteritems():
            threading.Thread(target=node.guessPasswords,args=(self.passwords,self.hashFunction,primer[nodeId],prefix[nodeId],self.charset,self.length)).start()
        
#        threads.deferToThread(callbacks.pop(0))
#        d.addCallback(callbacks.pop(0))
    
    def fetchResults(self):
        
        while self.runningWork or not self.results.empty():
            if not self.results.empty():
                self.catchResult()

        self.log('Signal','Work completed','fetchResults')

        notification = 'Work:Done'
        self.notifyObservers(notification)

#        return passes

    def catchResult(self):

        # blocking get from queue
        result = self.results.get()

        self.log('Signal','Result found','catchResults')
        notification = 'Results:' + repr(result)
        self.notifyObservers(notification)
        
    def stopWork(self):

        for node in self.nodes.itervalues():
            node.stopWork()
        
    def normalize(self,benches):
        
        data = benches.values()
        
        min = data[0]
        max = data[0]
        
        for value in data:
            if value < min:
                min = value
            if value > max:
                max = value
        
        d = float(max) / min
        
        min = min - 1
        
        d = d/(max - min)      
        
        result = {}
        
        for nodeId,bench in benches.iteritems():
            result[nodeId] = int(math.ceil((bench - min) * d))
            
        return result  
        
    def divideWork(self,ratios):
        """
        Divides the work across all the nodes according to their
        relative speeds as to ensure a uniform workload.
        """
        
        taskCount = 0

        #Sums up the ratio amounts
        for nodeId,ratio in ratios.iteritems():
            taskCount += ratio

        #Divide the work into 'taskCount' chunks
        [primer,prefix] = WorkRange(self.charset).divideMore(self.primer,self.prefix,taskCount)
        
        prim = {}
        pref = {}
        
        for nodeId,ratio in ratios.iteritems():
            prim[nodeId] = []
            pref[nodeId] = []

            #Assigns each node 'ratio' amount chunks
            for i in range(ratio):
                prim[nodeId].append(primer.pop())
                pref[nodeId].append(prefix.pop())


        return [prim,pref]

    def getMaxTime(self,hashSpeed):
        """Determine max seconds to run"""

        possiblePasswords = 0
        length = self.length
        while length > 0:
            possiblePasswords += len(self.charset) ** length
            length -= 1
        seconds = possiblePasswords // hashSpeed

        self.log('Signal','Maximum seconds to run is %ds with a HashSpeed of %d and %d possibilities' % (seconds,hashSpeed,possiblePasswords),'getMaxTime')

        return seconds

    def getHashSpeed(self,seconds):

        possiblePasswords = len(self.charset) ** self.length
        hashSpeed = possiblePasswords // seconds

        self.log('Signal','HashSpeed is %d' % hashSpeed, 'getHashSpeed')

        return hashSpeed

    def sumBenches(self,benches):
        result = 0

        for node,bench in benches.iteritems():
            result += int(bench)

        return result
            
    def lineReceived(self,data,originator):
        """
        Handles messages received from a networked node
        IServerObserver overwritten method
        """

        self.log('Signal','Received Line: %s...' % data[0:10],'lineReceived')
        
        #print "*** network to node: " + repr(data)
        if data == 'NodeJoined':
            self.addNetworkedNode(originator)
        elif data == 'NodeLeft':
            self.removeNetworkedNode(originator)
        elif originator in self.nodes:

            self.log('Signal','%s sent result' % originator,'lineReceived')
            
            #self.update(data)

            data = data.split(':',1)

            if data[0] == 'Passwords':

                self.log('Signal','A networked node "%s" returned these passwords: %s' % (originator,repr(data[1])),'lineReceived')

                self.addResult(data[1])
            elif data[0] == 'Bench':
                self.log('Signal','A networked node "%s" returned these benches: %s' % (originator,repr(data[1])),'lineReceived')

                self.addResult(data[1])
        else:
            self.log('S Warning','Unknown source sent: %s' % repr(data),'lineReceived')
            
            
    def sendMessage(self,data,destination):
        """
        Handles messages destined for a networked node,
        received from a local NetworkedNode object
        IObserverController overwritten method
        """
        
        self.log('Signal','Sending command to networked node "%s"' % destination,'sendMessage')
        
        if destination in self.nodes:

            self.log('Signal','Sent command to %s cmd: %s' % (destination,data),'sendMessage')
            
            self.server.sendMessage(data,destination)
            
    def addBench(self,bench):

        lit = ast.literal_eval(bench)
        self.nodeBenchQueue.put(lit)

        self.log('Signal','Added bench %s...' % bench[:10],'addBench')

    def addResult(self,result):
        """Processes a result and adds it to the result Queue"""

        lit = ast.literal_eval(result)
        self.resultQueue.put(lit)

        self.log('Signal','Added result %s...' % result[:10],'addResult')
            
    def update(self,data):
        """
        Updates the controller
        IObserver overwritten method
        """
        data = data.split(':',1)

        self.log('Signal','Received an update: %s...' % repr(data)[0:10],'update')
        
        #print "*** local: " + repr(data)
        
        if data[0] == 'Results':

            self.log('Signal','The local node returned these passwords: %s' % repr(data[1]),'update')

            self.addResult(data[1])
        elif data[0] == 'Bench':
            self.log('Signal','The local node returned these benches: %s' % repr(data[1]),'update')
            
            self.addBench(data[1])

        elif data[0] == 'Work':
            if data[1] == 'Done':
                self.finished += 1
                if self.finished >= len(self.nodes):
                    self.runningWork = False
                    self.log('Signal','Finished working','update')

                    notification = 'Work:Done'
                    self.notifyObservers(notification)

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'WorkMaster')
            