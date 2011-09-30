# To change this template, choose Tools | Templates
# and open the template in the editor.


__author__="Cameron"
__date__ ="$5-jul-2011 18:54:01$"

class IObserver(object):

    def update(self,data):
        """Updates data"""

class IServerObserver(object):

    def lineReceived(self,data,originator):
        """Handles line"""
        
class IObserverController(object):
    
    def sendMessage(self,data,originator):
        """Handles Message"""
        
class printObserver(IObserver):
        
    def __init__(self):
        IObserver.__init__(self)

    def update(self,data):
        print data

class ILogObserver(IObserver):

    def __init__(self):
        IObserver.__init__(self)

    def log(self,data,originator):
        print "%s : %s" % (originator.ljust(10),data)


if __name__ == "__main__":
    print "Hello World"
