# blackjack/simulation.py

import random
from .cards import Shoe
from .rules import BlackjackRules
from .strategy import BasicStrategy

class Simulator:
    def __init__(self, strategy_name=None, num_decks=6):
        #FIXME: Add settings.yml pull of rules, num_decks, etc...
        self.rules = BlackjackRules(num_decks, surrender_allowed=True)
        self.strategy = BasicStrategy(bet=15, strategy_name=strategy_name, spread_name="basic")
        self.shoe = Shoe(self.rules.decks)
        self.player_bankroll = 0.0
        self.hands_played = 0

        self.amount_bet = 0



    def play_hand(self):
        player_hands = [
            {
                "cards": [self.shoe.deal_card(), self.shoe.deal_card()],
                "bet": self.strategy.get_bet(self.shoe.decks_remaining()),
                "status": "active"
            }
        ]
        dealer_hand = [self.shoe.deal_card(), self.shoe.deal_card()]

        round_net = 0.0

        for card in player_hands[0]["cards"] + [dealer_hand[0]]:
            self.strategy.update_count(card)
        if self.rules.is_blackjack(player_hands[0]["cards"]):
            if self.rules.is_blackjack(dealer_hand):
                round_net == 0.0
            else:
                self.strategy.update_count(dealer_hand[1])
                round_net = player_hands[0]["bet"] * self.rules.blackjack_payout
            self.amount_bet += player_hands[0]["bet"]
            self.player_bankroll += round_net
            return round_net
        if self.rules.is_blackjack(dealer_hand):
            round_net = -player_hands[0]["bet"]
            self.player_bankroll += round_net
            self.amount_bet += player_hands[0]["bet"]
            return round_net

        player_hands = self.player_turn(player_hands, dealer_hand[0])
        dealer_outcome = self.dealer_turn(dealer_hand)

        print(f"Player: {player_hands}\nDealer: {dealer_hand}")

        for hand in player_hands:
            player_outcome = self.settle_bet(hand, self.rules.hand_value(dealer_hand))
            print(f"Player Outcome: {player_outcome}")
            round_net += player_outcome
            self.amount_bet += hand["bet"]
        print()
        self.strategy.update_count(dealer_hand[1])

        self.player_bankroll += round_net
        return round_net

    def player_turn(self, player_hands, dealer_card):
        """
            - H = Hit
            - S = Stand
            - DH = Double if allowed, otherwise hit
            - DS = Double if allowed, otherwise stand
            - P = Split
            - PH = Split if double after split is allowed, otherwise hit
            - RH = Surrender if allowed, otherwise hit
        """
        i = 0
        while i < len(player_hands):
            hand_info = player_hands[i]
            if hand_info["status"] != "active":
                i += 1
                continue
            while hand_info["status"] == "active":
                action_code = self.strategy.decide_player_action(hand_info["cards"], dealer_card, self.rules, self.shoe.decks_remaining())
                if action_code in ["H", "DH", "PH", "RH"]:
                    did_fallback = False

                    if action_code == "DH":
                        if self._can_double(hand_info["cards"]):
                            self._do_double(hand_info)
                            break
                        else:
                            did_fallback  = True

                    if action_code == "PH" and not did_fallback:
                        if self._can_split(hand_info["cards"]):
                            self._do_split(player_hands, i)
                            break
                        else:
                            did_fallback = True
                    
                    if action_code == "RH" and not did_fallback:
                        if self.rules.surrender_allowed and self._can_surrender(hand_info["cards"]):
                            self._do_surrender(hand_info)
                            break
                        else:
                            did_fallback = True
                    
                    if action_code == "H" or did_fallback:
                        new_card = self.shoe.deal_card()
                        self.strategy.update_count(new_card)
                        hand_info["cards"].append(new_card)
                        if self.rules.hand_value(hand_info["cards"]) > 21:
                            hand_info["status"] = "busted"
                            break
                            
                elif action_code in ["S", "DS"]:
                    if action_code == "DS" and self._can_double(hand_info["cards"]):
                        self._do_double(hand_info)
                        break
                    else:
                        hand_info["status"] = "stood"
                        break
                
                elif action_code == "P":
                    if self._can_split(hand_info["cards"]):
                        self._do_split(player_hands, i)
                        break

                else:
                    print(f"Invalid action code: {action_code}")
                    hand_info["status"] = "stood"
                    break
            i += 1
        return player_hands    
        
    def _can_double(self, hand):
        return len(hand) == 2

    def _can_split(self, hand):
        return len(hand) == 2 and hand[0].rank == hand[1].rank

    def _can_surrender(self, hand):
        return len(hand) == 2

    def _do_double(self, hand_info):
        print("Doubling down")
        hand_info["bet"] *= 2
        new_card = self.shoe.deal_card()
        self.strategy.update_count(new_card)
        hand_info["cards"].append(new_card)
        if self.rules.hand_value(hand_info["cards"]) > 21:
            hand_info["status"] = "busted"
        else:
            hand_info["status"] = "stood"

    def _do_split(self, player_hands, i):
        new_card_for_first = self.shoe.deal_card()
        new_card_for_second = self.shoe.deal_card()

        self.strategy.update_count(new_card_for_first)
        self.strategy.update_count(new_card_for_second)

        card_to_move = player_hands[i]["cards"].pop()

        player_hands[i]["cards"] = [player_hands[i]["cards"][0], new_card_for_first]
        player_hands[i]["status"] = "active"

        second_hand = {
            "cards": [card_to_move, new_card_for_second],
            "bet": player_hands[i]["bet"],
            "status": "active"
        }
        player_hands.insert(i + 1, second_hand)

    def _do_surrender(self, hand_info):
        hand_info["status"] = "surrendered"

    def dealer_turn(self, dealer_hand):
        while self.rules.dealer_should_hit(dealer_hand):
            new_card = self.shoe.deal_card()
            self.strategy.update_count(new_card)
            dealer_hand.append(new_card)
        return dealer_hand

    def settle_bet(self, hand_info, dealer_total):
        status = hand_info["status"]
        player_total = self.rules.hand_value(hand_info["cards"])
        bet = hand_info["bet"]

        if status == "surrendered":
            return -bet / 2
        elif status == "busted":
            return -bet
        else:
            if dealer_total > 21:
                return bet
            elif player_total > dealer_total:
                return bet
            elif player_total < dealer_total:
                return -bet
            else:
                return 0.0

    def run_simulation(self, num_hands=1000000):
        for _ in range(num_hands):
            if self.shoe.decks_remaining() < self.rules.deck_penetration:
                self.shoe = Shoe(self.rules.decks)
                self.strategy.reset_count()
            result = self.play_hand()
            self.player_bankroll += result
            self.hands_played += 1

        return {
            "hands_played": self.hands_played,
            "final_bankroll": self.player_bankroll,
            "amount_bet": self.amount_bet,
            "avg_profit_per_hand": self.player_bankroll / self.hands_played,
            "House Advantage (%)":  (1 - (self.player_bankroll + self.amount_bet) / self.amount_bet) * 100
        }