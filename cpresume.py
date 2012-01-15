#!/usr/bin/env python

from sys  import argv # parse arguments
from os   import path # read file size
from time import time # estimation of time left

# size of chunks for read write actions and overlap
chunkSize, overlap = 2**10, 2**20

# check for correct call
if len(argv) != 3:
    raise Exception ("wrong number of arguments - use: cpresume origin target")
else:
    origin = argv[1]
    target = argv[2]

# check if origin != target
if origin == target:
    raise Exception ("don't use the same file for origin and target'")

# check if target can be resumed
if path.getsize(origin) <= path.getsize(target): 
    raise Exception ("cannot resume because size of origin <= size of target")
else:
    originSize = path.getsize(origin)
    targetSize = path.getsize(target)

# open both files
with open (origin, 'rb') as originFile:
    with open(target, 'ab+') as targetFile:
        
        # if target is not empty check overlap
        if targetSize > 0:

            # calculate maximal overlay region and set file handler
            checkArea = min(overlap, targetSize)
            originFile.seek(targetSize - checkArea)
            targetFile.seek(targetSize - checkArea)
            
            if originFile.read(checkArea) != targetFile.read(checkArea):
                raise Exception ("files do not match at resuming position")

        # remember time and targetSize before copying
        startTime, currentSize = time(), targetSize

        # copy, copy, copy
        while currentSize < originSize:        
            
            # finally copy
            targetFile.write(originFile.read(chunkSize))
            currentSize += chunkSize
            
            # calculate output
            vel = (currentSize - targetSize) / (time() - startTime)
            tau = max(0, (originSize - currentSize) / vel)
            per = 100.0 * currentSize / originSize

            # and print it
            print "\r%2.2f percent copied"  % per,        \
                  "\t%2.0f minutes left"    % (tau / 60), \
                  "\t%2.2f kiB/s bandwidth" % (vel / 1024),
