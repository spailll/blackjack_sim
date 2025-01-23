from blackjack.simulation import Simulator

def main():
    simulator = Simulator(strategy_name="deviations", num_decks=2)
    results = simulator.run_simulation()

    print(results)


if __name__ == "__main__":
    main()