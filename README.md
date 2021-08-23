## General Mastermind ##

In 1977, Don Knuth showed that Mastermind takes 5 guesses.

I didn't know that, so in the spring of 2003 I wrote a LISP/Scheme program that attempted to determine this.

Or so I thought. What the program really did was just run and run, and I'm not sure whether it was because it would really just take that long or I had failed to properly end the recursion.

It turns out that Python is a much better language for this sort of thing (although LISP is of course still beautiful), so I got back at it this week and after a couple days I got 5, and then I looked it up, only to find out the above.

One corollary, though, was that I was able to edit a parenthetical remark in step 2 of the explication of his algorithm in the "Worst case" sub-subsection of the wikipedia page about the game: the commentator, failing to read their Knuth carefully, seemed to have been under the impression that red red orange yellow *cannot* win in five tries, whereas Knuth had only stated that *his* algorithm is not guaranteed to round out play starting with this guess in five tries. Also, I was able to determine that Knuth's hunch that red orange yellow green cannot round out in a total of five tries was incorrect.

Knuth's algorithm, which is sufficient for the board game itself, is to minimize the maximum cluster size among all responses to a given guess other than the first guess. This turns out to work out just fine for red red orange orange, but as he notes, if you begin with the first guess red red orange yellow, after determining that the follow-ups should be orange orange red green and yellow yellow green red, the cluster of six codes pertaining to the response black black cannot be dissolved into single codes by any fourth guess, and neither can the cluster of seven pertaining to black black black.

But if you use my algorithm, the program attempts to determine everything that it can, and chooses a better second and/or third guess.

Admittedly, though, it takes about fifteen minutes to run (the smarter version mastermind_general_2 takes one minute), and I'm not sure what that would scale to in '76/'77 with slower hardware but a faster programming language.

If you do run it, you will likely see a few lines and then the following:
	
	Initial guess? Use ROYGBV e.g., RROY:

so you can type RROO, RROY, or ROYG, to speak of three famous first guesses.

After that, you will see about 350 lines of output, and if your first guess was RROY, then somewhere around line 230 you'll see:

    Turning the noise on
	answer was 2 with bestGuess ['R', 'Y', 'G', 'B'] and situation
	Codelist is of length 36 
	and is ['YYGR', 'YYGO', 'YGYR', 'YGYO', 'YGGR', '....', 'VYGR', 'VYGO', 'VGYR', 'VGYO']
	Guess is  RYGB
	Results are
	(2, 1) 4 	 YRRV 2 ['YYGR', 'GYGR', 'BYGO', 'VYGR']
	(2, 0) 3 	 YRRV 2 ['YYGO', 'GYGO', 'VYGO']
	(0, 3) 8 	 YGRV 2 ['YGYR', 'YGBO', 'YGVR', 'GGYR', 'GBYO', 'GVYR', 'BGYO', 'VGYR']
	(0, 2) 5 	 YGRV 2 ['YGYO', 'YGVO', 'GGYO', 'GVYO', 'VGYO']
	(1, 2) 6 	 RRGV 2 ['YGGR', 'YBGO', 'YVGR', 'GYYR', 'GYBO', 'GYVR']
	(1, 1) 4 	 RRGV 2 ['YGGO', 'YVGO', 'GYYO', 'GYVO']
	(0, 4) 3 	 RGBR 2 ['YGBR', 'GBYR', 'BGYR']
	(1, 3) 2 	 YBGR 2 ['YBGR', 'GYBR']
	(2, 2) 1 	 BYGR 1 ['BYGR']
    Max node size 8
	
This means that the third guess was RYGB (unlike Knuth's YYGR), and interestingly, the response white white white (meaning three correct in the wrong place) leaves a cluster of 8, which is larger than Knuth's 7—but crucially, it dissolves after the guess YGRV.

At the end of the output you'll see something like:

	Codelist is of length 1296 
	and is ['RRRR', 'RRRO', 'RRRY', 'RRRG', 'RRRB', '....', 'VVVY', 'VVVG', 'VVVB', 'VVVV']
	Guess is  RROY
	Results are
	(2, 0) 105 	 ROGO 4 ['RRRR', 'RRRG', 'RRRB', 'RRRV', 'RRGR', '....', 'VYOY', 'VGOY', 'VBOY', 'VVOY']
	(2, 1) 40 	 RGYO 4 ['RRRO', 'RRYR', 'RRYG', 'RRYB', 'RRYV', '....', 'BRRY', 'BROR', 'VRRY', 'VROR']
	(3, 0) 20 	 ROGB 3 ['RRRY', 'RROR', 'RROO', 'RROG', 'RROB', '....', 'YROY', 'GROY', 'BROY', 'VROY']
	(4, 0) 1 	 None 0 ['RROY']
	(2, 2) 5 	 RRRO 3 ['RRYO', 'RORY', 'RYOR', 'ORRY', 'YROR']
	(1, 2) 84 	 ROYO 4 ['RORR', 'RORO', 'RORG', 'RORB', 'RORV', '....', 'VRYR', 'VRYO', 'VORY', 'VYOR']
	(1, 3) 4 	 ROYR 2 ['ROYR', 'RYRO', 'ORYR', 'YRRO']
	(1, 1) 230 	 RRGB 4 ['ROGO', 'ROGG', 'ROGB', 'ROGV', 'ROBO', '....', 'VBRY', 'VBOR', 'VVRY', 'VVOR']
	(1, 0) 182 	 RGOO 4 ['RGGG', 'RGGB', 'RGGV', 'RGBG', 'RGBB', '....', 'VVYY', 'VVGY', 'VVBY', 'VVVY']
	(0, 3) 44 	 OYRO 4 ['OORR', 'OOYR', 'OYRO', 'OYRG', 'OYRB', '....', 'VORR', 'VOYR', 'VYRR', 'VYRO']
	(0, 2) 222 	 OORG 4 ['OORO', 'OORG', 'OORB', 'OORV', 'OOYO', '....', 'VVRR', 'VVRO', 'VVYR', 'VVYO']
	(0, 1) 276 	 RGGB 4 ['OOGO', 'OOGG', 'OOGB', 'OOGV', 'OOBO', '....', 'VVBR', 'VVBO', 'VVVR', 'VVVO']
	(0, 4) 2 	 OYRR 2 ['OYRR', 'YORR']
	(0, 0) 81 	 GGGB 4 ['GGGG', 'GGGB', 'GGGV', 'GGBG', 'GGBB', '....', 'VVBV', 'VVVG', 'VVVB', 'VVVV']
	Max node size 276
	Duration: 914.1972591876984

This shows you how many guesses after the first guess each response could require as follow-up. For most clusters, you need to guess 4 more times. But for example if the response is black black black, only 20 codes are possible, and if you guess red orange green blue, it will only take 2 more guesses after that (so 3 guesses after the first guess, which is what is displayed).

If you look at the code, which is at mastermind.py, you'll notice some talk about 14 and 196. This is because there are 5+4+3+1+1=14 possible responses to a play: that sum is organized by number of black pegs, from 0 to 4, which allows for from 4 to 0 white pegs, respectively—but when there are three correct guesses in the right place, there can't be another correct in the wrong place, so we get 14 possible responses instead of 15. I had previously incorrectly calculated the number of possible responses as 10, even as I stared at lists of 14 possible responses as in the above output, and it's a shame that to be formally complete, I had to change it to 14, as it still gets the answer right when it thinks it's 10 and takes half or a third of the time (depending on the first guess) to finish.

If you decide to type in ROYG as your first guess instead, at the end you'll see

	Codelist is of length 1296 
	and is ['RRRR', 'RRRO', 'RRRY', 'RRRG', 'RRRB', '....', 'VVVY', 'VVVG', 'VVVB', 'VVVV']
	Guess is  ROYG
	Results are
	(1, 0) 108 	 OBVV 4 ['RRRR', 'RRRB', 'RRRV', 'RRBR', 'RRBB', '....', 'VVYV', 'VVGG', 'VVBG', 'VVVG']
	(1, 1) 252 	 RRYB 4 ['RRRO', 'RRRY', 'RROR', 'RROO', 'RROB', '....', 'VVRG', 'VVOG', 'VVYR', 'VVYO']
	(2, 0) 96 	 RROO 4 ['RRRG', 'RRYR', 'RRYY', 'RRYB', 'RRYV', '....', 'VYYG', 'VGYG', 'VBYG', 'VVYG']
	(1, 2) 132 	 RRGB 4 ['RROY', 'RRGO', 'RRGY', 'RYRO', 'RYOR', '....', 'VYRG', 'VYOG', 'VGYR', 'VGYO']
	(2, 1) 48 	 RROO 4 ['RROG', 'RRYO', 'RORY', 'ROOY', 'ROGR', '....', 'BOYR', 'VRYG', 'VORG', 'VOYR']
	(3, 0) 20 	 RRBV 3 ['RRYG', 'RORG', 'ROOG', 'ROYR', 'ROYO', '....', 'YOYG', 'GOYG', 'BOYG', 'VOYG']
	(4, 0) 1 	 None 0 ['ROYG']
	(2, 2) 6 	 RRRO 3 ['ROGY', 'RYOG', 'RGYO', 'ORYG', 'YORG', 'GOYR']
	(1, 3) 8 	 RRRO 3 ['RYGO', 'RGOY', 'OYRG', 'OGYR', 'YROG', 'YOGR', 'GRYO', 'GORY']
	(0, 2) 312 	 OBGB 4 ['ORRR', 'ORRO', 'ORRB', 'ORRV', 'OROR', '....', 'VVOY', 'VVGR', 'VVGO', 'VVGY']
	(0, 3) 136 	 OYBY 4 ['ORRY', 'OROY', 'ORGR', 'ORGO', 'ORGB', '....', 'VGRO', 'VGRY', 'VGOR', 'VGOY']
	(0, 4) 9 	 RRRO 3 ['ORGY', 'OYGR', 'OGRY', 'YRGO', 'YGRO', 'YGOR', 'GROY', 'GYRO', 'GYOR']
	(0, 1) 152 	 RBBV 4 ['OBOO', 'OBOB', 'OBOV', 'OBBO', 'OBBB', '....', 'VVBY', 'VVVR', 'VVVO', 'VVVY']
	(0, 0) 16 	 RRBB 3 ['BBBB', 'BBBV', 'BBVB', 'BBVV', 'BVBB', '....', 'VVBB', 'VVBV', 'VVVB', 'VVVV']
	Max node size 312
	Duration: 874.2224190235138

This verifies that Don Knuth's hunch that ROYG wouldn't finish up in four additional guesses was wrong.

## OK, but you titled the first section "General Mastermind" and then went on to talk about just the board game. What's the "General" part? ##

Hold on, I was just getting to that. The code for that is at mastermind_general_2.py; it is not recommended to look at the other one, which is an unfinished version.

When you run it, it'll probably try to get you to answer two questions:

	Number of colors?
	Length of codes?

By making these two things variables instead of constants, the program can now try to determine the worst-case scenario for any board game like Mastermind, meaning having whatever number of colors and whatever code length. But to make it really viable that it would wrap up in a reasonable time for somewhat larger codelists, I had to add a few speed-ups; for example, it makes ten random guesses, chooses the minimum over them of the maximum response cluster size, sees if it can finish up in its allotted number of guesses from there, and then if it can't, it goes back and looks at all guesses. I also used symmetry to reduce the total number of guesses it would have to check on the second guess.

If you choose 4 and 6 (as opposed to 6 and 4, which was the original board game), it will pause and wait for you to press enter a few times at the beginning as it generates the codelist etc., and then if you do press enter a few times, you'll see a few lines followed by:

	Attempting situation with max hi 550 critically.
	Codelist is of length 4096 and is ['AAAAAA', 'AAAAAB', 'AAAAAC', 'AAAAAD', 'AAAABA', '......', 'DDDDDA', 'DDDDDB', 'DDDDDC', 'DDDDDD']
	Guess is AAABBC and goal is to finish in at most 3 more guesses
	Respon	#Possib	 Next	 Lo	 Hi	 Chl Possibilities
	(3, 0)  137 	 None	 3 	 16  Yes ['AAAAAA', 'AAAAAD', 'AAAADA', 'AAAADD', 'AAADAA', '......', 'DDADBC', 'DDBBBC', 'DDCBBC', 'DDDBBC']
	(3, 1)  236 	 None	 3 	 236 No  ['AAAAAB', 'AAAACA', 'AAAACD', 'AAAADB', 'AAACAA', '......', 'DCABBD', 'DDAABC', 'DDABAC', 'DDABBA']
	(4, 0)  80 	  None	 3 	 13  Yes ['AAAAAC', 'AAAABA', 'AAAABD', 'AAAACC', 'AAAADC', '......', 'DADBBC', 'DBABBC', 'DCABBC', 'DDABBC']
	(4, 1)  44 	  None	 3 	 8 	 Yes ['AAAABB', 'AAABAB', 'AAABCA', 'AAABCD', 'AAABDB', '......', 'CAABBD', 'DAAABC', 'DAABAC', 'DAABBA']
	(5, 0)  18 	  None	 2 	 4 	 Yes ['AAAABC', 'AAABAC', 'AAABBA', 'AAABBB', 'AAABBD', '......', 'ADABBC', 'BAABBC', 'CAABBC', 'DAABBC']
	(3, 2)  155 	 None	 3 	 23  Yes ['AAAACB', 'AAACAB', 'AAACCB', 'AAACDB', 'AAADCB', '......', 'DACBBA', 'DBAABC', 'DBABAC', 'DCABBA']
	(6, 0)  1 	  AAABBC	 0 	 0 	 Don ['AAABBC']
	(4, 2)  11 	  None	 2 	 5 	 Yes ['AAABCB', 'AAACBB', 'AABABC', 'AABBAC', 'AACBBA', '......', 'ACABBA', 'BAAABC', 'BAABAC', 'CAABBA']
	(2, 2)  507 	 None	 3 	 507 No  ['AABAAA', 'AABAAD', 'AABADA', 'AABADD', 'AABCCD', '......', 'DDACBB', 'DDBABC', 'DDBBAC', 'DDCBBA']
	(2, 3)  204 	 None	 3 	 204 No  ['AABAAB', 'AABACA', 'AABACD', 'AABADB', 'AABCAA', '......', 'DCAABA', 'DCAABB', 'DCABAA', 'DCABAB']
	(2, 4)  21 	  None	 2 	 7 	 Yes ['AABACB', 'AABCAB', 'ABAACB', 'ABACAB', 'ABBAAC', '......', 'CABABA', 'CABBAA', 'CBAABA', 'CBABAA']
	(3, 3)  12 	  None	 2 	 6 	 Yes ['AABBCA', 'AABCBA', 'AACABB', 'AACBAB', 'ABABCA', '......', 'BAABCA', 'BAACBA', 'CAAABB', 'CAABAB']
	(2, 1)  378 	 None	 3 	 378 No  ['AABDDD', 'AACCCD', 'AACCDD', 'AACDCD', 'AACDDD', '......', 'DDCBBD', 'DDDABC', 'DDDBAC', 'DDDBBA']
	(2, 0)  105 	 None	 3 	 12  Yes ['AADDDD', 'ACCCCC', 'ACCCDC', 'ACCDCC', 'ACCDDC', '......', 'DDDBCC', 'DDDBDC', 'DDDCBC', 'DDDDBC']
	(1, 4)  166 	 None	 3 	 28  Yes ['ABBAAA', 'ABBAAB', 'ABBAAD', 'ABBACB', 'ABBACD', '......', 'DBCBAA', 'DCAAAB', 'DCBABA', 'DCBBAA']
	(1, 5)  12 	  BABCAA	 2 	 3 	 Don ['ABBACA', 'ABBCAA', 'ABCAAB', 'ACBAAB', 'BABACA', '......', 'BBACAA', 'BCAAAB', 'CABAAB', 'CBAAAB']
	(1, 3)  486 	 None	 3 	 486 No  ['ABBADB', 'ABBADD', 'ABBCCB', 'ABBCCD', 'ABBCDB', '......', 'DDCABA', 'DDCABB', 'DDCBAA', 'DDCBAB']
	(1, 2)  550 	 None	 3 	 550 No  ['ABBDDB', 'ABBDDD', 'ABCCCD', 'ABCCDD', 'ABCDCD', '......', 'DDDBCA', 'DDDBCB', 'DDDCBA', 'DDDCBB']
	(1, 1)  207 	 None	 3 	 21  Yes ['ABDDDD', 'ACCCCD', 'ACCCDD', 'ACCDCD', 'ACCDDD', '......', 'DDDCBD', 'DDDDAC', 'DDDDBA', 'DDDDBB']
	(1, 0)  37 	  None	 3 	 7 	 Yes ['ADDDDD', 'CCCCCC', 'CCCCDC', 'CCCDCC', 'CCCDDC', '......', 'DDDCDC', 'DDDDBD', 'DDDDCC', 'DDDDDC']
	(0, 5)  48 	  None	 3 	 9 	 Yes ['BBBAAA', 'BBBACA', 'BBBCAA', 'BBCAAB', 'BBCAAD', '......', 'DBCAAA', 'DBCAAB', 'DCBAAA', 'DCBAAB']
	(0, 4)  193 	 None	 3 	 24  Yes ['BBBAAB', 'BBBAAD', 'BBBACB', 'BBBACD', 'BBBADA', '......', 'DDBCAA', 'DDBCAB', 'DDCAAA', 'DDCAAB']
	(0, 3)  284 	 None	 3 	 284 No  ['BBBADB', 'BBBADD', 'BBBCCB', 'BBBCCD', 'BBBCDB', '......', 'DDDACA', 'DDDACB', 'DDDCAA', 'DDDCAB']
	(0, 2)  162 	 None	 3 	 18  Yes ['BBBDDB', 'BBBDDD', 'BBDDDB', 'BBDDDD', 'BCCCCD', '......', 'DDDDAA', 'DDDDAB', 'DDDDCA', 'DDDDCB']
	(0, 6)  3 	  BBCAAA	 2 	 3 	 Don ['BBCAAA', 'BCBAAA', 'CBBAAA']
	(0, 1)  38 	 	 None	 3 	 7 	 Yes ['BDDDDD', 'CCCCCD', 'CCCCDD', 'CCCDCD', 'CCCDDD', '......', 'DDDDAD', 'DDDDCD', 'DDDDDA', 'DDDDDB']
	(0, 0)  1 	  DDDDDD	 1 	 1 	 Don ['DDDDDD']
	Max node size 550
	tally1: 0
	tally2: 3296
	len(retlist) 800

This tells us a few things. One is that it wasn't able to round out the game in 4 (yes, 4) total guesses by making random second guesses, so it has to try the first guess AAABBC "critically," meaning looking at all the possible second guesses. Since only a paltry four out of the 27 possible responses have next guesses attached to them, that means that it's going to have to use the full codelist for the other 23 cases. In some of those cases, the "Hi" bound on the number of guesses to follow up is still the number of possibilities, whereas in others, it has managed to do some work to reduce the Hi by quite a bit. The "tally1" and "tally2" at the end of the output show how many possible second guesses are being skipped over due to symmetry, and so then the "len(retlist)" is how many end up actually needing to be checked (800 out of 4096, so about a fifth).

After some minutes, you will likely see:

	Increasing the goal by one move.
	Press enter to proceed.

(You can take that second line out if you need to go somewhere.) This means that the program found that it was impossible to be sure to beat this "inverted" Mastermind in 4 moves, so it's going to try to beat it in 5. I've run it overnight and it hasn't finished; by some estimates, it could take ten thousand hours to figure this out.

The table below shows the total number of guesses in the worst-case scenario for (n,k)-Mastermind, where n is the number of colors and k is the length of the code, as determined by the program.

	n\k	1	2	3	4	5	6
	1	1	1	1	1	1	1
	2	2	3	3	4	4	5
	3	3	3	4	4	4
	4	4	4	4	4	5
	5	5	4	5	5
	6	6	5	5	5
	7	7	5
	8	8	6
	9	9	6
	10	10	7

## OK, I'm done reading. What should I do next? ##

Well I'm no expert on that, but I suggest taking a look at my repository [Turing](https://github.com/danbriggs/Turing).