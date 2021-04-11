from cardodds import deck

hands = (
    ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),  # Straight flush
    ((0, 0), (0, 1), (0, 2), (0, 3), (1, 3)),  # Four aces
    ((2, 1), (3, 1), (3, 2), (2, 3), (2, 0)),  # Full house
    ((3, 1), (5, 1), (7, 1), (9, 1), (11, 1)),  # Flush
    ((3, 0), (4, 1), (5, 2), (6, 2), (7, 3)),  # Straight
    ((0, 0), (1, 1), (2, 2), (2, 3), (2, 0)),  # Three of a kind
    ((0, 3), (9, 1), (8, 0), (9, 3), (8, 1)),  # Two pair
    ((12, 1), (4, 2), (9, 1), (2, 1), (4, 3)),  # Pair
    ((11, 0), (2, 1), (5, 3), (8, 0), (1, 1)),  # No hand
)


def test_cards():
    assert len(set(deck(4, 2).cards)) == 8
    assert len(set(deck(13, 4).cards)) == 52
    assert len(set(deck(20, 6).cards)) == 120


def test_flush():
    d = deck(13, 4)
    assert d._is_flush(hands[0]) == True
    assert d._is_flush(hands[1]) == False
    assert d._is_flush(hands[2]) == False
    assert d._is_flush(hands[3]) == True
    assert d._is_flush(hands[4]) == False
    assert d._is_flush(hands[5]) == False
    assert d._is_flush(((0, 0),)) == True


def test_straight():
    d = deck(13, 4)
    d._generate_straight_sets(5)
    assert deck._is_straight(d, hands[0]) == True
    assert deck._is_straight(d, hands[1]) == False
    assert deck._is_straight(d, hands[2]) == False
    assert deck._is_straight(d, hands[4]) == True
    assert deck._is_straight(d, ((0, 0), (1, 0), (2, 0),)) == False  # short hand


def test_sets():
    assert deck._count_sets("foo", ((0, 0), (0, 2))) == [2]
    assert deck._count_sets("foo", hands[0]) == []
    assert deck._count_sets("foo", hands[1]) == [4]
    assert deck._count_sets("foo", hands[2]) == [2, 3]
    assert deck._count_sets("foo", hands[3]) == []
    assert deck._count_sets("foo", hands[5]) == [3]
    assert deck._count_sets("foo", hands[6]) == [2, 2]
    assert deck._count_sets("foo", hands[7]) == [2]
    assert deck._count_sets("foo", hands[8]) == []


def test_straight_generation():
    d = deck(13, 4)
    d._generate_straight_sets(5)
    assert {0, 1, 2, 3, 4} in d.hand_sets["full_straights"]
    assert {1, 2, 3, 4, 5} in d.hand_sets["full_straights"]
    assert {5, 6, 7, 8, 9} in d.hand_sets["full_straights"]
    assert {9, 10, 11, 12, 0} in d.hand_sets["full_straights"]
    assert {0, 1, 2, 3, 5} not in d.hand_sets["full_straights"]

    assert {0, 1, 3, 4} in d.hand_sets["straight_minus_1"]
    assert {1, 2, 3, 5} in d.hand_sets["straight_minus_1"]
    assert {3, 5, 9, 12} not in d.hand_sets["straight_minus_1"]

    d = deck(13, 4, aces_low_straight=False)
    d._generate_straight_sets(5)
    # assert {0, 1, 2, 3, 4} not in d.hand_sets["full_straights"]
    # assert {1, 2, 3, 4, 5} in d.hand_sets["full_straights"]
    # assert {5, 6, 7, 8, 9} in d.hand_sets["full_straights"]
    # assert {9, 10, 11, 12, 0} in d.hand_sets["full_straights"]
    # assert {0, 1, 2, 3, 5} not in d.hand_sets["full_straights"]
    # assert {0, 1, 7, 3, 4} not in d.hand_sets["straight_minus_1"]
    # assert {8, 1, 2, 3, 6} in d.hand_sets["straight_minus_1"]
    # assert {9, 8, 5, 3, 6} in d.hand_sets["straight_minus_1"]
    # assert {0, 12, 10, 11, 6} in d.hand_sets["straight_minus_1"]
    # assert {1, 3, 5, 7, 9} not in d.hand_sets["straight_minus_1"]

    d = deck(13, 4, aces_high_straight=False)
    d._generate_straight_sets(5)
    # assert {0, 1, 2, 3, 4} in d.hand_sets["full_straights"]
    # assert {1, 2, 3, 4, 5} in d.hand_sets["full_straights"]
    # assert {5, 6, 7, 8, 9} in d.hand_sets["full_straights"]
    # assert {9, 10, 11, 12, 0} not in d.hand_sets["full_straights"]
    # assert {0, 1, 2, 3, 5} not in d.hand_sets["full_straights"]
    # assert {0, 1, 7, 3, 4} in d.hand_sets["straight_minus_1"]
    # assert {8, 1, 2, 3, 6} in d.hand_sets["straight_minus_1"]
    # assert {9, 8, 5, 3, 6} in d.hand_sets["straight_minus_1"]
    # assert {0, 12, 10, 11, 6} not in d.hand_sets["straight_minus_1"]
    # assert {1, 3, 5, 7, 9} not in d.hand_sets["straight_minus_1"]

    d = deck(13, 4, aces_low_straight=False, aces_high_straight=False)
    d._generate_straight_sets(5)
    # assert {0, 1, 2, 3, 4} not in d.hand_sets["full_straights"]
    # assert {1, 2, 3, 4, 5} in d.hand_sets["full_straights"]
    # assert {5, 6, 7, 8, 9} in d.hand_sets["full_straights"]
    # assert {9, 10, 11, 12, 0} not in d.hand_sets["full_straights"]
    # assert {0, 1, 2, 3, 5} not in d.hand_sets["full_straights"]
    # assert {0, 1, 7, 3, 4} not in d.hand_sets["straight_minus_1"]
    # assert {8, 1, 2, 3, 6} in d.hand_sets["straight_minus_1"]
    # assert {9, 8, 5, 3, 6} in d.hand_sets["straight_minus_1"]
    # assert {0, 12, 10, 11, 6} not in d.hand_sets["straight_minus_1"]
    # assert {1, 3, 5, 7, 9} not in d.hand_sets["straight_minus_1"]
