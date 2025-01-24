# blackjack/strategy.py

import yaml
import math 

class Strategy:
    def __init__(self, hand, dealer_card, rules):
        self.hand = hand
        self.dealer_card = dealer_card
        self.rules = rules

        self.dealer_index_map = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "10": 8, "J": 8, "Q": 8, "K": 8, "A": 9}         

    
    def get_coordinates(self):
        if self._is_pair():
            row_index = self._pair_row_index()
            table_index = 2
        elif self._is_soft():
            row_index = self._soft_row_index()
            table_index = 1
        else:
            row_index = self._hard_row_index()
            table_index = 0
        
        col_index = self._get_col_index()

        return table_index, row_index, col_index

    def _is_pair(self):
        return (len(self.hand) == 2) and (self.hand[0].rank == self.hand[1].rank)

    def _is_soft(self):
        total = self.rules.hand_value(self.hand)
        has_ace = any(card.rank == "A" for card in self.hand)
        return has_ace and self.rules.hand_value(self.hand) < 21

    def _pair_row_index(self):
        rank = self.hand[0].rank
        if rank == '2': return 0
        if rank == '3': return 1
        if rank == '4': return 2
        if rank == '5': return 3
        if rank == '6': return 4
        if rank == '7': return 5
        if rank == '8': return 6
        if rank == '9': return 7
        if rank in ['10', 'J', 'Q', 'K']: return 8
        if rank == 'A': return 9
        return 0

    def _soft_row_index(self):
        total = self.rules.hand_value(self.hand)
        if total >= 19:
            return 6
        row = total - 13
        if row < 0:
            row = 0
        return row

    def _hard_row_index(self):
        total = self.rules.hand_value(self.hand)
        if total < 9:
            return 0
        if total >= 17:
            return 9
        return total - 8

    def _get_col_index(self):
        return self.dealer_index_map[self.dealer_card.rank]

class BasicStrategy:
    def __init__(self, bet=15, strategy_name=None, spread_name=None, insurance_count_threshold=3, counting_system="hi-lo"):
        self.bet = bet
        self.running_count = 0
        self.insurance_count_threshold = insurance_count_threshold
        self.counting_system = counting_system

        self.strategy_name = strategy_name
        self.spread_name = spread_name

        with open ("config/strategy.yaml", "r") as f:
            data = yaml.safe_load(f)

        if self.strategy_name:
            print("Using Strategy: ", strategy_name)
            self._all_charts = data[strategy_name]["counts"]
        else:    
            self._all_charts = data["basic"]["counts"]
        

        if self.spread_name:

            with open("config/spread.yaml", "r") as f:
                data = yaml.safe_load(f)
            self._spread = data[spread_name]["thresholds"]
            print(self._spread)
        else: 
            self._spread = None

# ================COUNTING SYSETMS=================
    def update_count(self, card):
        # Hi-Lo Example (2-6 = +1, 7-9 = 0, 10-Ace = -1)
        rank = card.rank
        if self.counting_system == "hi-lo":
            if rank in ["2", "3", "4", "5", "6"]:
                self.running_count += 1
            elif rank in ["10", "J", "Q", "K", "A"]:
                self.running_count -= 1

        elif self.counting_system == "hi-lo opt I":
            if rank in ["3", "4", "5", "6"]:
                self.running_count += 1
            elif rank in ["10", "J", "Q", "K"]:
                self.running_count -= 1
        
        elif self.counting_system == "hi-lo opt II":
            if rank in ["2", "3", "6", "7"]:
                self.running_count += 1
            elif rank in ["4", "5"]:
                self.running_count += 2
            elif rank in ["10", "J", "Q", "K"]:
                self.running_count -= 2
        
        elif self.counting_system == "k-o":
            if rank in ["2", "3", "4", "5", "6", "7"]:
                self.running_count += 1
            elif rank in ["10", "J", "Q", "K", "A"]:
                self.running_count -= 1

        elif self.counting_system == "mentor":
            if rank in ["2", "7"]:
                self.running_count += 1
            elif rank in ["3", "4", "5", "6"]:
                self.running_count += 2
            elif rank in ["9", "A"]:
                self.running_count -= 1
            elif rank in ["10", "J", "Q", "K"]:
                self.running_count -= 2

        elif self.counting_system == "omega II":
            if rank in ["2", "3", "7"]:
                self.running_count += 1
            elif rank in ["4", "5", "6"]:
                self.running_count += 2
            elif rank == "9":
                self.running_count -= 1
            elif rank in ["10", "J", "Q", "K"]:
                self.running_count -= 2

        elif self.counting_system == "reko":
            if rank in ["2", "3", "4", "5", "6", "7"]:
                self.running_count += 1
            elif rank in ["10", "J", "Q", "K", "A"]:
                self.running_count -= 1

        elif self.counting_system == "reverse point count":
            if rank in ["2", "7"]:
                self.running_count += 1
            elif rank in ["3", "4", "5", "6"]:
                self.running_count += 2
            elif rank in ["10", "J", "Q", "K", "A"]:
                self.running_count -= 2

        elif self.counting_system == "reverse 14 count":
            if rank == "7":
                self.running_count += 1
            elif rank in ["2", "3", "6"]:
                self.running_count += 2
            elif rank == "4":
                self.running_count += 3
            elif rank == "5":
                self.running_count += 4
            elif rank == "9":
                self.running_count -= 2
            elif rank in ["10", "J", "Q", "K"]:
                self.running_count -= 3

        elif self.counting_system == "reverse rapc":
            if rank in ["2", "7"]:
                self.running_count += 2
            elif rank in ["3", "4", "6"]:
                self.running_count += 3
            elif rank == "5":
                self.running_count += 4
            elif rank == "9":
                self.running_count -= 1
            elif rank in  ["10", "J", "Q", "K"]:
                self.running_count -= 3
            elif rank == "A":
                self.running_count -= 4

        elif self.counting_system == "silver fox":
            if rank in ["2", "3", "4", "5", "6", "7"]:
                self.running_count += 1
            elif rank in ["9", "10", "J", "Q", "K", "A"]:
                self.running_count -= 1

        elif self.counting_system == "unbalanced zen 2":
            if rank in ["2", "7"]:
                self.running_count += 1
            elif rank in ["3", "4", "5", "6"]:
                self.running_count += 2
            elif rank == "A":
                self.running_count -= 1
            elif rank in ["10", "J", "Q", "K"]:
                self.running_count -= 2

        elif self.counting_system == "uston apc":
            if rank in ["2", "8"]:
                self.running_count += 1
            elif rank in ["3", "4", "6", "7"]:
                self.running_count += 2
            elif rank == "5":
                self.running_count += 3
            elif rank == "9":
                self.running_count -= 1
            elif rank in ["10", "J", "Q", "K"]:
                self.running_count -= 3

        elif self.counting_system == "uston ss":
            if rank == "7":
                self.running_count += 1
            elif rank in ["2", "3", "4", "6"]:
                self.running_count += 2
            elif rank == "9":
                self.running_count -= 1
            elif rank in ["10", "J", "Q", "K", "A"]:
                self.running_count -= 2

        elif self.counting_system == "wong halves":
            if rank in ["2", "7"]:
                self.running_count += 0.5
            elif rank in ["3", "4", "6"]:
                self.running_count += 1
            elif rank == "5":
                self.running_count += 1.5
            elif rank == "9":
                self.running_count -= 0.5
            elif rank in ["10", "J", "Q", "K", "A"]:
                self.running_count -= 1

        elif self.counting_system == "zen count":
            if rank in ["2", "3", "7"]:
                self.running_count += 1
            elif rank in ["4", "5", "6"]:
                self.running_count += 2
            elif rank == "A":
                self.running_count -= 1
            elif rank in ["10", "J", "Q", "K"]:
                self.running_count -= 2
# =================================================

    def reset_count(self):
        self.running_count = 0

    def get_true_count(self, decks_remaining):
        if decks_remaining < 1:         # Avoid divide by 0
            return self.running_count
        return self.running_count / (decks_remaining)

    # FIXME: Change to add spread.yaml and pull values from there
    # Rework all logic in here
    def get_bet(self, decks_remaining):
        tc = math.floor(self.get_true_count(decks_remaining))
        chosen_bet = 1 # Default
        if not self._spread:
            return self.bet
        for x in self._spread:
            threshold = x["count"] 
            if tc >= threshold:
                chosen_bet = x["bet"]
        return chosen_bet * self.bet

    def decide_player_action(self, hand, dealer_card, rules, decks_remaining):
        # TC_index Logic Goes here in other versions
        if self.strategy_name != "basic":
            tc = math.floor(self.get_true_count(decks_remaining))
            tc = min(max(tc, -6), 6)
            chart = self._all_charts[tc + 6]
        else:
            chart = self._all_charts[0]

        strategy = Strategy(hand, dealer_card, rules)
        table_index, row_index, col_index = strategy.get_coordinates()

        return chart[table_index][row_index][col_index]
