import random
import time

class Situation:
    """Models a general mastermind situation."""
    def __init__(self, guess, codelist):
        """Constructs the mastermind situation where
        the possibilities were codelist, and a given
        guess was put forth."""
        global codelen
        self.guess = guess
        self.codelist = codelist
        self.results = []
        for code in self.codelist:
            result = response(self.guess,code)
            self.results.append(result)
        self.results_dict = {}
        self.nextguess_dict = {}
        self.numguesses_dict = {}
        for i in range(len(self.results)):
            curr_result = self.results[i]
            curr_code = self.codelist[i]
            if curr_result in self.results_dict:
                self.results_dict[curr_result].append(curr_code)
            else:
                self.results_dict[curr_result] = [curr_code]
                self.nextguess_dict[curr_result] = None
                if curr_result == (codelen,0):
                    self.numguesses_dict[curr_result] = 0
                else:
                    self.numguesses_dict[curr_result] = None
        for k in self.results_dict:
            if len(self.results_dict[k]) == 2: #may have to try both
                self.nextguess_dict[k] = self.results_dict[k][0]
                self.numguesses_dict[k] = 2
            elif k != (codelen,0) and len(self.results_dict[k]) == 1:
                self.nextguess_dict[k] = self.results_dict[k][0]
                self.numguesses_dict[k] = 1
    def maxNodeSize(self):
        return max(len(li) for li in self.results_dict.values())
    def pretty_print(self, order=0):
        print("Codelist is of length",len(self.codelist),
              "\nand is",stry(self.codelist))
        print("Guess is ",''.join(self.guess))
        print("Resp.  #Possibs Next Trns Possibilities")
        prd(self.results_dict,self.nextguess_dict,self.numguesses_dict, order=order)
        print("Max node size",self.maxNodeSize())
    def done(self):
        """Returns whether all nodes are decorated."""
        for k in self.results_dict:
            if self.numguesses_dict[k] is None:
                return False
        return True
    def numTurns(self, force_eval=False):
        """Returns the maximum possible number of turns the game may take
        AFTER the current situation."""
        if not force_eval:
            if not self.done():
                return None
        return max(self.numguesses_dict.values())
    def compute_nodes(self, max_node_size=None, do_recurse = True):
        """Attempts to compute the situations with codelists of length
        at most max_node_size that haven't been computed yet."""
        di = self.results_dict
        enumerator = sorted(di, key=(lambda x:len(di[x])), reverse=True)
        for result in enumerator:
            codelist = di[result]
            if self.numguesses_dict[result] is None and (
                max_node_size is None or len(codelist) <= max_node_size):
                success = False
                max_num_responses = triangle_num(codelen)
                if len(codelist) <= max_num_responses:
                    #Try all codes to see if any splits codelist completely
                    for guess in all_codes: #This takes long :(
                        if dissolves(codelist, guess):
                            self.nextguess_dict[result] = guess
                            self.numguesses_dict[result] = 2
                            success = True
                            break
                    if success:
                        continue
                #Now we know that no single guess after self.guess dissolves codelist,
                #so cannot guarantee end in another 2 moves. If we're gunning to be
                #done in another 3 moves, any guess whose split leaves a cluster
                #of size greater than 10 may be thrown out.
                if not do_recurse:
                    continue #Would take too long otherwise
                answer = None
                bestGuess = None
                if len(codelist) <= max_num_responses**2:
                    for guess in all_codes:
                        next_turn = Situation(guess,codelist)
                        next_turn.compute_nodes(max_node_size=max_num_responses, do_recurse = False)
                        if next_turn.done():
                            val = next_turn.numTurns()
                            if answer is None or val < answer:
                                answer = val
                                bestGuess = guess
                                if answer == 2: #Min possible
                                    break
                if answer is not None:
                    self.nextguess_dict[result] = bestGuess
                    self.numguesses_dict[result] = answer+1
                    continue
                #Now we know that all possible guesses after result need to grant the possibility
                #of needing to be followed up by more than two more guesses, since if one of them
                #could guarantee finishing up after two more guesses after it, then (1) it would
                #split codelist into a distribution in which no cluster was larger than max_num_responses
                #codes, and (2) to each cluster there would have been a guess that dissolved that cluster
                #into singletons; we would have discovered this in the single recursion.
                #Thus, if there *is* a guess that can be followed up by *exactly three* more guesses,
                #thus making numguesses be equal to 4, we can just use that guess and be done.
                minMax = None
                bestTry = None
                bestSit = None
                print("Beginning total recursion for cluster of size",len(codelist))
                time_start = time.time()
                for guess in all_codes:
                    next_turn = Situation(guess, codelist)
                    maxSize = next_turn.maxNodeSize()
                    if minMax is None or maxSize < minMax:
                        minMax = maxSize
                        bestTry = guess
                        bestSit = next_turn
                print("Suggested followup is",bestTry,"with max node size",minMax,"and situation")
                bestSit.pretty_print()
                bestSit.compute_nodes() #Try computing them *with* recursion, hopefully they're small.
                #Hopefully they finish, and hopefully the max they say is 3.
                if bestSit.done():
                    bestSitNumTurns = bestSit.numTurns()
                    self.nextguess_dict[result] = bestTry
                    self.numguesses_dict[result] = bestSitNumTurns + 1
                    print("Recursion completed in",time.time()-time_start,"seconds with")
                    bestSit.pretty_print()
                else:
                    print("Warning: the suggested guess has not finished being evaluated.")
                
def triangle_num(n):
    return n*(n+1)//2
                
def dissolves(codelist,guess):
    results = []
    for code in codelist:
        result = response(guess, code)
        if result in results:
            return False
        results.append(result)
    return True        

def stry(li):
    """Like str, but joins members' elements, and abbreviates if more than 10"""
    global codelen
    if len(li)<=10:
        return [''.join(x) for x in li]
    else:
        return [''.join(x) for x in li[:5]]+['.'*codelen]+[''.join(x) for x in li[-4:]]

def prd(di,di2,di3,order=0):
    """Pretty prints three dictionaries sharing keys."""
    if order > 0:
        enumerator = sorted(di, key=(lambda x:len(di[x])))
    elif order < 0:
        enumerator = sorted(di, key=(lambda x:len(di[x])), reverse=True)
    else:
        enumerator = di
    for result in enumerator:
        print(result, len(di[result]),'\t',
              comp(di2[result]),di3[result], stry(di[result]))

def comp(li):
    if li:
        return ''.join(li)
    else:
        return li

def response(guess, code):
    """The number of correct guesses in the correct place,
    followed by the remaining number of correct guesses in the wrong place"""
    is_correct = [guess[i]==code[i] for i in range(len(code))]
    num_right = sum(is_correct)
    is_used = is_correct.copy()
    num_displaced = 0
    for i in range(len(guess)):
        if not is_correct[i]:
            for j in range(len(code)):
                if not is_used[j] and guess[i]==code[j]:
                    num_displaced += 1
                    is_used[j] = True
                    break
    return num_right, num_displaced

def gen_colors(n):
    """ABC... instead of ROYGBV"""
    return [chr(i) for i in range(ord('A'),ord('A')+n)]

def gen_codes(n):
    """generates all codes of length up to n"""
    codes = [[[]]]
    for i in range(n):
        codes.append([])
        for code in codes[-2]:
            codes[-1].extend(all_extensions(code))
    return codes[-1]

def all_extensions(code):
    global colors
    return [code+[c] for c in colors]

numColors = int(input('Number of colors?'))
colors = gen_colors(numColors)
codelen = int(input('Length of codes?'))
gen_start = time.time()
all_codes = gen_codes(codelen)
gen_end = time.time()
print("OK. Generated",len(all_codes),"codes in",gen_end-gen_start,"seconds.")

def main():
    global all_codes
    
    first_guess = ['A','B','C','D']
    if codelen <= 4:
        first_guess = first_guess[:codelen]
    else:
        first_guess = first_guess + ['C']*(codelen-4)
    print('first guess',''.join(first_guess))
    t1 = time.time()
    sit = Situation(first_guess, all_codes)
    sit.pretty_print(order = -1)
    sit.compute_nodes()
    sit.pretty_print()
    t2 = time.time()
    duration = t2 - t1
    print("Duration:",duration)

if __name__ == '__main__':
    main()
