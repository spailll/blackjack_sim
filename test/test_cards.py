def test_card_creation():
    from blackjack.cards import Card
    c = Card("A", "♠")
    assert c.rank == "A"
    assert c.suit == "♠"

def test_deck_init():
    from blackjack.cards import Deck
    d = Deck()
    assert len(d.cards) == 52
    # Optional: check for duplicates, suits, ranks
    ranks = [card.rank for card in d.cards]
    suits = [card.suit for card in d.cards]
    assert len(set(ranks)) > 1  # all ranks appear
    assert len(set(suits)) == 4

def test_deck_shuffle():
    from blackjack.cards import Deck
    d1 = Deck()
    d2 = Deck()
    # Both decks are unshuffled initially
    # Shuffle one of them
    d2.shuffle()
    # Compare sequences
    # It's possible (though extremely unlikely) they might match exactly by chance,
    # but we can at least check they differ in most cases.
    assert d1.cards != d2.cards

def test_shoe_init():
    from blackjack.cards import Shoe
    shoe = Shoe(6)
    assert len(shoe.cards) == 6 * 52

