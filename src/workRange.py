from math import floor

class WorkRange(object):
    
    def __init__(self,charset):
        self.charset = charset
        
    def divideNormal(self,sequence,count,n=-1):
        
        #check if the sequence has more than 1 item to be able to make variations
        if len(self.charset) < 2:
            raise ValueError('The charset needs to be at least 2 items long')
            
        #check if the sequence is large enough to be divided in count items
        if count > len(sequence):
            raise ValueError("The count can't be larger than the length of the sequence")
        
        #working sequence
        copy = sequence
        
        #determine the chunksize / remainder
        r = int(floor( len(copy) / count ))
        remainder = len(copy) % count
        index = 0
        expanded = []
        
        #divide the sequence
        while(index + r < len(copy)):
            stop = index + r
            if remainder > 0:
                stop += 1
                remainder -= 1
            expanded.append(copy[index:stop])
            index = stop
            
        #add last variable size piece to the result
        if index + r >= len(copy):   
            expanded.append(copy[index:])
            
        #if provided, return on the n'th piece
        if n >= 0 and n < len(expanded):
            return expanded[n]
        else:
            return expanded
        
    def divide(self,count,n=-1):
        
        return self.divideMore(self.charset,count,n)
       
    def divideMore(self,primer,sequence,count,n=-1):
        """
        Divides the given sequence and primer into 'count' chunks and returns the result or just the n'th
        chunk if it was provided
        """
        
        #check if the charset has more than 1 item to be able to make variations
        if len(self.charset) < 2:
            raise ValueError('The charset needs to be at least 2 items long')
        
        tS = []
        tP = []

        #join the primer
        for p in primer:
            tP.extend(p)
            
        #join the sequence
        for c in sequence:
            tS.extend(c)
            
        primer = tP
        sequence = tS

        #holds the additional primer items
        addPrimer = []

        
        #if the sequence is too small to divide in count pieces: extend the sequence
        while(len(sequence) < count):
            addPrimer.extend(sequence)
            
            divSequence = []
            
            if len(sequence) > 0:
                for i in range(len(sequence)):
                    for k in range(len(self.charset)):
                        divSequence.append(''.join([sequence[i],self.charset[k]]))
            else:
                for k in range(len(self.charset)):
                    divSequence.append(self.charset[k])
            sequence = divSequence

        #add the additional primer items to the primer
        primer.extend(addPrimer)

        #PRIMER
        #determine the chunksize / remainder
        r = int(floor( len(primer) / count ))
        remainder = len(primer) % count
        index = 0
        divPrimer = []
        
        #divide the primer
        while(index + r < len(primer)):
            stop = index + r
            if remainder > 0:
                stop += 1
                remainder -= 1
            divPrimer.append(primer[index:stop])
            index = stop

        #add last variable size piece to the result
        if index + r >= len(primer):   
            divPrimer.append(primer[index:])

        #SEQUENCE
        #determine the chunksize / remainder
        r = int(floor( len(sequence) / count ))
        remainder = len(sequence) % count
        index = 0
        divSequence = []

        #divide the sequence
        while(index + r < len(sequence)):
            stop = index + r
            if remainder > 0:
                stop += 1
                remainder -= 1
            divSequence.append(sequence[index:stop])
            index = stop

        #add last variable-size piece to the result
        if index + r >= len(sequence):
            divSequence.append(sequence[index:])
            
        while len(divPrimer) < len(divSequence):
            divPrimer.append([])

        

        #if provided, return on the n'th piece
        if n >= 0 and n < len(divSequence):
            return [divPrimer[n],divSequence[n]]
        else:
            return [divPrimer,divSequence]
        
        
    
if __name__ == '__main__':
    
    import timeit
    
    from charsetGenerators import NumericGenerator
    
    w = WorkRange(NumericGenerator().getCharset())
    
    x = w.divideMore([],[],11)
    x = w.divideMore(x[0],x[1],15)
    
    #x = w.divideMore(map(str,range(10)),map(str,range(10,12)),10)
    
    
    #t = timeit.Timer('workRange.WorkRange(charsetGenerators.NumericGenerator().getCharset()).divideMore([],charsetGenerators.NumericGenerator().getCharset(),100001)','import workRange,charsetGenerators')
    #
    #times = t.repeat(1,1)
    #
    #sum = 0
    #
    #for i in range(len(times)):
    #    print "time " + str(i) + ": " + str(times[i]) + "s"
    #    sum += times[i]
    #
    #print "avg:    " + str(sum/len(times)) + "s"
    
    result = []
    
    count = 0
    for r in x[0]:
        count += 1
        print str(count).rjust(4,'0'),
        print str(len(r)).rjust(4,'0'),
        result.extend(r)
        print r
    
    count = 0
    for r in x[1]:
        count += 1
        print str(count).rjust(4,'0'),
        print str(len(r)).rjust(4,'0'),
        result.extend(r)
        print r
        

        