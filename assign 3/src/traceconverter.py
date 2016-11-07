# -*- coding: utf-8 -*-

#
# traceconverter.py
#
#------------------------
# By Øyvind Holmstad
# For Inf-2200 Fall 2010
#------------------------
#
# A script converting a memory trace created with valgrind+lackey to the BYU Address Trace Format
#
# The valgrind command used to produce compatible log trace files:
# ./valgrind --log-file=logfile --tool=lackey --trace-mem=yes [your-program-name]
#
# Output is saved in trace.tr
#

from struct import *

def main():
    fmt = '<LBBBBL'
    
    logfile = open('logfile', 'r')
    tracefile = open('trace.tr', 'wb')
    
    for line in logfile:
        if line.startswith('=='): # Comment
            continue
        else: # Memory instruction
            
            # Determine type
            reqtype = 0
            atype = line[0:3].strip()
            if atype == 'I':
                reqtype = 0
            elif atype == 'S':
                reqtype = 3
            elif atype == 'L':
                reqtype = 1
            else: 
                continue
            
            if len(line) < 13:
                continue
            
            # Read address
            address = int(line[3:11], 16)
            
            # Read size
            size = int(line[12:13])
            
            # Pack to binary and write to file
            a = pack(fmt, address, reqtype, size, 0, 0, 0)
            tracefile.write(a)
        
    logfile.close()
    tracefile.close()


if __name__ == "__main__":
    main()
