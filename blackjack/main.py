from blackjack.simulation import Simulator
from blackjack.analysis import analyze_simulation_results

def main():
    # results = []
    # initial_bankroll = 4500
    # for _ in range(5000):
    #     simulator = Simulator(debug=False)
    #     simulator.setup_from_config(scenario=0)
    #     result = simulator.run_simulation(num_hands=1000, bankroll_limit=initial_bankroll)
    #     # print(f"Final Bankroll: ${result['final_bankroll']}")
    #     results.append(result)

    # analysis = analyze_simulation_results(results, initial_bankroll)
    # print(analysis)


    simulator = Simulator(debug=False)
    simulator.setup()
    result = simulator.run_simulation()
    # print(f"Final Bankroll: ${result['final_bankroll']}")
    print(f"House Edge: {result['House Advantage (%)']}%")
    print(f"Average Profit per Hand: ${result['avg_profit_per_hand']}")



if __name__ == "__main__":
    main()