from datetime import datetime
from multiprocessing import Lock

class Logger(object):

    """TODO: Make singleton (ish)
             Make Enums for log types

             Thread-safe non-blocking Logger
             (TODO when used as a singleton)

    """

    
    __instanceLock = Lock()
    __instance = None

    class __impl:

        def __init__(self):
            self.lock = Lock()

        def log(self,level,data, method='',name=''):

            name = name.ljust(15)

            if method != '':
                method = method + '()'
            method = method.ljust(20)

            level = level.ljust(7)
            now = str(datetime.now()).split('.')[0]

            if method is not '':
                hasMethod = '-'
            else:
                hasMethod = ' '

            self.lock.acquire()
            print "[%s] %s %s %s ~*~ %s : %s" % (now,name,hasMethod,method,level,data)
            self.lock.release()

    def __init__(self):

        """ Create singleton instance """

        # Check whether we already have an instance
        if Logger.__instance is None:
            #acquire lock for thread/process safety
            Logger.__instanceLock.acquire()
            #and check again
            if Logger.__instance is None:
                # Create and remember instance
                Logger.__instance = Logger.__impl()
            Logger.__instanceLock.release()

        # Store instance reference as the only member in the handle
        self.__instance = Logger.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)


if __name__ == "__main__":
    print "Hello World"
