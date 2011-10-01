class Task(object):
    
    def __init__(self,passwords,hashFunction,primer,prefix,charset,length,results,exit):
        self.passwords = passwords
        self.hashFunction = hashFunction
        self.primer = primer
        self.prefix = prefix
        self.charset = charset
        self.length = length
        self.keyCharsets = [prefix.__iter__()]    
        self.key = ['']
        self.results = results
        self.exit = exit
        self.recoverPassword()

    def run(self):
        self.recoverPassword()
    
    def generateKeys(self):
        
        done = False               

        for key in self.primer:
            self.key[-1] = key
            yield ''.join(self.key)
            
        while (not done):
            
            incremented = False
            i = len(self.key) - 1
        
            while(not incremented):
                
                #increment
                try:
                    self.key[i] = self.keyCharsets[i].next()
                    incremented = True
                except StopIteration:
                    pass
                        
                #if end or last was reached reset every char and move one to the left /
                # add a char
                if not incremented:
                                   
                    it = range( i, len(self.key) )
                
                    # reset every char
                    for k in it:

                        if k != 0:
                            self.keyCharsets[k] = self.charset.__iter__()
                        else:
                            self.keyCharsets[k] = self.prefix.__iter__()
                        self.key[k] = self.keyCharsets[k].next()
                    
                    #if the beginning hasnt been reached, move one to the left
                    if i > 0:
                        i = i - 1
                    
                    # else if the beginning has been reached and
                    # the key hasn't reached max length, add a char
                    elif len(''.join(self.key)) < self.length:
                        self.keyCharsets.append(self.charset.__iter__())
                        self.key.append(self.keyCharsets[-1].next())
                        incremented = True

                    # key has reached max length and last / end chars
                    else:
                        done = True
                        break
            
            if not done:              
                yield ''.join(self.key)
        
    def hash(self, string):
        return self.hashFunction(string)
    
    def recoverPassword(self):
#        cracks = {}
        hash = ''
        
        for i in range(len(self.passwords)):
            self.passwords[i] = self.passwords[i].upper()
            
        for key in self.generateKeys():
            if self.exit.is_set():
                break
            hash = self.hash(key)
            for i in range(len(self.passwords)):
                if hash.upper() == self.passwords[i]:
                    result = {key: self.passwords[i]}
                    self.results.put(result)
    
class ParallelTask(Task):
    
    def __init__(self,passwords,hashFunction,primer,prefix,charset,length,resultQueue):
        Task.__init__(self, passwords, hashFunction, primer, prefix, charset, length)
        self.resultQueue = resultQueue
        self.recoverPassword()
        
    def recoverPassword(self):
        self.resultQueue.put( Task.recoverPassword(self) )

class Task2(object):

    def __init__(self,passwords,hashFunction,primer,prefix,charset,length):
        self.passwords = passwords
        self.hashFunction = hashFunction
        self.primer = primer
        self.prefix = prefix
        self.charset = charset
        self.length = length
        self.keyCharsets = [prefix.__iter__()]
        self.key = ['']
        self.recoverPassword()

    def keys(self):

        done = False

        for key in self.primer:
            self.key[-1] = key
            yield ''.join(self.key)

        while (not done):

            incremented = False
            i = len(self.key) - 1

            while(not incremented):

                #increment
                try:
                    self.key[i] = self.keyCharsets[i].next()
                    incremented = True
                except StopIteration:
                    pass

                #if end or last was reached reset every char and move one to the left /
                # add a char
                if not incremented:

                    it = range( i, len(self.key) )

                    # reset every char
                    for k in it:

                        if k != 0:
                            self.keyCharsets[k] = self.charset.__iter__()
                        else:
                            self.keyCharsets[k] = self.prefix.__iter__()
                        self.key[k] = self.keyCharsets[k].next()

                    #if the beginning hasnt been reached, move one to the left
                    if i > 0:
                        i = i - 1

                    # else if the beginning has been reached and
                    # the key hasn't reached max length, add a char
                    elif len(''.join(self.key)) < self.length:
                        self.keyCharsets.append(self.charset.__iter__())
                        self.key.append(self.keyCharsets[-1].next())
                        incremented = True

                    # key has reached max length and last / end chars
                    else:
                        done = True
                        break

            if not done:
                yield ''.join(self.key)

    def hash(self, string):
        return self.hashFunction(string)

    def recoverPassword(self):
        cracks = {}
        hash = ''

        for i in range(len(self.passwords)):
            self.passwords[i] = self.passwords[i].upper()

        for key in self.keys():

            hash = self.hash(key)
            for i in range(len(self.passwords)):
                if hash.upper() == self.passwords[i]:
                    cracks[key] = self.passwords[i]
                    if len(cracks) == len(self.passwords):
                        break

        return cracks
        
if __name__ == '__main__':
     from hash import Hash
     from charsetGenerators import NumericGenerator
     
     task = Task([''],Hash().lanman,['a'],['aa','ab'],NumericGenerator(),5)
     
     for key in task.generateKeys():
        print key