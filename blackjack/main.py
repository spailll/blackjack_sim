from blackjack.simulation import Simulator
from blackjack.analysis import analyze_simulation_results

def main():
    # results = []
    # for _ in range(100):
    #     simulator = Simulator(strategy_name="deviations", num_decks=2, debug=False, base_bet=25)
    #     result = simulator.run_simulation(num_hands=1000, bankroll_limit=1000)
    #     results.append(result)
        
    simulator = Simulator(strategy_name="deviations", num_decks=2, debug=False, base_bet=25)
    result = simulator.run_simulation(num_hands=5000000)
    # print(f"House Edge: {result['House Advantage (%)']}")
    print(result['House Advantage (%)'])
    print(result['avg_profit_per_hand'])
    # analysis = analyze_simulation_results(results)
    # print(analysis)


if __name__ == "__main__":
    main()