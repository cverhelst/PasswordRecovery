# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="cameron"
__date__ ="$Sep 19, 2011 8:52:21 PM$"


from controller import Controller

import yappi

if __name__ == "__main__":
    yappi.start()
    c = Controller()
    c.main()
    yappi.print_stats()
