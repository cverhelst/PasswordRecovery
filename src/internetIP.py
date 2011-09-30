# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Cameron"
__date__ ="$9-jul-2011 23:36:35$"

import urllib

def getIP():
    
    whatismyip = 'http://automation.whatismyip.com/n09230945.asp'
    return urllib.urlopen(whatismyip).readlines()[0]

if __name__ == "__main__":
    print getIP()
    

