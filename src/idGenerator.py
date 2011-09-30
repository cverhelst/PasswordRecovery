# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Cameron"
__date__ ="$15-jul-2011 17:07:05$"

class IDGenerator(object):

    def __init__(self):
        self.bot = 'a'
        self.max = 122
        self.uniqueKey = '#' + 'a'

    def getID(self):
        result = self.uniqueKey
        char = self.uniqueKey[-1]
        char = ord(char)
        char += 1
        if char > self.max:
            self.uniqueKey = ''.join((self.uniqueKey,self.bot))
        else:
            char = chr(char)
            self.uniqueKey = ''.join((self.uniqueKey[0:-1],char))
        return result


if __name__ == "__main__":
    idG = IDGenerator()

    for i in range(200):
        print idG.getID()
