from hash import Hash
import multiprocessing

import charsetGenerators
from hash import Hash
from logger import Logger
import observable
import observer
import task
import timeit
import time
import os

from twisted.internet import threads, reactor
from workRange import WorkRange

class Node(observable.IObservable):

    """Abstract node class"""

    def __init__(self):
        observable.IObservable.__init__(self)

    def runBenchmark(self,hashFunction,charset,length=3):
        pass

    def guessPasswords(self,passwords,hashFunction,primer,prefix,charset,length):
        pass

class RemoteNode(Node,observable.IObservableController):

    """Adaptor for a networked node"""

    def __init__(self,nodeId):
        Node.__init__(self)
        observable.IObservableController.__init__(self)
        self.nodeId = nodeId

    def runBenchmark(self,hashFunction,charset,length=3):
        self.notifyObservers('Cmd:runBenchmark("%s",%s,%d)' % (hashFunction,repr(charset),length), self.nodeId)

    def guessPasswords(self,passwords,hashFunction,primer,prefix,charset,length):
        message = 'Cmd:guessPasswords(%s,"%s",%s,%s,%s,%d)' % (repr(passwords),hashFunction,repr(primer),repr(prefix),repr(charset),length)
        self.notifyObservers(message,self.nodeId)

class LocalNode(Node):

    """Implementation for a local node"""

    def __init__(self,nodeId='default'):
        Node.__init__(self)
        self.nodeId = nodeId
        self.logger = Logger()
        self.results = multiprocessing.Queue()
        self.coreCount = multiprocessing.cpu_count()
        self.maxProcesses = self.coreCount * 2
        self.processes = []
        self.running = []
        self.working = False

    def runBenchmark(self,hashFunction='lanman',charset=None,length=3):

        self.log('Signal','Starting the benchmark (node=%s,hash=%s,length=%d)' % (self.nodeId,hashFunction,length),'runBenchmark')

        if charset == None:
            charset = charsetGenerators.PrintableASCIIGeneratorUpper().getCharset()

        max = len(charset) ** length

        arg = 'node.LocalNode().benchmark("%s",%s,%d)' % (hashFunction,repr(charset),length)
        t = timeit.Timer(arg,'import node')
        times = t.repeat(1,1)

        sum = 0

        for time in times:
            sum += time

        avg = sum / len(times)

        bench = int(max / avg)

        result = 'Bench:{"%s" : %d}' % (self.nodeId,bench)

        self.log('Signal','Benchmark completed with result: %d (node=%s)' % (bench,self.nodeId),'runBenchmark')

        self.notifyObservers(result)

    def benchmark(self,hashFunction,charset,length):

        password = ''

        primer = [[]]
        prefix = [charset]

        self.log('Signal','Beginning benchmark','benchmark')

        self.guessPasswords(password, hashFunction, primer, prefix, charset,length)

        while self.working:
            pass

        self.log('Signal','Benchmark finished','benchmark')

    def optimizeTasks(self,primer,prefix,charset):

        # if there are less chunks than there are cores to put to work,
        # divide the work into more chunks
        if len(prefix) < self.coreCount:
            [primer,prefix] = WorkRange(charset).divideMore(primer,prefix,self.coreCount)

        return [primer,prefix]

    def guessPasswords(self,passwords,hashFunction,primer,prefix,charset,length):

        #print "observers:" + str(len(self.observers))
        [primer,prefix] = self.optimizeTasks(primer,prefix,charset)

        hashFunctions = Hash().getPossibleHashFunctions()

        if hashFunction in hashFunctions:
            hashFunction = hashFunctions[hashFunction]
        else:
            raise ValueError('Hashfunction "%s" not available' % hashFunction)

        # it is possible to have more tasks than there are cores
        taskCount = len(prefix)

        work = range(taskCount)

        for i in range(taskCount):
            args = []
            args.append(passwords)
            args.append(hashFunction)
            args.append(primer[i])
            args.append(prefix[i])
            args.append(charset)
            args.append(length)
            args.append(self.results)

            args = tuple(args)
            work[i] = args

        self.processes = []

        self.log('Signal','Starting subprocesses enabling parallelism','guessPasswords')

        # initialize the processes
        for i in range(taskCount):
            p = apply(task.Task,work[i])
            self.processes.append(p)

#        if not bench:
            # initialize the manager
        self.initializeManager()

#        else:
#
#            maxProcesses = self.coreCount * 2
#            self.running = []
#
##            print "current processID: " + str(os.getpid())
#
#            #while there are still processes that need to be started / are running
#            while(len(self.processes) > 0 or len(self.running) > 0):
#
#                #while there are free process slots and there are still processes that
#                # need to be started, start an extra process
#                while len(self.running) < maxProcesses and len(self.processes) > 0:
#
#                    p = self.processes.pop()
#                    p.start()
#
##                    print str(p.pid) + " started"
#
#                    self.running.append(p)
#
#                # for each running process
#                for p in self.running:
#
#                    # if the process has finished
#                    if not p.is_alive():
#
##                        print str(p.pid) + " finished"
#
#                        # remove the process from the running list
#                        self.running.remove(p)

    def initializeManager(self):

        self.running = []
        self.working = True
#        threads.deferToThread(self.manageProcesses)
#        threads.deferToThread(self.fetchResults)

        self.manageProcesses()
        self.fetchResults()

    def manageProcesses(self):

        #while still working
        if self.working:

            #while there are free process slots and there are still processes that
            # need to be started, start an extra process
            while len(self.running) < self.maxProcesses and len(self.processes) > 0:

                p = self.processes.pop()
                p.start()

                self.running.append(p)

            # for each running process
            for p in self.running:

                # if the process has finished
                if not p.is_alive():

                    # remove the process from the running list
                    self.running.remove(p)

            # check if the work hasn't finished
            if len(self.processes) == 0 and len(self.running) == 0:
                self.working = False
            reactor.callLater(0.5,self.manageProcesses)

    def fetchResults(self):

        # while still working or while there are still results in the queue
        if self.working or not self.results.empty():
            while not self.results.empty():
                self.catchResult()
            reactor.callLater(0.5,self.fetchResults)
        else:
            self.log('Signal','Work completed','fetchResults')

            # no more results to get and the work has been completed
            # send this info upstream
            notification = 'Work:Done'
            self.notifyObservers(notification)

    def catchResult(self):
        # blocking get from Queue
        result = self.results.get()

        self.log('Signal','Result found: %s' % result,'catchResult')
        # send the result upstream
        notification = 'Results:' + repr(result)
        self.notifyObservers(notification)


    def stopWork(self):

        self.working = False

        for process in self.processes:
            process.shutdown()
            process.join()


        for process in self.running:
            process.shutdown()
            process.join()

        self.log('Signal','Stopped work processes','stopWork')

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'LocalNode')

if __name__ == '__main__':

    local = LocalNode()
    local.registerObserver(observer.printObserver())
    local.runBenchmark(length=3)
