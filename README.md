## Generalized Mastermind ##

In 1977, Don Knuth showed that Mastermind takes 5 guesses.

I didn't know that, so in the spring of 2003 I wrote a Lisp/Scheme program that attempted to determine this.

Or so I thought. What the program really did was just run and run, and I'm not sure whether it was because it would really just take that long or I had failed to properly end the recursion.

It turns out that Python is a much better language for this sort of thing (although LISP is of course still beautiful), so I got back at it this week and after a couple days I got 5, and then I looked it up, only to find out the above.

One corollary, though, was that I was able to edit a parenthetical remark in step 2 of the explication of his algorithm in the "Worst case" sub-subsection of the wikipedia page about the game: the commentator, failing to read their Knuth carefully, seemed to have been under the impression that red red green blue *cannot* win in five tries, whereas Knuth had only stated that *his* algorithm is not guaranteed to round out play in five tries.

