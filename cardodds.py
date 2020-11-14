import argparse
from operator import itemgetter
from itertools import combinations, product
from collections import defaultdict, Counter
import time

# from tabulate import tabulate


class deck:
    def __init__(
        self,
        total_ranks=13,
        total_suits=4,
        aces_low_straight=True,
        aces_high_straight=True,
    ):
        self.ranks = total_ranks
        self.suits = total_suits
        self.aces_low_straight = aces_low_straight
        self.aces_high_straight = aces_high_straight

    @property
    def cards(self):
        return product(range(self.ranks), range(self.suits))

    def calc_odds(self, hand_size=5, drawing_hands=False):
        self._generate_straight_sets(hand_size)
        start = time.perf_counter()
        combos = combinations(self.cards, hand_size)

        poker_odds = Counter()
        poker_odds.hand_size = hand_size
        for nth_hand, hand in enumerate(combos, start=1):

            flush = self._is_flush(hand)
            straight = self._is_straight(hand)
            if flush and straight:
                poker_odds["straight flush"] += 1
            elif flush:
                poker_odds["flush"] += 1
            elif straight:
                poker_odds["straight"] += 1
            set_info = self._count_sets(hand)
            if set_info:
                poker_odds[str(set_info)] += 1

        poker_odds["all hands"] = nth_hand
        self.odds = poker_odds
        end = time.perf_counter()
        self.elapsed = end - start

    def _is_flush(self, hand):
        # Given a hand of cards, determine if a flush is held
        # (all cards have same suit)
        # first item of card is rank, second item is suit
        suit = hand[0][1]
        for card in hand[1:]:
            if card[1] != suit:
                return False
        return True

    def _is_straight(self, hand):
        # Given a hand of cards, determine if a flush is held
        # (all cards have same suit)
        # first item of card is rank, second item is suit
        h = hand
        return {x[0] for x in hand} in self.hand_sets["full_straights"]

    def _count_sets(self, hand):
        # Given a hand of cards, indicate the number of "sets" of each rank
        # Output count of each set with more than 1 member
        ranks = sorted([x[0] for x in hand])
        large_sets = []
        set_size = 0
        last_rank = -1
        for rank in ranks:
            if rank != last_rank:
                if set_size > 1:
                    large_sets.append(set_size)
                set_size = 1
                last_rank = rank
            else:
                set_size += 1
        if set_size > 1:
            large_sets.append(set_size)
        return sorted(large_sets)

    def _generate_straight_sets(self, hand_size):
        # Generate sets that can be use for comparisons
        # of straights and optionally near-straights

        # simple straights
        full_straights = set()
        starting_card = 0 if self.aces_low_straight else 1
        for low_card in range(starting_card, self.ranks - hand_size + 1):
            full_straights.add(frozenset(range(low_card, low_card + hand_size)))
        if self.aces_high_straight:
            high_straight = set(range(low_card + 1, low_card + hand_size))
            high_straight.add(0)
            full_straights.add(frozenset(high_straight))
        self.hand_sets = {}
        self.hand_sets["full_straights"] = full_straights

        # drawing straights
        straight_minus_1 = set()
        for hand in full_straights:
            c = combinations(hand, len(hand) - 1)
            straight_minus_1 |= set(frozenset(x) for x in c)
        self.hand_sets["straight_minus_1"] = straight_minus_1

        straight_minus_2 = set()
        for hand in straight_minus_1:
            straight_minus_2 |= set(combinations(hand, len(hand) - 1))
        self.hand_sets["straight_minus_2"] = straight_minus_2


def hand_name(set_representation):
    # Given a string representation of a count of sets,
    # return a common name for that set distribution.
    # Example [2] represents a single pair, while
    # [2, 3] represents a full house.  The count of sets
    # is always to be sorted.

    # The current map has names for all sets possible in
    # a five-card hand (including some that are not possible
    # with a standard deck).  If simulating hands larger than 5,
    # you may need to add new names (such as three pair).

    names = {
        "[2]": "one pair",
        "[3]": "three of a kind",
        "[4]": "four of a kind",
        "[5]": "five of a kind",
        "[2, 2]": "two pair",
        "[2, 3]": "full house",
    }
    return names.get(set_representation, set_representation)


if __name__ == "__main__":

    def check_more_than_1(value):
        try:
            ivalue = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("Argument must be integer larger than 1")
        if ivalue <= 1:
            raise argparse.ArgumentTypeError("Argument must be integer larger than 1")
        return ivalue

    parser = argparse.ArgumentParser(description="Calculate hand odds of a card deck")
    parser.add_argument(
        "--ranks",
        "-r",
        default=13,
        type=check_more_than_1,
        help="Number of different ranks (default: 13)",
    )
    parser.add_argument(
        "--suits",
        "-s",
        default=4,
        type=check_more_than_1,
        help="Number of different suits (default: 4)",
    )
    parser.add_argument(
        "--hand_size",
        default=5,
        type=check_more_than_1,
        help="Number of cards per hand (default: 5)",
    )
    args = parser.parse_args()

    ranks = args.ranks  # Standard deck has 13 ranks from A - K
    suits = args.suits  # Standard deck has 4 suits
    hand_size = args.hand_size  # Normal poker hand has 5 cards

    deck = create_deck(ranks, suits)
    combos = combinations(deck, hand_size)

    poker_hand_count = defaultdict(int)
    for hand_count, hand in enumerate(combos, start=1):

        flush = 0
        straight = 0

        flush = is_flush(hand)
        straight = is_straight(hand, ranks)
        if flush and straight:
            poker_hand_count["straight flush"] += 1
        elif flush:
            poker_hand_count["flush"] += 1
        elif straight:
            poker_hand_count["straight"] += 1
        set_info = count_sets(hand)
        if len(set_info) == 0:
            continue
        poker_hand_count[str(set_info)] += 1

    table = []
    headers = ["hand type", "count", "1 in x odds"]

    for hand_type, count in poker_hand_count.items():
        if count:
            odds = hand_count // count
        else:
            odds = "-"
        hand_type = hand_name(hand_type)
        table.append([hand_type, count, odds])

    table.append(["all hands", hand_count, 1])
    table.sort(key=itemgetter(1))
    print(tabulate(table, headers=headers))
