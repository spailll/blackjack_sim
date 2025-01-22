# blackjack/rules.py

class BlackjackRules:
    def __init__(self, decks, dealer_hits_soft_17=True, blackjack_payout=1.5, surrender_allowed=False):
        self.decks = decks
        self.dealer_hits_soft_17 = dealer_hits_soft_17
        self.blackjack_payout = blackjack_payout
        self.surrender_allowed = surrender_allowed

    def is_blackjack(self, hand):
        return len(hand) == 2 and hand.value() == 21

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