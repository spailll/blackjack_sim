from blackjack.simulation import Simulator
from blackjack.analysis import analyze_simulation_results

def main():
    # results = []
    # for _ in range(100):
    #     simulator = Simulator(strategy_name="deviations", num_decks=2, debug=False, base_bet=25)
    #     result = simulator.run_simulation(num_hands=1000, bankroll_limit=1000)
    #     results.append(result)
        
    simulator = Simulator(scenario=0, debug=True)
    result = simulator.run_simulation()
    print(f"Final Bankroll: ${result['final_bankroll']}")
    print(f"House Edge: {result['House Advantage (%)']}%")
    print(f"Average Profit per Hand: ${result['avg_profit_per_hand']}")
    # analysis = analyze_simulation_results(results)
    # print(analysis)


if __name__ == "__main__":
    main()