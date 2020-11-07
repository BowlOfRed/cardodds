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
    assert deck._is_flush("foo", ((0, 0),)) == True
    assert deck._is_flush("foo", hands[0]) == True
    assert deck._is_flush("foo", hands[1]) == False


def test_straight():
    d = deck(13, 4)
    assert deck._is_straight(d, ((0, 1, 2),)) == True
    assert deck._is_straight(d, hands[0]) == True
    assert deck._is_straight(d, hands[1]) == False
    assert deck._is_straight(d, hands[2]) == False
    assert deck._is_straight(d, hands[4]) == True


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
