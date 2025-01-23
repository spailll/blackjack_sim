# blackjack/rules.py

class BlackjackRules:
    def __init__(self, decks, dealer_hits_soft_17=False, blackjack_payout=1.5, surrender_allowed=False, double_after_split_allowed=True, deck_penetration=0.5):
        self.decks = decks
        self.dealer_hits_soft_17 = dealer_hits_soft_17
        self.blackjack_payout = blackjack_payout
        self.surrender_allowed = surrender_allowed
        self.double_after_split_allowed = double_after_split_allowed
        self.deck_penetration = deck_penetration

    def is_blackjack(self, hand):
        return len(hand) == 2 and self.hand_value(hand) == 21

    def hand_value(self, hand):
        total = sum(card.value() for card in hand)
        aces = sum(card.rank == "A" for card in hand) # Count Aces in hand
        while aces > 0 and total + 10 <= 21:
            total += 10
            aces -= 1
        return total

    def dealer_should_hit(self, hand):
        value = self.hand_value(hand)
        if value < 17:
            return True
        if value == 17 and self.dealer_hits_soft_17:
            if any(card.rank == "A" for card in hand):
                return True
        return False