from cardodds import deck

hands = (
         ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)), # Straight flush
         ((0, 0), (0, 1), (0, 2), (0, 3), (1, 3)), # Four aces
         ((2, 1), (3, 1), (3, 2), (2, 3), (2, 0)), # Full house
         ((3, 1), (5, 1), (7, 1), (9, 1), (11, 1)), # Flush
         ((3, 0), (4, 1), (5, 2), (6, 2), (7, 3)), # Straight
         ((0, 0), (1, 1), (2, 2), (2, 3), (2, 0)), # Three of a kind
         ((0, 3), (9, 1), (8, 0), (9, 3), (8, 1)), # Two pair
         ((12, 1), (4, 2), (9, 1), (2, 1), (4, 3)), # Pair
         ((11, 0), (2, 1), (5, 3), (8, 0), (1, 1)), # No hand
         )

def test_basic_deck():
    assert len(set(deck(13, 4).deck))==52
    assert len(set(deck(2, 2).deck))==4
    assert len(set(deck(20, 6).deck))==120


def test_flush():
    assert deck._is_flush('foo', ((0, 0),)) == True
    assert deck._is_flush('foo', hands[0]) == True
    assert deck._is_flush('foo', hands[1]) == False


