# blackjack_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import time  # Used for simulating a long-running task
import platform

# Import the Simulator class from your simulation module
from blackjack.simulation import Simulator  # Adjust the import path as needed
from blackjack.analysis import analyze_simulation_results
from blackjack.utils import load_settings, save_to_yaml

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Simulator")
        
        # Detect Operating System
        os_name = platform.system()
        
        if os_name == "Windows":
            self.root.state('zoomed')  # Maximizes the window on Windows
        elif os_name == "Linux":
            self.root.attributes('-zoomed', True)  # Attempts to maximize on Linux
        elif os_name == "Darwin":  # macOS
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")
        else:
            self.root.geometry("1400x900")  # Default size for other OS
        
        # Set minimum and maximum sizes (optional)
        self.root.minsize(1200, 800)
        self.root.maxsize(2000, 1600)
        
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)


        # Simulation Parameters Frame
        sim_params_frame = ttk.LabelFrame(main_frame, text="Simulation Parameters")
        sim_params_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

        sim_type_frame = ttk.LabelFrame(main_frame, text="Simulation Type")
        sim_type_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Game Rules Frame
        game_rules_frame = ttk.LabelFrame(main_frame, text="Game Rules")
        game_rules_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        spread_config_frame = ttk.LabelFrame(main_frame, text="Spread Configuration")
        spread_config_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Configure grid weights
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)


        # ---------------- Simulation Type ----------------
        self.sim_type_var = tk.StringVar(value="Casino Edge")

        ttk.Radiobutton(sim_type_frame, text="Casino Edge", variable=self.sim_type_var, value="Casino Edge").pack(side="left", padx=10, pady=5)

        ttk.Radiobutton(sim_type_frame, text="Risk of Ruin", variable=self.sim_type_var, value="Risk of Ruin").pack(side="left", padx=10, pady=5)

        # ---------------- Simulation Parameters ----------------

        # Number of Hands
        ttk.Label(sim_params_frame, text="Number of Hands per Simulation:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.hands_var = tk.IntVar(value=100000)
        ttk.Entry(sim_params_frame, textvariable=self.hands_var, width=15).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Base Bet Amount
        ttk.Label(sim_params_frame, text="Base Bet Amount ($):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.bet_var = tk.DoubleVar(value=15.0)
        ttk.Entry(sim_params_frame, textvariable=self.bet_var, width=15).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Number of Simulation Runs
        ttk.Label(sim_params_frame, text="Number of Simulation Runs:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.runs_var = tk.IntVar(value=10)
        ttk.Entry(sim_params_frame, textvariable=self.runs_var, width=15).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Bankroll Limit
        ttk.Label(sim_params_frame, text="Bankroll Limit (Optional) ($):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.bankroll_var = tk.DoubleVar(value=0.0)
        ttk.Entry(sim_params_frame, textvariable=self.bankroll_var, width=15).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Counting System Selection
        ttk.Label(sim_params_frame, text="Counting System:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.counting_var = tk.StringVar()
        counting_systems = [
            "hi-lo", "hi-lo opt I", "hi-lo opt II", "k-o", "mentor", "omega II",
            "rkeo", "reverse point count", "reverse 14 count", "reverse rapc",
            "silver fox", "unbalanced zen 2", "uston apc", "uston ss",
            "wong halves", "zen count"
        ]
        self.counting_combo = ttk.Combobox(sim_params_frame, textvariable=self.counting_var,
                                           values=counting_systems, state="readonly", width=20)
        self.counting_combo.current(0)
        self.counting_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Insurance Threshold
        ttk.Label(sim_params_frame, text="Insurance Threshold:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.insurance_threshold_var = tk.IntVar(value=3)
        ttk.Entry(sim_params_frame, textvariable=self.insurance_threshold_var, width=15).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Strategy Name
        ttk.Label(sim_params_frame, text="Strategy Name:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.strategy_name_var = tk.StringVar()
        strategies = ["basic", "deviations"]  # Add more strategies as needed
        self.strategy_combo = ttk.Combobox(sim_params_frame, textvariable=self.strategy_name_var,
                                           values=strategies, state="readonly", width=20)
        self.strategy_combo.current(0)
        self.strategy_combo.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Spread Name
        ttk.Label(sim_params_frame, text="Spread Name:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.spread_name_var = tk.StringVar()
        spreads = ["none", "basic", "custom"]  # Add more spreads as needed
        self.spread_combo = ttk.Combobox(sim_params_frame, textvariable=self.spread_name_var,
                                         values=spreads, state="readonly", width=20)
        self.spread_combo.current(0)
        self.spread_combo.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        # ---------------- Game Rules ----------------

        # Number of Decks
        ttk.Label(game_rules_frame, text="Number of Decks:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.decks_var = tk.IntVar(value=2)
        ttk.Spinbox(game_rules_frame, from_=1, to=8, textvariable=self.decks_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Blackjack Payout
        ttk.Label(game_rules_frame, text="Blackjack Payout (1:X):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.blackjack_payout_var = tk.DoubleVar(value=1.5)
        ttk.Entry(game_rules_frame, textvariable=self.blackjack_payout_var, width=15).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Penetration
        ttk.Label(game_rules_frame, text="Penetration (%):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.penetration_var = tk.DoubleVar(value=0.25)
        ttk.Entry(game_rules_frame, textvariable=self.penetration_var, width=15).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Hit on Soft 17
        self.hit_soft_17_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(game_rules_frame, text="Hit on Soft 17", variable=self.hit_soft_17_var).grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Surrender Allowed
        self.surrender_allowed_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(game_rules_frame, text="Surrender Allowed", variable=self.surrender_allowed_var).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Double After Split
        self.double_after_split_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(game_rules_frame, text="Double After Split", variable=self.double_after_split_var).grid(row=4, column=0, padx=5, pady=5, sticky="w")

        # Insurance Allowed
        self.insurance_allowed_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(game_rules_frame, text="Insurance Allowed", variable=self.insurance_allowed_var).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # ---------------- Spread Configuration ----------------

        self.spread_config_vars = []

        for i, num in enumerate(range(-8, 9)):
            label_text = f"TC +{num}" if num > 0 else f"TC {num}"
            label = ttk.Label(spread_config_frame, text=label_text)
            label.grid(row=0, column=i, padx=5, pady=(0, 5))

            var = tk.StringVar()
            self.spread_config_vars.append(var)

            entry = ttk.Entry(spread_config_frame, textvariable=var, width=5, justify="center")
            entry.grid(row=1, column=i, padx=5, pady=(0, 5))



        # Additional Game Rules (Add as needed)
        # Example:
        # self.example_rule_var = tk.BooleanVar(value=False)
        # ttk.Checkbutton(game_rules_frame, text="Example Rule", variable=self.example_rule_var).grid(row=5, column=0, padx=5, pady=5, sticky="w")

        # Enable GUI to expand
        for i in range(11):
            sim_params_frame.columnconfigure(i, weight=1)
        for i in range(5):
            game_rules_frame.columnconfigure(i, weight=1)

        # ---------------- Buttons ----------------

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.run_button = ttk.Button(button_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(side="left", padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset Fields", command=self.reset_fields)
        self.reset_button.pack(side="left", padx=5)

        self.export_button = ttk.Button(button_frame, text="Export Results", command=self.export_results, state="disabled")
        self.export_button.pack(side="left", padx=5)

        # ---------------- Progress Bar ----------------

        self.progress = ttk.Progressbar(main_frame, orient='horizontal', mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # ---------------- Results Display ----------------

        results_frame = ttk.LabelFrame(main_frame, text="Simulation Results")
        results_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Configure results_frame to expand
        main_frame.rowconfigure(4, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=1)
        results_frame.rowconfigure(1, weight=1)

        # Text Area for Statistics
        self.results_text = tk.Text(results_frame, height=10, state="disabled")
        self.results_text.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # Plot Area
        plot_frame = ttk.Frame(results_frame)
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        plot_frame2 = ttk.Frame(results_frame)
        plot_frame2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.figure2, self.ax2 = plt.subplots(figsize=(5, 4))
        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=plot_frame2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(fill="both", expand=True)

    def reset_fields(self):
        # Reset Simulation Parameters
        self.decks_var.set(2)
        self.hands_var.set(100000)
        self.bet_var.set(15.0)
        self.runs_var.set(10)
        self.bankroll_var.set(0.0)
        self.counting_combo.current(0)
        self.blackjack_payout_var.set(1.5)
        self.insurance_threshold_var.set(3)
        self.strategy_combo.current(0)
        self.spread_combo.current(0)
        self.penetration_var.set(0.25)

        # Reset Game Rules
        self.hit_soft_17_var.set(True)
        self.surrender_allowed_var.set(True)
        self.double_after_split_var.set(True)
        self.insurance_allowed_var.set(True)

        # Reset Results and Plot
        self.results_text.config(state="normal")
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state="disabled")
        self.ax.clear()
        self.canvas.draw()

        self.ax2.clear()
        self.canvas2.draw()

        # Reset Progress Bar
        self.progress['value'] = 0

        # Disable Export Button
        self.export_button.config(state="disabled")

    def run_simulation(self):
        # Gather input parameters
        params = {
            "num_decks": self.decks_var.get(),
            "num_hands": self.hands_var.get(),
            "base_bet": self.bet_var.get(),
            "num_runs": self.runs_var.get(),
            "bankroll_limit": self.bankroll_var.get(),
            "strategy_name": self.strategy_name_var.get(),
            "spread_name": self.spread_name_var.get(),
            "penetration": self.penetration_var.get(),
            "double_after_split": self.double_after_split_var.get(),
            "dealer_hits_soft_17": self.hit_soft_17_var.get(),
            "blackjack_payout": self.blackjack_payout_var.get(),
            "surrender_allowed": self.surrender_allowed_var.get(),
            "insurance_allowed": self.insurance_allowed_var.get(),
            "insurance_threshold": self.insurance_threshold_var.get(),
            "counting_system": self.counting_var.get(),
            "sim_type": self.sim_type_var.get()
        }

        # Input Validation
        if params['num_decks'] < 1 or params['num_decks'] > 8:
            messagebox.showerror("Invalid Input", "Number of Decks must be between 1 and 8.")
            return

        if params['num_hands'] < 1:
            messagebox.showerror("Invalid Input", "Number of Hands must be at least 1.")
            return

        if params['base_bet'] <= 0:
            messagebox.showerror("Invalid Input", "Base Bet Amount must be greater than 0.")
            return

        if params['num_runs'] < 1:
            messagebox.showerror("Invalid Input", "Number of Simulation Runs must be at least 1.")
            return

        if params['penetration'] <= 0 or params['penetration'] > 1:
            messagebox.showerror("Invalid Input", "Penetration must be between 0 (exclusive) and 1 (inclusive).")
            return

        if params['blackjack_payout'] <= 0:
            messagebox.showerror("Invalid Input", "Blackjack Payout must be greater than 0.")
            return

        if params['insurance_threshold'] < 0:
            messagebox.showerror("Invalid Input", "Insurance Threshold cannot be negative.")
            return

        # Disable Run button to prevent multiple clicks
        self.run_button.config(state="disabled")
        self.export_button.config(state="disabled")
        self.results_text.config(state="normal")
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state="disabled")
        self.ax.clear()
        self.canvas.draw()
        self.progress['value'] = 0

        # Start simulation in a new thread
        thread = threading.Thread(target=self.simulation_thread, args=(params,))
        thread.start()

    def simulation_thread(self, params):
        results_list = []
        simulator = Simulator(debug=False)  # Initialize a single Simulator instance

        if params['spread_name'] == "custom":
            custom_vars = [int(var.get()) for var in self.spread_config_vars]

            spreads = load_settings("config/spread.yaml")

            # custom_spread = [int(var.get()) for var in self.spread_config_vars]

            custom_spread = []
            for i, num in enumerate(range(-8, 9)):                    
                if int(self.spread_config_vars[i].get()) != 0:
                    custom_spread += [{"count": num if i != 0 else -999, "bet": int(self.spread_config_vars[i].get())}]

            if "custom" in spreads:
                spreads["custom"]["thresholds"] = custom_spread
            else:
                sp = {"thresholds": custom_spread}
                spreads.update({"custom": sp})

            save_to_yaml(spreads, "config/spread.yaml")

        # Setup the simulator with the collected parameters
        simulator.setup(
            num_decks=params['num_decks'],
            num_hands=params['num_hands'],
            base_bet=params['base_bet'],
            double_after_split=params['double_after_split'],
            dealer_hits_soft_17=params['dealer_hits_soft_17'],
            blackjack_payout=params['blackjack_payout'],
            surrender_allowed=params['surrender_allowed'],
            insurance_threshold=params['insurance_threshold'],
            counting_system=params['counting_system'],
            strategy_name=params['strategy_name'],
            spread_name=params['spread_name'],
            penetration=params['penetration']
        )
        i = 0
        for run in range(1, params['num_runs'] + 1):
            # Update progress
            progress_percentage = (run - 1) / params['num_runs'] * 100
            self.progress['value'] = progress_percentage
            self.root.update_idletasks()

            # Run simulation
            result = simulator.run_simulation(
                num_hands=params['num_hands'],
                bankroll_limit=params['bankroll_limit'] if params['bankroll_limit'] > 0 else None
            )
            results_list.append(result)

            if params['num_runs'] > 1:
                # Update progress to 90%
                self.progress['value'] = (100 / params['num_runs']) * (i)
                self.root.update_idletasks()

        # Update progress to 100%
        self.progress['value'] = 100
        self.root.update_idletasks()

        # Analyze and display results
        if params["sim_type"] == "Risk of Ruin":
            self.display_results(results_list, params)
        else:
            self.display_results_nolim(results_list, params)

        # Re-enable Run button
        self.run_button.config(state="normal")

    def display_results_nolim(self, results, params):
        # Aggregate results
        total_hands_played = sum(result["hands_played"] for result in results)
        average_final_bankroll = sum(result["final_bankroll"] for result in results) / len(results)
        total_amount_bet = sum(result["amount_bet"] for result in results)
        average_profit_per_hand = sum(result["avg_profit_per_hand"] for result in results) / len(results)
        average_house_advantage = sum(result["House Advantage (%)"] for result in results) / len(results)

        # Display statistics
        stats = (
            f"Number of Runs: {params['num_runs']}\n"
            f"Total Hands Played: {total_hands_played}\n"
            f"Average Final Bankroll: ${average_final_bankroll:.2f}\n"
            f"Total Amount Bet: ${total_amount_bet:.2f}\n"
            f"Average Profit per Hand: ${average_profit_per_hand:.2f}\n"
            f"Average House Advantage: {average_house_advantage:.2f}%\n"
        )

        self.results_text.config(state="normal")
        self.results_text.insert(tk.END, stats)
        self.results_text.config(state="disabled")

        # Plot histogram of final bankrolls
        final_bankrolls = [result["final_bankroll"] for result in results]
        self.ax.hist(final_bankrolls, bins=20, color='skyblue', edgecolor='black')
        self.ax.set_title("Final Bankroll Distribution")
        self.ax.set_xlabel("Final Bankroll ($)")
        self.ax.set_ylabel("Frequency")
        self.canvas.draw()

        bankroll_histories = [result["bankroll_history"] for result in results]

        min_length = min(len(history) for history in bankroll_histories)

        truncated_histories = [history[:min_length] for history in bankroll_histories]

        average_bankroll_history = [sum(hand_bankrolls) / len(hand_bankrolls) for hand_bankrolls in zip(*truncated_histories)]

        hands_played = list(range(1, min_length + 1))

        self.ax2.plot(hands_played, average_bankroll_history, color='green')
        self.ax2.set_title("Average Bankroll Over Time")
        self.ax2.set_xlabel("Hands Played")
        self.ax2.set_ylabel("Average Bankroll ($)")
        self.ax2.grid(True)
        self.canvas2.draw()

        # Enable Export button
        self.export_button.config(state="normal")


    def display_results(self, results, params):
        # Aggregate results
        total_hands_played = sum(result["hands_played"] for result in results)
        average_final_bankroll = sum(result["final_bankroll"] for result in results) / len(results)
        total_amount_bet = sum(result["amount_bet"] for result in results)
        average_profit_per_hand = sum(result["avg_profit_per_hand"] for result in results) / len(results)
        average_house_advantage = sum(result["House Advantage (%)"] for result in results) / len(results)

        # Calculate Risk of Ruin
        analysis = analyze_simulation_results(results, params['bankroll_limit'])

        risk_of_ruin = analysis["risk_of_ruin"]
        avg_profit = analysis["mean_profit"]
        stddev_profit = analysis["stddev_profit"]
    
        # Display statistics
        stats = (
            f"Number of Runs: {params['num_runs']}\n"
            f"Total Hands Played: {total_hands_played}\n"
            f"Average Final Bankroll: ${average_final_bankroll:.2f}\n"
            f"Total Amount Bet: ${total_amount_bet:.2f}\n"
            f"Average Profit per Hand: ${average_profit_per_hand:.2f}\n"
            f"Average Profit: ${avg_profit:.2f}\n"
            f"Standard Deviation: ${stddev_profit:.2f}\n"
            f"Risk of Ruin: {risk_of_ruin:.2f}%\n"
        )

        self.results_text.config(state="normal")
        self.results_text.insert(tk.END, stats)
        self.results_text.config(state="disabled")

        # Plot histogram of final bankrolls
        final_bankrolls = [result["final_bankroll"] for result in results]
        self.ax.hist(final_bankrolls, bins=20, color='skyblue', edgecolor='black')
        self.ax.set_title("Final Bankroll Distribution")
        self.ax.set_xlabel("Final Bankroll ($)")
        self.ax.set_ylabel("Frequency")
        self.canvas.draw()
        
        bankroll_histories = [result["bankroll_history"] for result in results]

        min_length = min(len(history) for history in bankroll_histories)

        truncated_histories = [history[:min_length] for history in bankroll_histories]

        average_bankroll_history = [sum(hand_bankrolls) / len(hand_bankrolls) for hand_bankrolls in zip(*truncated_histories)]

        hands_played = list(range(1, min_length + 1))

        self.ax2.plot(hands_played, average_bankroll_history, color='green')
        self.ax2.set_title("Average Bankroll Over Time")
        self.ax2.set_xlabel("Hands Played")
        self.ax2.set_ylabel("Average Bankroll ($)")
        self.ax2.grid(True)
        self.canvas2.draw()

        # Enable Export button
        self.export_button.config(state="normal")

    def export_results(self):
        # Ask user where to save the CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                                 title="Save Results")
        if not file_path:
            return  # User cancelled

        # Extract data from results_text (simple example)
        # For a more detailed export, you should modify the simulation to store results in a structured format
        stats = self.results_text.get("1.0", tk.END).strip().split("\n")
        data = {}
        for stat in stats:
            if ": " in stat:
                key, value = stat.split(": ", 1)
                data[key.strip()] = value.strip()

        # Convert to DataFrame and save
        df = pd.DataFrame([data])
        try:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export Successful", f"Results exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An error occurred while exporting:\n{e}")

def main():
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
