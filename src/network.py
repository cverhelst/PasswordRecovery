from TwistedClient import ChatClientFactory
from TwistedServer import ChatServerFactory
from logger import Logger
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, TCP4ServerEndpoint
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="cameron"
__date__ ="$Sep 6, 2011 3:30:55 PM$"

class ServerWrapper(object):

    def __init__(self,idGenerator):
        self.logger = Logger()
        self.server = ''
        self.idGenerator = idGenerator

    def setupServer(self,port=55555):

        self.server = ChatServerFactory(self.idGenerator)

        self.log('Signal','Setting up the server on port %d' % port,'setupServer')

        endpoint = TCP4ServerEndpoint(reactor, port)
        d = endpoint.listen(self.server)
        d.addErrback(self.errorHandler)

        self.checkServer()

    def errorHandler(self,data):

        self.server = None
        self.log('Error','Server: %s -> %s' % (repr(data),data.getErrorMessage()),'errorHandler')

    def checkServer(self):

        if self.server == None:
            raise Exception('Server not set')

    def sendMessage(self,data,originator):

        self.log('Signal','Message Sent over network: %s...' % data[0:10],'sendMessage')

        self.server.sendMessage(data,originator)

    def registerObserver(self,observer):
        self.server.registerObserver(observer)

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'ServerWrapper')

class ClientWrapper(object):

    def __init__(self):
        self.logger = Logger()
        self.client = ''

    def setupClient(self,host='localhost',port=55555):

        self.client = ChatClientFactory()

        endpoint = TCP4ClientEndpoint(reactor, host, port)
        d = endpoint.connect(self.client)
        d.addErrback(self.errorHandler)

        self.checkClient()

    def errorHandler(self,data):
        self.client = None
        self.log('Error','%s -> %s' % (repr(data),data.getErrorMessage()),'errorHandler')

    def checkClient(self):

        if self.client == None:
            raise Exception('Client not set')

    def sendMessage(self,data):

        self.log('Signal','Message Sent over network: %s...' % data[0:10],'sendMessage')

        self.client.sendMessage(data)

    def registerObserver(self,observer):
        self.client.registerObserver(observer)

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'ClientWrapper')
        
if __name__ == "__main__":
    print "Hello World"
