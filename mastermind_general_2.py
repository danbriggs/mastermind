"""In this version, we try to avoid requiring the program to iterate through
all possible codes unless absolutely needed. Instead, we keep track of what the
best result we could hope for is, and try to achieve it as quickly as possible.
If it's not possible, then that's because there is a response to which all
follow-ups require more than n (say) guesses. At *that* point, we have to
iterate through all the guesses, showing for each one that either the size of
the largest cluster got is too big, or that some cluster requires more than
n-1 guesses.

Clearly, we can't *know* that the response requires too many guesses until we've
tried to go through each process; each of the two distinct processes may be long,
and a priori it's impossible to say which of the two is longer. So for each
response to a given first (say) guess, we should keep track of three things:
(1) the lower bound for how many more guesses it will take,
(2) the upper bound for how many more guesses it will take,
(3) whether that response has child nodes representing partially-completed
    computations (situations).
It is important to try to keep the total number of places where (3) is yes
below a reasonable bound for the sake of memory."""

import random
import time

class Situation:
    """Models a general mastermind situation."""
    def __init__(self, guess, codelist, goal=None, parent=None):
        """Constructs the mastermind situation where
        the possibilities were codelist, and a given
        guess was put forth.
        If goal is provided, then we're trying to determine
        whether the game can be guaranteed to wrap up in at
        most goal further guesses."""
        global codelen
        if goal is None:
            goal = ceil_log(triangle_num(codelen+1)-1,len(codelist))
            #For example, in the classic 6-color length-4 situation,
            #there are at most 14 possible responses to the first guess
            #since a response of (codelen - 1, 1) is impossible,
            #thus 5+4+3+1+1; since the initial codelist is of length 1296,
            #and 14^3 > 1296 > 14^2, we're trying to see if the game can wrap up
            #in at most 3 more guesses after the first guess. (It can't.)
        if parent is None:
            self.level = 0
        else:
            self.level = parent.level + 1
        self.goal = goal
        self.guess = guess
        self.codelist = codelist
        self.results = []
        for code in self.codelist:
            result = response(self.guess,code)
            self.results.append(result)
        self.results_dict = {}
        self.nextguess_dict = {}
        self.loguesses_dict = {}
        self.higuesses_dict = {}
        self.children_dict = {}
        for i in range(len(self.results)):
            curr_result = self.results[i]
            curr_code = self.codelist[i]
            if curr_result in self.results_dict:
                self.results_dict[curr_result].append(curr_code)
            else:
                self.results_dict[curr_result] = [curr_code]
                self.nextguess_dict[curr_result] = None
                self.children_dict[curr_result] = None
                if curr_result == (codelen,0):
                    self.loguesses_dict[curr_result] = 0
                    self.higuesses_dict[curr_result] = 0
        for k in self.results_dict:
            if k != (codelen,0):
                self.loguesses_dict[k] = ceil_log(
                    triangle_num(codelen+1)-1, len(self.results_dict[k]))+1
                self.higuesses_dict[k] = len(self.results_dict[k])
            if len(self.results_dict[k]) == 2:
                self.nextguess_dict[k] = self.results_dict[k][0]
            elif k != (codelen,0) and len(self.results_dict[k]) == 1:
                self.nextguess_dict[k] = self.results_dict[k][0]
        self.max_node_size = self.maxNodeSize()
    def is_conceivable(self):
        """Returns whether it's still conceivable based the lower bounds on the number of guesses
        that the goal is achievable."""
        if max(self.loguesses_dict.values()) > self.goal:
            return False
        return True
    def maxNodeSize(self):
        return max(len(li) for li in self.results_dict.values())
    def pretty_print(self, order=0):
        print("Codelist is of length",len(self.codelist),
              "and is",stry(self.codelist))
        print("Guess is",''.join(self.guess),
              "and goal is to finish in at most",self.goal,"more guesses")
        print("Respon\t#Possib\t","Next\t",
              "Lo\t","Hi\t","Chl Possibilities")
        prd(self.results_dict, self.nextguess_dict,
            self.loguesses_dict, self.higuesses_dict,
            self.children_dict, order=order)
        print("Max node size",self.maxNodeSize())
    def done(self):
        """Returns whether all nodes are decorated."""
        for k in self.results_dict:
            if self.numguesses_dict[k] is None:
                return False
        return True
    def allDone(self):
        for k in self.results_dict:
            if self.higuesses_dict[k] > self.goal:
                return False
            elif self.nextguess_dict[k] is None:
                print("Warning: in Situation.allDone():",
                      "higuesses is low enough but no next guess has been assigned.")
        return True
    def numTurns(self, force_eval=False):
        """Returns the maximum possible number of turns the game may take
        AFTER the current situation."""
        if not force_eval:
            if not self.done():
                return None
        return max(self.numguesses_dict.values())
    def maxhi(self):
        """Returns the maximum upper bound number of guesses after this one over all responses."""
        return max(self.higuesses_dict.values())
    def maxlo(self):
        """Returns the maximum lower bound number of guesses after this one over all responses."""
        return max(self.loguesses_dict.values())
    def won(self):
        return self.maxhi() <= self.goal
    def lost(self):
        return self.maxlo() > self.goal
    def compute_nodes(self, max_node_size=None, do_recurse = True,
                      critical = False, numTries = 5, use_symmetry = False):
        """Attempts to compute the situations with codelists of length
        at most max_node_size that haven't been computed yet.
        numTries indicates the number of iterations of random index generation to try.
        use_symmetry should only be used if self is a first guess situation;
        otherwise the result will be incorrect. It only matters in the critical case."""
        global all_codes
        if self.lost():
            return #If the goal is unachievable, no point in trying.
        di = self.results_dict
        enumerator = sorted(di, key=(lambda x:len(di[x])), reverse=True)
        enumlen = len(enumerator)
        results_covered = 0
        enumlist = all_codes
        if use_symmetry:
            enumlist = sym_reduce_all(self.guess)
        for result in enumerator:
            codelist = di[result]
            if not critical:
                start = time.time()
                bestSituation, bestTop = best_random_situation(codelist, self.goal, numTries, numTries, parent = self)
                end = time.time()
                #print("Took",end-start,"seconds.")
                #print("Proceeding with situation:")
                #bestSituation.pretty_print()
                #print("Its goal is",bestSituation.goal)
                bestHope = ceil_log(triangle_num(codelen+1)-1,bestTop) + 1
                #print("and by math, the best we can hope for is",bestHope)
                if bestSituation.goal < bestHope:
                    pass
                else:
                    #print("So we may as well proceed.")
                    self.children_dict[result] = bestSituation
                    oldhi = self.higuesses_dict[result]
                    self.higuesses_dict[result] = min(oldhi, bestTop + 1)
                    if self.higuesses_dict[result] <= self.goal:
                        self.nextguess_dict[result] = bestSituation.guess
                        self.children_dict[result] = 'Don'
                continue #Skip the next 70 or so lines to see how it proceeds
            elif critical:
                #Now we actually have to look at all possibilities for the unknowns.
                results_covered += 1
                child = self.children_dict[result]
                if child is 'Don':
                    continue
                sit_list = []
                start = time.time()
                for guess in enumlist:
                    sit = Situation(guess, codelist, self.goal - 1, parent = self) #Hopefully this isn't too slow!
                    if not sit.lost():
                        sit_list.append(sit)
                sitlen = len(sit_list)
                print(sitlen, "situations out of", len(enumlist),
                      "were not obviously lost and thus put in sit_list.")
                end = time.time()
                print("Critical compute: situation generation took",end-start,"seconds.")
                sit_list.sort(key = lambda x: x.max_node_size)
                print("List sort took",time.time()-end,"seconds.")
                success = False
                sitnum = 0
                for sit in sit_list:
                    sitnum += 1
                    if sit.lost():
                        continue
                    self.children_dict[result] = sit
                    
                    sit.compute_nodes(critical=False, numTries=5, do_recurse=False)
                    #Was numTries = 20, do_recurse = True
                    if not sit.won():
                        sit.compute_nodes(critical=True)
                        sit.purge_children()
                    if sit.won():
                        success = True
                        break
                    else:
                        if self.level <= 1:
                            print("At level",self.level,"response",results_covered,"of",enumlen,
                                  "guess",sitnum,"of",sitlen,"could not be won.")
                if success:
                    print("Yes, the response",self.results_dict[result],
                          "(response "+str(results_covered)+"/"+str(enumlen),
                          "at level "+str(self.level)+") was won.")
                    continue
                else:
                    print("No, the response",result,"giving",
                          len(self.results_dict[result]),"possibilities",
                          "(response "+str(results_covered)+"/"+str(enumlen),
                          "at level "+str(self.level)+")",
                          "could not be won in",self.goal,"moves.")
                    self.loguesses_dict[result] = self.goal+1
                    self.purge_children()
                    if self.level == 0:
                        self.pretty_print()
                    return
            if self.numguesses_dict[result] is None and (
                max_node_size is None or len(codelist) <= max_node_size):
                success = False
                max_num_responses = triangle_num(codelen+1)-1
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
                        next_turn = Situation(guess,codelist, parent = self)
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
                    next_turn = Situation(guess, codelist, parent = self)
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
        if critical:
            self.update_his()
            self.purge_children()
            if level <= 1:
                print("From critical compute end:")
                self.pretty_print(order='hi_desc')
                if level == 0:
                    input("pause")
        elif not critical and do_recurse:
            #print("Now the situation is")
            #self.pretty_print(order = 'hi_desc') #Display in descending order of higuesses.
            #This is the order in which we'd like to try to work it out, since if it can't
            #be done, we're more likely to find out sooner.
            #input("Pause")
            start = time.time()
            numDone = 0
            numTotal = len(self.results_dict)
            for result in sorted(self.higuesses_dict, key=self.higuesses_dict.get, reverse=True):
                child = self.children_dict[result]
                if child is None:
                    continue #We should figure out what to do about this later
                elif child is 'Don':
                    continue #This node has been solved
                child.compute_nodes(do_recurse=False)
                #We will remove the do_recurse=False later, this is just better for testing
                oldhi = self.higuesses_dict[result]
                self.higuesses_dict[result] = min(oldhi, child.maxhi()+1)
                numDone += 1
                #print("Fraction done:",numDone/numTotal)
            #self.pretty_print(order = 'hi_desc')
            print("Time elapsed:",time.time() - start)
            for result in sorted(self.higuesses_dict, key=self.higuesses_dict.get, reverse=True):
                #Now we try to make some of the children finish up.
                #Trying all possible codes is extremely inefficient, and we don't need to, because
                #we're not in a critical situation. On the other hand, we may need to recurse as many
                #as goal times to figure it out. We use the Situation.boil() method to do this.
                child = self.children_dict[result]
                if child is None or child is 'Don':
                    continue
                child.boil(False)
            self.update_his()
            self.purge_children()
            #print("After boiling and purging all children:")
            #self.pretty_print(order = 'hi_desc')
            #input("Pause line 253")
            #Now the situation is slightly warmer. Try computing more random situations.
            #successes = 0
            #failures = 0
            #for result in sorted(self.higuesses_dict, key=self.higuesses_dict.get, reverse=True):
            #    child = self.children_dict[result]
            #    codelist = self.results_dict[result]
            #    if child is not None and child is not 'Don':
            #        bestSit, bestTop = best_random_situation(codelist, self.goal, 20, 20)
            #        bestSit.compute_nodes(do_recurse = False, numTries = 20)
            #        bestSit.boil(depth = 1)
            #        print("bestSit.maxhi() is",bestSit.maxhi(),"and child.maxhi() is",child.maxhi())
            #        if bestSit.maxhi() < child.maxhi():
            #            successes += 1
            #            self.children_dict[result] = bestSit
            #            self.higuesses_dict[result] = bestTop
            #        else:
            #            failures += 1
            #self.update_his()
            #print(successes,"successes and",failures,"failures,")
            #self.purge_children()
            #self.pretty_print(order='hi_desc')
            #input("Pause line 273")
                        
                    
    def update_his(self):
        """Reduces each higuess according to one more than the max higuess of the corresponding child
        for those children that are still active."""
        for result in self.results_dict:
            child = self.children_dict[result]
            if child is None or child is 'Don':
                continue
            oldhi = self.higuesses_dict[result]
            self.higuesses_dict[result] = min(oldhi, child.maxhi()+1)
    def purge_children(self):
        """For each hi that is less than or equal to the goal,
        takes the guess from the child and turns the child into 'Don'."""
        for result in self.results_dict:
            child = self.children_dict[result]
            if child is None or child is 'Don':
                continue
            if self.higuesses_dict[result] <= self.goal:
                self.nextguess_dict[result] = child.guess
                self.children_dict[result] = 'Don'
    def boil(self, critical = False, depth = 1):
        """Given that the goal is to finish in at most goal more turns, we attempt a good-faith
        effort to show by recursion that this can happen in the case of each of the responses.
        Use a depth greater than 1 to recurse."""
        #print("My goal is to finish up in at most",self.goal,"more turns and I look like this:")
        #self.pretty_print(order='hi_desc')
        #input("Pause")
        for result in sorted(self.higuesses_dict, key=self.higuesses_dict.get, reverse=True):
            child = self.children_dict[result]
            if child is not None and child is not 'Don':
                #child.pretty_print(order = 'hi_desc')
                child.compute_nodes(do_recurse = False)
                #print("After computation:")
                #child.pretty_print(order = 'hi_desc')
                if not child.allDone():
                    child.compute_nodes(do_recurse = False, numTries = 15)
                    if depth > 1:
                        child.boil(depth = depth - 1)
                    #print("After more computation:")
                    #child.pretty_print(order = 'hi_desc')
                #input("Pause line 312")
        self.update_his()
        #print("After updating his:")
        #self.pretty_print(order = 'hi_desc')
        self.purge_children()
        #print("After purging children:")
        #self.pretty_print(order = 'hi_desc')
        #input("Pause line 319")
                
def best_random_situation(codelist, goal, codelist_tries = 5, allcodes_tries = 5, parent = None):
    """Generates codelist_tries + allcodes_tries random guesses from codelist and all_codes,
    respectively, and returns a pair consisting of the one that has the smallest largest node
    splitting codelist, and the size of that node."""
    global all_codes
    #print("Starting inspection for result",result)
    li1 = gen_random_numbers(codelist_tries, 0, len(codelist) - 1)
    li2 = gen_random_numbers(allcodes_tries, 0, len(all_codes) - 1)
    #If the situation isn't critical, then we're just trying
    #to determine if there is a "good enough" guess to guarantee
    #the game wrapping up in at most self.goal more turns.
    #To this end, we choose numTries random codes among the possible winners
    #and five random codes among all possible codes,
    #inspect their distributions, and go with the one with the lowest max,
    #throwing the other nine out.
    guesses1 = [codelist[i] for i in li1]
    guesses2 = [all_codes[i] for i in li2]
    bestSituation = None
    bestTop = None
    for guess in guesses1:
        sit = Situation(guess, codelist, goal = goal - 1, parent = parent)
        top = sit.maxNodeSize()
        #print("A possible correct guess gives a max node size of",top)
        if bestSituation is None or top < bestTop:
            bestSituation = sit
            bestTop = top
    for guess in guesses2:
        sit = Situation(guess, codelist, goal = goal - 1, parent = parent)
        top = sit.maxNodeSize()
        #print("A completely random guess gives a max node size of",top)
        if top < bestTop:
            bestSituation = sit
            bestTop = top
    return bestSituation, bestTop


def gen_random_numbers(numnums, m, M):
    return [random.randint(m,M) for i in range(numnums)]
                
def triangle_num(n):
    return n*(n+1)//2

def ceil_log(b,x):
    if b <= 1:
        print("Error:",b,"used as base in ceil_log")
        return 0
    ans = 0
    prod = 1
    while prod < x:
        prod *= b
        ans += 1
    return ans
      
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

def prd(di,di2,di3,di4,di5,order=0):
    """Pretty prints four dictionaries sharing keys."""
    if order == 'hi_desc':
        enumerator = sorted(di, key=di4.get, reverse=True)
    elif order > 0:
        enumerator = sorted(di, key=(lambda x:len(di[x])))
    elif order < 0:
        enumerator = sorted(di, key=(lambda x:len(di[x])), reverse=True)
    else:
        enumerator = di
    for result in enumerator:
        print(result, '', len(di[result]),'\t',
              str(comp(di2[result]))+'\t',di3[result],'\t',di4[result],'\t',
              yesno(di5[result]),stry(di[result]))

def yesno(obj):
    if obj is None:
        return 'No '
    elif obj == 'Don':
        return 'Don'
    else:
        return 'Yes'

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

def all_firsts(symbs, to_fill, first_index_max = 0):
    """Returns a list of all codes that are in alphabetical order and don't skip a letter.
    These are the only ones necessary to try as a first code."""
    if to_fill == 0:
        return [[]]
    if symbs == []:
        return [[]]
    #Only the head symbol or the next symbol may be used in the second place.
    poss = []
    for i in range(0,min(len(symbs),first_index_max+1)):
        poss += [[symbs[i]]+x for x in all_firsts(symbs[i:], to_fill - 1, first_index_max = 1)]
    return poss 

def skips_unused_and_lands(code, guess):
    global colors
    guess_last_letter = guess[-1]
    colorIndex = colors.index(guess_last_letter)
    if len(colors) - colorIndex <= 2:
        return False
    lettersOfInterest = colors[colorIndex + 1:]
    hasDict = {color: False for color in lettersOfInterest}
    for ch in code:
        if ch in lettersOfInterest:
            hasDict[ch] = True
    oneWasMissing = False
    for k in sorted(hasDict):
        if not oneWasMissing:
            if hasDict[k] == False:
                oneWasMissing = True
        else:
            if hasDict[k] == True:
                return True
    return False

def unlex(charList):
    for i in range(len(charList) - 1):
        ch1 = charList[i]
        ch2 = charList[i+1]
        if ch2 < ch1:
            return True
    return False

def has_an_unlex_block(code, guess):
    global colors
    spotsWhereLettersShowUpInGuess = {ch: [] for ch in colors}
    for i in range(len(guess)):
        ch = guess[i]
        spotsWhereLettersShowUpInGuess[ch].append(i)
    for _, spots in spotsWhereLettersShowUpInGuess.items():
        codeChars = [code[spot] for spot in spots]
        if unlex(codeChars):
            return True
    return False

def blocks_unlex_re_eqlen_blocks(code, guess):
    return False

def sym_reduce_all(guess):
    global all_codes
    """Produces a list of all the codes worth checking
    in the context of the given first guess.
    TODO: Later, a version from two guesses."""
    #We devise a canonical version of a code in the context of symmetry.
    #First, we verify that the given code does not skip a letter
    #that was not used in guess and include the next letter.
    #For example, if the first guess was AAAAAB, we exclude DABADA.
    #Next, we make sure that the letters appearing in positions
    #corresponding to a letter block of guess come in nondecreasing order.
    #If the first guess was for example AABBCC,
    #DBCCBA would be out because it's equivalent to BDCCAB.
    #Finally, we make sure that letters forming letter blocks in the code
    #made up of positions forming letter blocks in guess of equal size
    #show up in nondecreasing lexicographical order.
    #We take advantage of the fact that we can assume that the first guess
    #was given in canonical order to streamline the process.
    #For example, if the first guess was AABBCC, then the code BDCDAB
    #would be out because AB is before BD in lexicographical order.
    tally1 = 0
    tally2 = 0
    retlist = []
    for code in all_codes:
        if skips_unused_and_lands(code, guess):
            tally1 += 1
            continue
        if has_an_unlex_block(code, guess):
            tally2 += 1
            continue
        if blocks_unlex_re_eqlen_blocks(code, guess):
            continue
        retlist.append(code)
    print("tally1:",tally1)
    print("tally2:",tally2)
    print("len(retlist)",len(retlist))
    return retlist
     
def signature(guess):
    """A given first guess's prospects depend only on its signature,
    meaning how many of each letter shows up. This function returns
    the signature as an ordered list; it is suggested to retain only
    those first guesses whose signature is a nonincreasing sequence."""
    numOccurrences = {}
    for ch in guess:
        if ch in numOccurrences:
            numOccurrences[ch] += 1
        else:
            numOccurrences[ch] = 1
    return list(numOccurrences.values())

def descending_only(li):
    retlist = []
    for x in li:
        sig = signature(x)
        if sorted(sig, reverse=True)==sig:
            retlist.append(x)
    return retlist

def main():
    global all_codes
    global colors
    first_guesses = all_firsts(colors, codelen)
    print("first guesses:",first_guesses)
    filtered_first_guesses = descending_only(first_guesses)
    first_guesses = filtered_first_guesses
    print("Filtered by signature:",first_guesses)
    input("pause")
    numConceivable = 0
    sitList = []
    for first_guess in first_guesses:
        print('first guess',''.join(first_guess),signature(first_guess))
        t1 = time.time()
        sit = Situation(first_guess, all_codes)
        #second argument used to be all_codes
        #sit.pretty_print(order = -1)
        sitList.append(sit)
        if sit.is_conceivable():
            print("The situation was conceivable.")
            numConceivable += 1
    while numConceivable == 0:
        print("No first guesses can be guaranteed to finish up in",sitList[0].goal,
              "moves after the first move. Updating goals.")
        for sit in sitList:
            sit.goal += 1
            if sit.is_conceivable():
                numConceivable += 1
    print("There were",numConceivable,"distinct first guesses for which it is conceivable",
          "that they may be guaranteed to complete in",sitList[0].goal,"moves after the first move.")
    ans = input("Press enter to proceed.")
    wasWon = False
    sitList.sort(key = lambda x: x.max_node_size)
    for sit in sitList:
        sit.compute_nodes()
        if sit.won():
            print("Won!")
            wasWon = True
            break
        else:
            print("Max hi was",sit.maxhi(),"for situation with goal",sit.goal)
            print("Moving on to next first guess.")
    sitList.sort(key = lambda x: x.maxhi())
    for sit in sitList:
        #print("Attempting situation non-critically:")
        print("Attempting situation with max hi",sit.maxhi(),"critically.")
        sit.pretty_print()
        sit.compute_nodes(critical=True, use_symmetry = True)
        sit.pretty_print(order='hi_desc')
        if sit.won():
            print("It was won!")
        input("pause")
    #TODO: If wasWon is still False, then we have proved that the game cannot be guaranteed to end
    #in that many moves. Update goals by adding 1 to them, and try again.
    t2 = time.time()
    duration = t2 - t1
    print("Duration:",duration)
    return sitList

if __name__ == '__main__':
    final_sitlist = main()
