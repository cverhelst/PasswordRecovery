# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "Cameron"
__date__ = "$4-jul-2011 18:13:37$"

from twisted.protocols import basic
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.internet.error import ConnectionDone
from observable import IObservable
from logger import Logger
import sys
import threading

class ChatClient(basic.LineReceiver):
    
    def connectionMade(self):
        self.factory.clientReady(self)
        self.factory.log('Signal','Connection Made')

    def connectionLost(self,reason):
        if reason.type != ConnectionDone:
            self.factory.log('Warning','Connection Lost, reason : %s' % repr(reason))
            self.factory.notifyObservers('*** Connection Lost: ' + repr(reason))
        else:
            self.factory.log('Signal','Connection Closed')
         
    def lineReceived(self, line):
        self.factory.notifyObservers(line)

    def remoteTerminate(self):
        self.transport.loseConnection()

class ChatClientFactory(ClientFactory,IObservable):

    def __init__(self):
        IObservable.__init__(self)
        self.logger = Logger()
    
    def startedConnecting(self, connector):
        self.log('Signal','Started to connect')

    def buildProtocol(self, addr):
        
        #self.resetDelay()
        self.messageQueue = []
        self.clientInstance = None

        client = ChatClient()
        client.factory = self
        return client

    def clientReady(self,instance):
        self.clientInstance = instance
        for msg in self.messageQueue:
            sendMessage(msg)

    def sendMessage(self,msg):

        if self.clientInstance is not None:
            self.clientInstance.sendLine(msg)
        else:
            self.messageQueue.append(msg)

    def remoteTerminate(self):
        self.clientInstance.remoteTerminate()

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'TwistedClient')

def getParameter(line, parameter, default=''):

    value = default
    try:
        line = line.strip('/')
        line = line.split('=')
        wordFound = False
        for word in line:

            if wordFound == True:
                value = word
                break

            if word == parameter:
                wordFound = True
    except Exception:
        pass
    return value


class InputEventHandler(threading.Thread):

    def __init__(self,factory):
        threading.Thread.__init__(self)
        self.chatClientFactory = factory
        self.chatClientFactory.input = self
        self.running = True

    def run(self):

        while self.running:
            input = sys.stdin.readline().strip()
            try:
                if input == self.chatClientFactory.end:
                    self.chatClientFactory.remoteTerminate()
                    self.running = False
                else:
                    self.chatClientFactory.sendMessage(input)
            except Exception:
                print 'Connection Failed'
                break

        print 'closing client..'

    def stop(self):
        self.running = False



def main():

    host = 'localhost'
    port = 8000

    args = sys.argv

    try:
        if args[1] is not None:
            host = args[1]
        if args[2] is not None:
            port = int(args[2])
    except Exception:
        pass

    print 'arguments: (',host, ',', port,')'

    factory = ChatClientFactory()
    reactor.connectTCP(host, port, factory)

    inputHandler = InputEventHandler(factory)
    inputHandler.start()

    reactor.run()

if __name__ == "__main__":
    main()
