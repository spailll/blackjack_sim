# blackjack/analysis.py

import math
import statistics

def compute_basic_stats(results):
    if not results:
        return {
            "mean": 0,
            "std_dev": 0,
            "min": 0,
            "max": 0,
        }

    mean_val = statistics.mean(results)
    std_dev_val = statistics.pstdev(results)
    min_val = min(results)
    max_val = max(results)

    return {
        "mean": mean_val,
        "std_dev": std_dev_val,
        "min": min_val,
        "max": max_val,
    }

def confidence_interval(mean, stddev, n, confidence=0.95):
    if n <= 1:
        return (mean, mean)
    z = 1.96 # 95% confidence interval
    margin_of_error = z * (stddev / math.sqrt(n))
    return (mean - margin_of_error, mean + margin_of_error)

def compute_risk_of_ruin_monte_carlo(bankroll_history, ruin_threshold=0):
    if not bankroll_history:
        return 0.0

    bankrupt_count = sum(1 for bk in bankroll_history if bk < ruin_threshold)
    return bankrupt_count / len(bankroll_history)


def analyze_simulation_results(results):
    if not results:
        return {}
    
    final_bankrolls = [res["final_bankroll"] for res in results]

    stats = compute_basic_stats(final_bankrolls)
    mean = stats["mean"]
    stddev = stats["std_dev"]
    n = len(final_bankrolls)
    
    # Confidence Interval
    ci_lower, ci_upper = confidence_interval(mean, stddev, n)

    # Risk of Ruin
    ror = compute_risk_of_ruin_monte_carlo(final_bankrolls, ruin_threshold=0.0)

    analysis_results = {
        "mean_final_bankroll": mean,
        "stddev_final_bankroll": stddev,
        "CI_95": (ci_lower, ci_upper),
        "risk_of_ruin": ror,
        "min_final_bankroll": stats["min"],
        "max_final_bankroll": stats["max"],
    }

    return analysis_results


def compute_statistics(results):
    if not results:
        return {}
    
    mean = sum(results) / len(results)

    variance = sum((x - mean) ** 2 for x in results) / (len(results) - 1)
    std_dev = math.sqrt(variance)

    return {
        "mean": mean,
        "std_dev": std_dev,
        "min": min(results),
        "max": max(results),
    }
