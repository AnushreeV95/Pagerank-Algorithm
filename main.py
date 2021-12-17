import re, sys
from project import *

entropy = int(sys.argv[1])
outFile = sys.argv[2]

with open(outFile,'x') as myFile:
    myFile.write(str(reverseEntropy(entropy)))