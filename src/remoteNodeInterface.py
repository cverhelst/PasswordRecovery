from logger import Logger
from network import ClientWrapper
from node import LocalNode
from observer import IObserver

class RemoteNodeInterface(IObserver):
    """Interface from a local workSlave to the networked workMaster"""
    
    def __init__(self):
        IObserver.__init__(self)
        self.client = ClientWrapper()
        self.node = LocalNode()
        self.node.registerObserver(self)
        self.logger = Logger()
        
    def setupClient(self,host='localhost',port=55555):
        
        self.client.setupClient(host,port)
        self.client.registerObserver(self)
        
    def update(self,data):
        """
        Receive a message from the network
        or send results back to the host
        """
        
        copy = data.split(':',1)
        
        if copy[0] == 'Cmd': 
            cmd = "self.node." + copy[1]
            
            self.log('Signal','Running command %s' % cmd,'update')
            
            exec cmd
        elif copy[0] == 'NodeId':

            self.log('Signal','Setting nodeId to %s' % repr(copy[1]),'update')

            self.node.nodeId = copy[1]
        elif copy[0] == 'Results':
            
            self.log('Signal','Sending back results %s' % repr(copy[1]),'update')
            
            self.client.sendMessage(data)
            
        elif copy[0] == 'Bench':

            self.log('Signal','Sending back benches %s' % repr(copy[1]),'update')
            
            self.client.sendMessage(data)
        elif copy[0] == 'Work':
            if copy[1] == 'Done':
                self.log('Signal','Sending back signal of work done','update')

                self.client.sendMessage(data)

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'WorkSlave')
            
