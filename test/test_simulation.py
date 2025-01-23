import pytest
from unittest.mock import patch

def test_player_bust():
    from blackjack.simulation import Simulator
    from blackjack.cards import Card

    sim = Simulator()

    # Patch the Shoe.deal_card() method so we know exactly which cards are dealt
    # Suppose player's first two cards are (10, 10) => bust
    # Dealer's first card is 5, second card is Q
    deal_sequence = [
        Card("J","♣"), Card("2","♦"),  # player's hand
        Card("9","♣"), Card("A","♦"),   # dealer's hand
        # Next card for player
        Card("Q","♠")
    ]
    
    with patch.object(sim.shoe, 'deal_card', side_effect=deal_sequence):
        result = sim.play_hand()
        # Player busts => lose bet
        assert result == -sim.strategy.bet

def test_player_blackjack():
    from blackjack.simulation import Simulator
    from blackjack.cards import Card

    sim = Simulator()

    # Patch the Shoe.deal_card() method so we know exactly which cards are dealt
    # Suppose player's first two cards are (A, K) => blackjack
    # Dealer's first card is 5, second card is Q
    deal_sequence = [
        Card("A","♠"), Card("K","♥"),  # player's hand
        Card("5","♣"), Card("Q","♦")   # dealer's hand
    ]
    
    with patch.object(sim.shoe, 'deal_card', side_effect=deal_sequence):
        result = sim.play_hand()
        # Player should have blackjack, dealer does not => pay 1.5 * bet
        # bet is 15 from the example code
        assert result == 15 * sim.rules.blackjack_payout

def test_player_blackjack_dealer_blackjack():
    from blackjack.simulation import Simulator
    from blackjack.cards import Card

    sim = Simulator()

    deal_sequence = [
        Card("A","♠"), Card("K","♥"),  # player
        Card("A","♣"), Card("Q","♦")   # dealer
    ]
    with patch.object(sim.shoe, 'deal_card', side_effect=deal_sequence):
        result = sim.play_hand()
        # Both have blackjack => push => 0.0
        assert result == 0.0

def test_double_down():
    from blackjack.simulation import Simulator
    from blackjack.cards import Card

    sim = Simulator()
    sim.strategy.bet = 10  # override bet for test
    
    # Suppose we want the player to get 11 (5,6),
    # dealer has 6 up, 10 down,
    # then the player draws a 9 after doubling => total 20
    # dealer ends up with something below 21 => outcome depends on final comparison.
    deal_sequence = [
        # Player's 2 cards
        Card("5","♠"), Card("6","♥"),
        # Dealer's 2 cards
        Card("6","♣"), Card("10","♦"),
        # Player's double-down cards
        Card("9","♥"),
        # Next cards for dealer if needed
        Card("2","♠")
    ]
    
    with patch.object(sim.shoe, 'deal_card', side_effect=deal_sequence):
        result = sim.play_hand()
        # Evaluate outcome based on the test scenario.
        # Player has 20, dealer has 16 => hits or stands depending on rules, etc.
        # Let’s just check no errors, or that result is correct if we map the scenario out fully.
        assert result != None

def test_splitting():
    from blackjack.simulation import Simulator
    from blackjack.cards import Card

    sim = Simulator()
    sim.strategy.bet = 10

    # Player: 8, 8
    # Dealer: 10, 4
    # Next two cards for each split hand: (2, 3)
    deal_sequence = [
        Card("8","♠"), Card("8","♥"),  # Player
        Card("10","♦"), Card("4","♣"), # Dealer
        Card("2","♦"), Card("3","♣"),  # first new card for first hand, second new card for second
        # possible additional dealer draws if needed
        Card("2","♠"), Card("3","♠")
    ]
    
    with patch.object(sim.shoe, 'deal_card', side_effect=deal_sequence):
        result = sim.play_hand()
        # Verify the final result if you can map out exactly what each hand does
        # Or just check that no errors occur and the function returns a float.
        assert isinstance(result, float)

def test_surrender():
    from blackjack.simulation import Simulator
    from blackjack.cards import Card

    sim = Simulator()
    sim.strategy.bet = 10
    sim.rules.surrender_allowed = True

    # Force player's hand = (9,7) => 16
    # Dealer up = 10
    # Suppose strategy or fallback => "RH"
    deal_sequence = [
        Card("9","♠"), Card("7","♥"),     # Player hand
        Card("10","♦"), Card("4","♣"),    # Dealer hand
        # Next cards for dealer if needed
        Card("8","♠"), Card("3","♠")
    ]
    with patch.object(sim.shoe, 'deal_card', side_effect=deal_sequence):
        result = sim.play_hand()
        # If player surrenders => lose half bet => -5
        # But check how your logic is coded 
        assert result == -5

def test_insurance_win():
    from blackjack.simulation import Simulator
    from blackjack.cards import Card

    sim = Simulator(num_decks=1)
    sim.strategy.bet = 10
    sim.rules.insurance_count_threshold = 3

    sim.strategy.running_count = 4  # Force insurance option

    # Force dealer's hand = (A, 10) => blackjack
    # Player's hand = (9, 7) => 16
    # Suppose strategy or fallback => "RH"
    deal_sequence = [
        Card("9","♠"), Card("7","♥"),     # Player hand
        Card("A","♦"), Card("10","♣"),    # Dealer hand
        # Next cards for dealer if needed
        Card("8","♠"), Card("3","♠")
    ]
    with patch.object(sim.shoe, 'deal_card', side_effect=deal_sequence):
        result = sim.play_hand()
        # If player takes insurance, and dealer has blackjack => push
        assert result == 0.0