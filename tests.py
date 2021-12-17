from project import *
from random import randint

def lowEntropyTest():
    entropy = 5
    return reverseEntropy(entropy) == -5
        
def highEntropyTest():
    entropy = 999999999999
    return reverseEntropy(entropy) == -999999999999

def randomEntropyTest():
    for i in range(1000):
        entropy = randint(1, 100000000)
        if reverseEntropy(entropy) != -entropy:
            return False

    return True

if __name__ == '__main__':
    print(lowEntropyTest())
    print(highEntropyTest())
    print(randomEntropyTest())