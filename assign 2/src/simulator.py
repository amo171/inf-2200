'''
Code written for inf-2200, University of Tromso
'''

import sys
from mipsSimulator import MIPSSimulator

def runSimulator(sim):
    # Replace this with your own main loop!
    while (1):
        sim.tick()

if __name__ == '__main__':
    assert(len(sys.argv) == 2), 'Usage: python %s memoryFile' % (sys.argv[0],)
    memoryFile = sys.argv[1]

    simulator = MIPSSimulator(memoryFile)
    runSimulator(simulator)
