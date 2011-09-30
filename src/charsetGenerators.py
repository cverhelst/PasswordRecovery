"""This module contains generators for charsets that all exclude the lower case letters"""

class ExtendedASCIIGenerator():
    def __init__(self):
        self.data = set( [chr(char) for char in range(0,256)] )
    def excludeLower(self):
        self.data -= set( [chr(char) for char in range(97,123)] )
    def __iter__(self):
        return self.getCharset().__iter__()
    def getCharset(self):
        return sorted(list(self.data))
    
class ExtendedASCIIGeneratorUpper(ExtendedASCIIGenerator):
    def __init__(self):
        ExtendedASCIIGenerator.__init__(self)
        self.excludeLower()
        
        
        
class ASCIIGenerator(ExtendedASCIIGenerator):
    """Iterator for looping over a sequence backwards."""
    def __init__(self):
        ExtendedASCIIGenerator.__init__(self)
        self.data = set( [chr(char) for char in range(0,128)] )
        
class ASCIIGeneratorUpper(ASCIIGenerator):
    def __init__(self):
        ASCIIGenerator.__init__(self)
        self.excludeLower()


        
class PrintableASCIIGenerator(ExtendedASCIIGenerator):
    """Iterator for looping over a sequence backwards."""
    def __init__(self):
        ExtendedASCIIGenerator.__init__(self)
        self.data = set( [chr(char) for char in range(32,127)] )
        
class PrintableASCIIGeneratorUpper(PrintableASCIIGenerator):
    def __init__(self):
        PrintableASCIIGenerator.__init__(self)
        self.excludeLower()
        
        
        
class AlphaNumericGenerator(ExtendedASCIIGenerator):
    """Iterator for looping over a sequence backwards."""
    def __init__(self):
        ExtendedASCIIGenerator.__init__(self)
        self.data = set( [chr(char) for char in range(48,58)] )
        self.data |= set( [chr(char) for char in range(65,91)] )
        self.data |= set( [chr(char) for char in range(97,123)] )
        
class AlphaNumericGeneratorUpper(AlphaNumericGenerator):
    """Iterator for looping over a sequence backwards."""
    def __init__(self):
        AlphaNumericGenerator.__init__(self)
        self.excludeLower()
        
        
        
class AlphaGenerator(ExtendedASCIIGenerator):
    """Iterator for looping over a sequence backwards."""
    def __init__(self):
        ExtendedASCIIGenerator.__init__(self)
        self.data = set( [chr(char) for char in range(65,91)] )
        self.data |= set( [chr(char) for char in range(97,123)] )
        
class AlphaGeneratorUpper(AlphaGenerator):
    """Iterator for looping over a sequence backwards."""
    def __init__(self):
        AlphaGenerator.__init__(self)
        self.excludeLower()
        
        
        
class NumericGenerator(ExtendedASCIIGenerator):
    """Iterator for looping over a sequence backwards."""
    def __init__(self):
        ExtendedASCIIGenerator.__init__(self)
        self.data = set( [chr(char) for char in range(48,58)] )
        
if __name__ == '__main__':
    
    g = AlphaNumericGeneratorUpper()
    print len(g.getCharset())
    
    #print "** extended ASCII"
    #g = ExtendedASCIIGenerator()
    #for char in g:
    #    print str(ord(char)) + " " + char
    #    
    #print "** extended ASCII excluding lower"
    #g = ExtendedASCIIGeneratorUpper()
    #for char in g:
    #    print str(ord(char)) + " " + char
    #    
    #print "** ASCII"
    #g = ASCIIGenerator()
    #for char in g:
    #    print str(ord(char)) + " " + char
    #    
    #print "** printable ASCII"
    #g = PrintableASCIIGenerator()
    #for char in g:
    #    print str(ord(char)) + " " + char
    #    
    #print "** alphanumeric"
    #g = AlphaNumericGenerator()
    #for char in g:
    #    print str(ord(char)) + " " + char
    #    
    #print "** alpha"
    #g = AlphaGenerator()
    #for char in g:
    #    print str(ord(char)) + " " + char
    #    
    #print "** numeric"
    #g = NumericGenerator()
    #for char in g:
    #    print str(ord(char)) + " " + char
    