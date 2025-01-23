# blackjack/cards.py

import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


    def __repr__(self):
        return f"{self.rank}{self.suit}"
    
    def value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11           # We'll treat Aces as 1 here and handle 11 logic elsewhere 
        else:
            return int(self.rank)

class Deck:
    ranks = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
    suits = ["♠", "♥", "♦", "♣"]

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

class Shoe:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.cards = []
        self._build_shoe()

    def _build_shoe(self):
        self.cards = []
        for _ in range(self.num_decks):
            d = Deck()
            d.shuffle()
            self.cards.extend(d.cards)
        random.shuffle(self.cards)

    def deal_card(self):
        if not self.cards:
            self._build_shoe()            # If shoe is empty, rebuild it
        return self.cards.pop()

    def cards_remaining(self):
        return len(self.cards)

    def decks_remaining(self):
        return len(self.cards) / 52