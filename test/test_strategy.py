def test_basic_strategy_hard_9():
    from blackjack.strategy import BasicStrategy
    from blackjack.cards import Card
    from blackjack.rules import BlackjackRules

    rules = BlackjackRules()
    strategy = BasicStrategy(strategy_path="config/strategy.yaml", bet=1)

    # Hard 9 vs dealer 4 => expect "DH" or "double if allowed, otherwise hit"
    player_hand = [Card("4","♠"), Card("5","♥")]  # total = 9
    dealer_up = Card("4", "♦")
    action = strategy.decide_player_action(player_hand, dealer_up, rules)
    assert action == "DH"

def test_basic_strategy_soft_17_vs_dealer_6():
    from blackjack.strategy import BasicStrategy
    from blackjack.cards import Card
    from blackjack.rules import BlackjackRules

    strategy = BasicStrategy(strategy_path="config/strategy.yaml")
    rules = BlackjackRules()

    # Soft 17 => A+6 => might check your chart for correct code
    # Suppose "DH" or "DS" or something similar
    player_hand = [Card("A","♠"), Card("6","♥")]
    dealer_up = Card("6", "♦")
    action = strategy.decide_player_action(player_hand, dealer_up, rules)
    # Verify matches your strategy chart row
    assert action in ["DH","DS","H"]  # depends on your chart

def test_basic_strategy_pair_8s_vs_dealer_10():
    from blackjack.strategy import BasicStrategy
    from blackjack.cards import Card
    from blackjack.rules import BlackjackRules

    strategy = BasicStrategy("config/strategy.yaml")
    rules = BlackjackRules()

    # 8,8 vs 10 typically is "P" (split)
    player_hand = [Card("8","♠"), Card("8","♥")]
    dealer_up = Card("K","♦")  # treat K as 10
    action = strategy.decide_player_action(player_hand, dealer_up, rules)
    assert action == "P"  # or "PH" if your chart says so
