# cardodds
Calculated odds of drawing particular hands from a deck of cards

While you could calculate it faster using known equations, this code generates a deck of cards given the number of ranks and suits, and then generates every possible hand.  It then counds each type of hand and displays the count and frequency.

Defaults to a standard deck

```
$ python3 generate_hands.py
hand type          count    1 in x odds
---------------  -------  -------------
straight flush        40          64974
four of a kind       624           4165
full house          3744            694
flush               5108            508
straight           10200            254
three of a kind    54912             47
two pair          123552             21
one pair         1098240              2
all hands        2598960              1
```

```
$ python3 generate_hands.py -r 10 --hand 2
hand type         count    1 in x odds
--------------  -------  -------------
straight flush       40             19
one pair             60             13
straight            120              6
flush               140              5
all hands           780              1
```
