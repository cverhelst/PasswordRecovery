# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Cameron"
__date__ ="$4-jul-2011 14:50:22$"

import sys

from observable import IObservableServer
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import ServerFactory
from twisted.protocols import basic
from logger import Logger

class ChatServer(basic.LineReceiver):

    def connectionMade(self):
        self.id = self.factory.getID()
        self.factory.clients[self.id] = self
        self.factory.log('Signal','Client Connected','connectionMade')
        self.factory.sendMessage("NodeId:%s" % (self.id),self.id)
        self.factory.notifyObservers("NodeJoined",self.id)
        
    def connectionLost(self, reason):

        if reason.type == ConnectionDone:
            del self.factory.clients[self.id]
            self.factory.log('Signal','Client Disconnected','connectionLost')
            self.factory.notifyObservers("NodeLeft",self.id)
            
        else:
            self.factory.log('Warning','Client Dropped','connectionLost')

    def lineReceived(self, line):

        self.factory.log('Signal','Observers: %s' % repr(self.factory.observers),'lineReceived')
        self.factory.notifyObservers(line, self.id)

class ChatServerFactory(ServerFactory,IObservableServer):

    def __init__(self,idGenerator):
        IObservableServer.__init__(self)
        self.clients = {}
        self.protocol = ChatServer
        self.idGenerator = idGenerator
        self.logger = Logger()
        self.log('Signal','Server Started','__init__')

    def sendMessage(self,message,destination):

        if destination in self.clients:
            self.clients[destination].sendLine(message)
                
    def getID(self):
        return self.idGenerator.getID()

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'TwistedServer')

def main():
    print "Attempting to setup Server"

    chatServerFactory = ChatServerFactory()

    args = sys.argv
    for arg in args:
        print arg
    port = 8000
    try:
        if args[1] is not None:
            port = int(args[1])
    except Exception:
        pass

    print 'arguments: ',port

    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(chatServerFactory)

    reactor.run()
    
if __name__ == "__main__":
    main()






