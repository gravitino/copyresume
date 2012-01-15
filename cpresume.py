from sys import argv
from os  import path

# size of chunks for read write actions
chunkSize = 2**20

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

with open (origin, 'rb') as originFile:
    with open(target, 'ab+') as targetFile:
        
        print originSize, targetSize

        if targetSize > 0:
            originFile.seek(targetSize - 1)
            targetFile.seek(targetSize - 1)
            if originFile.read(1) != targetFile.read(1):
                raise Exception ("files do not match at resuming position")

        if targetSize > 100:
            originFile.seek(targetSize - 101)
            targetFile.seek(targetSize - 101)
            if originFile.read(101) != targetFile.read(101):
                raise Exception ("files do not match at resuming position")

        while targetSize < originSize:        
            targetFile.write(originFile.read(chunkSize))
            print "%2.2f" % (float(targetSize) / float(originSize) * 100)
            targetSize += chunkSize
