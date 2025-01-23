# blackjack/analysis.py

import math




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


