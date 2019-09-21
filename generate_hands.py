import argparse
from itertools import combinations
from collections import defaultdict
from tabulate import tabulate

def create_deck(total_ranks, total_suits):
    # Create a deck of cards that enumerates every pair of 
    # ranks and suits
    # output is a list of cards.  
    deck = []
    ranks = range(total_ranks)
    suits = range(total_suits)

    for suit in suits:
        for rank in ranks:
            card = (rank, suit)
            deck.append(card)
    return deck


def is_flush(hand):
    # Given a hand of cards, determine if a flush is held
    # (all cards have same suit)
    # first item of card is rank, second item is suit
    suit = hand[0][1]
    for card in hand[1:]:
        if card[1] != suit:
            return False
    return True


def is_straight(hand, number_ranks):
    # Given a hand of cards, indicate if a straight is held
    # first itme of card is rank, second item is suit
    ranks = sorted([x[0] for x in hand])
    last = ranks[0]
    has_ace = False

    # Rank 0 is an Ace.  Aces can also be rank = number_ranks.
    # Only need to check the first card since list is sorted.
    if ranks[0] == 0:
        has_ace = True

    for card in ranks[1:]:
        last += 1
        if card != last:
            if has_ace:
                # See if straight is present if Ace is treated high rather than low.
                return is_straight([(x, 0) for x in ranks[1:]] + [(number_ranks, 0)], number_ranks)
            return False
    return True


def count_sets(hand):
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
            '[2]': 'one pair',
            '[3]': 'three of a kind',
            '[4]': 'four of a kind',
            '[5]': 'five of a kind',
            '[2, 2]': 'two pair',
            '[2, 3]': 'full house'
            }
    return names.get(set_representation, set_representation)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Calculate hand odds of a card deck')
    parser.add_argument('--ranks', '-r', type=int, default=13, help='Number of different ranks (default: 13)')
    parser.add_argument('--suits', '-s', type=int, default=4, help='Number of different suits (default: 4)')
    parser.add_argument('--hand_size', type=int, default=5, help='Number of cards per hand (default: 5)')
    args = parser.parse_args()

    ranks = args.ranks          # Standard deck has 13 ranks from A - K
    suits = args.suits          # Standard deck has 4 suits
    hand_size = args.hand_size  # Normal poker hand has 5 cards

    deck = create_deck(ranks, suits)
    combos = combinations(deck, hand_size)

    poker_hand_count = defaultdict(int)
    for hand_count, hand in enumerate(combos, start=1):

        flush = 0
        straight = 0

        flush = is_flush(hand)
        straight = is_straight(hand, ranks)
        if (flush and straight):
            poker_hand_count['straight flush'] += 1
        elif flush:
            poker_hand_count['flush'] += 1
        elif straight:
            poker_hand_count['straight'] += 1
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
    table.sort(key=lambda x: x[1])
    print(tabulate(table, headers = headers))
