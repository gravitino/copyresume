from sys import argv

# check for correct call
if len(argv) != 3:
    raise Exception ("wrong number of arguments - use: cpresume origin target")

# check if origin != target
if argv[1] == argv[2]:
    raise Exception ("don't use the same file for origin and target'")

origin = argv[1]
target = argv[2]

with open (origin, 'rb') as originFile:
    with open(target, 'wb') as targetFile:
        print dir(originFile)
