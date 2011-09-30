# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Cameron"
__date__ ="$5-jul-2011 18:50:29$"

class IObservable(object):

    """Interface for the observer pattern"""
    def __init__(self):
        self.observers = []

    def registerObserver(self,observer):
        """Adds an observer"""
        self.observers.append(observer)

    def removeObserver(self,observer):
        """Removes an observer"""
        self.observers.remove(observer)

    def notifyObservers(self,data):
        """Notifies all observers"""
        for observer in self.observers:
            observer.update(data)

class IObservableServer(IObservable):
    
    def __init__(self):
        IObservable.__init__(self)

    def notifyObservers(self,data,originator):
        """Notifies Observer"""
        for observer in self.observers:
            observer.lineReceived(data,originator)
        
class IObservableController(IObservable):
    
    def __init__(self):
        IObservable.__init__(self)
        
    def notifyObservers(self,data,originator):
        
        for observer in self.observers:
            observer.sendMessage(data,originator)

class ILoggable(IObservable):

    def __init__(self):
        IObservable.__init__(self)
        
    def notifyObservers(self,data,originator):
        print "%s : %s" % (originator,data)


if __name__ == "__main__":
    print "Hello World"
