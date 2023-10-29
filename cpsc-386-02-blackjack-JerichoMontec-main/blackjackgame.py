#!/usr/bin/python3
#Jericho Montecillo
#jerichomontec@csu.fullerton.edu
#CPSC 386-01
#@JerichoMontec

"""
module sys allows for exiting

module blackjackgame.__init__ has all the classes and functions for blackjack
"""

import sys
from blackjackgame.__init__ import *

if __name__ == "__main__":
    game = Game()
    RETURN_VALUE = game.run()
    sys.exit(RETURN_VALUE)
