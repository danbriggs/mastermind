#Note: old mastermind.py and mastermind2.py programs are in "mastermind" folder
#This one is for the Situation class
#Reminder: a response of (4,0) means the game is done,
#but any other response narrowing it down to one possibility needs another guess!

import random
import time

class Situation:
    """Models a mastermind situation."""
    def __init__(self, guess, codelist):
        """Constructs the mastermind situation where
        the possibilities were codelist, and a given
        guess was put forth."""
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
                if curr_result == (4,0):
                    self.numguesses_dict[curr_result] = 0
                else:
                    self.numguesses_dict[curr_result] = None
        for k in self.results_dict:
            if len(self.results_dict[k]) == 2: #may have to try both
                self.nextguess_dict[k] = self.results_dict[k][0]
                self.numguesses_dict[k] = 2
            elif k != (4,0) and len(self.results_dict[k]) == 1:
                self.nextguess_dict[k] = self.results_dict[k][0]
                self.numguesses_dict[k] = 1
    def maxNodeSize(self):
        return max(len(li) for li in self.results_dict.values())
    def pretty_print(self):
        print("Codelist is of length",len(self.codelist),
              "\nand is",stry(self.codelist))
        print("Guess is ",''.join(self.guess))
        print("Results are")
        prd(self.results_dict,self.nextguess_dict,self.numguesses_dict)
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
        for (result,codelist) in self.results_dict.items():
            if self.numguesses_dict[result] is None and (
                max_node_size is None or len(codelist) <= max_node_size):
                success = False
                if len(codelist) <= 14: #incorrectly had 10 before
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
                #of size greater than 14 may be thrown out.
                if not do_recurse:
                    continue #Would take too long otherwise
                answer = None
                bestGuess = None
                if len(codelist) <= 196: #incorrectly had 100 before
                    noisy = False
                    if result==(0,2) and len(codelist)==36:
                        noisy = True
                        print("Turning the noise on")
                    for guess in all_codes:
                        next_turn = Situation(guess,codelist)
                        next_turn.compute_nodes(max_node_size=14, do_recurse = False) #note 14
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
                    if noisy:
                        print("answer was",answer,"with bestGuess",bestGuess,"and situation")
                        next_turn.pretty_print()
                    continue
                #Now we know that all possible guesses after result need to grant the possibility
                #of needing to be followed up by more than two more guesses, since if one of them
                #could guarantee finishing up after two more guesses after it, then (1) it would
                #split codelist into a distribution in which no cluster was larger than 10 codes,
                #and (2) to each cluster there would have been a guess that dissolved that cluster
                #into singletons; we would have discovered this in the single recursion.
                #Thus, if there *is* a guess that can be followed up by *exactly three* more guesses,
                #thus making numguesses be equal to 4, we can just use that guess and be done;
                #because I suspect there *is*, in at least most cases, and possibly every case,
                #let's do heuristics for smart guessing.
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
    if len(li)<=10:
        return [''.join(x) for x in li]
    else:
        return [''.join(x) for x in li[:5]]+['....']+[''.join(x) for x in li[-4:]]

def prd(di,di2,di3):
    """Pretty prints three dictionaries sharing keys."""
    for result in di.keys():
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

colors = ['R','O','Y','G','B','V']

def gen_codes(n):
    """generates all codes of length up to n"""
    global colors
    codes = [[[]]]
    for i in range(n):
        codes.append([])
        for code in codes[-2]:
            codes[-1].extend(all_extensions(code))
    return codes[-1]

def all_extensions(code):
    global colors
    return [code+[c] for c in colors]

all_codes = gen_codes(4)

def main():
    global all_codes
    guesses = []
    for n in range(5):
        guessnums = [random.randint(0,5) for x in range(4)]
        guess = [colors[i] for i in guessnums]
        guesses.append(guess)
    codenums = [random.randint(0,5) for x in range(4)]
    code = [colors[i] for i in codenums]

    print([''.join(guess) for guess in guesses])
    print(''.join(code))

    print(code,'is code')
    responses = []
    for guess in guesses:
        result = response(guess, code)
        print(guess, result)
        responses.append(result)
        sit = Situation(guess, all_codes)
        #sit.pretty_print()

    #first_strings = ['RRRR','RRRO','RROO','RROY','ROYG']
    first_string = input("Initial guess? Use ROYGBV e.g., RROY:")
    first_strings = [first_string]
    first_guesses = [list(s) for s in first_strings]
    print('first guesses',first_strings)
    t1 = time.time()
    for guess in first_guesses[::-1]:
        sit = Situation(guess, all_codes)
        #sit.pretty_print()
        sit.compute_nodes(max_node_size=700) #Attempts to compute the nodes for your first guess.
        #Lower the max_node_size if you'd prefer an incomplete but faster run.
        sit.pretty_print()
    t2 = time.time()
    duration = t2 - t1
    print("Duration:",duration)

if __name__ == '__main__':
    main()
