"""Aims to determine how often a situation with from 3 to (k+1)k/2 codes
can be won in two guesses, where k is the length of codes.
Note: these statistics may *not* be representative of the situations we
find as we try to solve, because they are not completely random."""

from mastermind_general_2 import *

def gen_randoms(start, stop, numEach):
    """Returns numEach sets of i random codes
    for each i from start to stop."""
    theLists = []
    for i in range(start, stop+1):
        theLists.append([])
        for j in range(numEach):
            nums = gen_random_numbers(i, 0, len(all_codes) - 1)
            codes = [all_codes[x] for x in nums]
            theLists[-1].append(codes)
    return theLists

def do_stats():
    data = gen_randoms(5, 21, 10)
    interesting_set = ['BCDCAC', 'BDACCC', 'CBDACC', 'DACCCB', 'DBACCC', 'DCCCBA']
    data[1].insert(0,[list(x) for x in interesting_set])
    #print("data:",data)
    for sets in data:
        setlen = len(sets[0])
        print("Working with sets of length",setlen)
        for x in sets: #x consists of setlen random codes
            numSuccesses = 0
            for code in all_codes:
                sit = Situation(code, x, 2)
                #sit.pretty_print()
                #input("pause")
                maxSize = sit.maxNodeSize()
                if maxSize == 1:
                    numSuccesses += 1
            print("numSuccesses:",numSuccesses,"out of",len(all_codes))
        #input("pause")

if __name__ == "__main__":
    #do_stats()
