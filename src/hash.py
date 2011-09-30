
from logger import Logger
from multiprocessing import Lock
import hashlib


class Hash(object):

	def __init__(self):

		self.logger = Logger()
		self.hashes = ['lanman','sha1','sha256','sha512','md5']

		try:
			import lanman
		except Exception:
			del hashes['lanman']
			self.log('Warning','No lanman hash available','__init__')

	def lanman(self,key):
		#return lmHash.LMHash(key) #selfPython
		#import lanman2
		#return lanman2.lmhash(key) #otherPython
		#return lmHash.LMHash2(key)  #selfC
		import lanman
		return lanman.lmhash(key) #otherC

	def sha1(self,key):
		return hashlib.sha1(key).hexdigest()

	def sha256(self,key):
		return hashlib.sha256(key).hexdigest()

	def sha512(self,key):
		return hashlib.sha512(key).hexdigest()

	def md5(self,key):
		return hashlib.md5(key).hexdigest()

	def getPossibleHashes(self):
		return self.hashes

	def getPossibleHashFunctions(self):

		hashFunctions = {}

		for hash in self.hashes:
			hashFunctions[hash] = getattr(self,hash)

		return hashFunctions

	def log(self,level,data,method=''):
		self.logger.log(level,data,method,'Hash')

			
# class Hash(object):

    # __instanceLock = Lock()
    # __instance = None

    # class __impl:

        # def __init__(self):

            # self.logger = Logger()
            # self.hashes = ['lanman','sha1','sha256','sha512','md5']

            # try:
                # import lanman
            # except Exception:
                # del hashes['lanman']
                # self.log('Warning','No lanman hash available','__init__')

        # def lanman(self,key):
            # #return lmHash.LMHash(key) #selfPython
            # #import lanman2
            # #return lanman2.lmhash(key) #otherPython
            # #return lmHash.LMHash2(key)  #selfC
            # import lanman
            # return lanman.lmhash(key) #otherC

        # def sha1(self,key):
            # return hashlib.sha1(key).hexdigest()

        # def sha256(self,key):
            # return hashlib.sha256(key).hexdigest()

        # def sha512(self,key):
            # return hashlib.sha512(key).hexdigest()

        # def md5(self,key):
            # return hashlib.md5(key).hexdigest()

        # def getPossibleHashes(self):
            # return self.hashes

        # def getPossibleHashFunctions(self):

            # hashFunctions = {}

            # for hash in self.hashes:
                # hashFunctions[hash] = getattr(self,hash)

            # return hashFunctions

        # def log(self,level,data,method=''):
            # self.logger.log(level,data,method,'Hash')

    # def __init__(self):

        # """ Create singleton instance """

        # # Check whether we already have an instance
        # if Hash.__instance is None:
            # #acquire lock for thread/process safety
            # Hash.__instanceLock.acquire()
            # #and check again
            # if Hash.__instance is None:
                # # Create and remember instance
                # Hash.__instance = Hash.__impl()
            # Hash.__instanceLock.release()

        # # Store instance reference as the only member in the handle
        # self.__instance = Hash.__instance

    # def __getattr__(self, attr):
        # """ Delegate access to implementation """
        # return getattr(self.__instance, attr)

    # def __setattr__(self, attr, value):
        # """ Delegate access to implementation """
        # return setattr(self.__instance, attr, value)


if __name__ == '__main__':

    h = Hash()

    hashes = h.getPossibleHashFunctions()
    print repr(hashes)

    for hash,func in hashes.iteritems():
        print hash,
        print repr(func('e'))
