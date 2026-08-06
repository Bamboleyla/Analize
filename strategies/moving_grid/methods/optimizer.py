import time
import pandas as pd
from myLib.indicators import grid_chanel
from .calculate import calculate_method


def _evaluate_config(quotes: pd.DataFrame, step_size: int, num_levels: int) -> dict:
    steps = [step_size * i for i in range(1, num_levels + 1)]
    indicators = [{"type": "grid_chanel", "steps": steps}]

    prepared = grid_chanel(df=quotes, steps=steps)
    res = calculate_method(data=prepared, indicators=indicators)

    final_balance = round(res["BALANCE"].iloc[-1], 2) if len(res) > 0 else 0.0
    total_commission = round(res["COMMISSION"].sum(), 2) if len(res) > 0 else 0.0
    closed_trades = int(res["PROFIT"].notna().sum()) if len(res) > 0 else 0
    max_long = int(res["POSITION"].max()) if len(res) > 0 else 0

    return {
        "step_size": step_size,
        "num_levels": num_levels,
        "max_grid_range": max(steps),
        "final_balance": final_balance,
        "total_commission": total_commission,
        "closed_trades": closed_trades,
        "max_long_pos": max_long,
    }


def optimize_moving_grid(
    quotes: pd.DataFrame,
    step_range: list[int] = None,
    levels_range: list[int] = None,
    top_n: int = 10,
) -> pd.DataFrame:
    if step_range is None:
        step_range = list(range(10, 101, 10))  # 10, 20, ..., 100
    if levels_range is None:
        levels_range = list(range(3, 21, 1))  # 3, 4, ..., 20

    total_combinations = len(step_range) * len(levels_range)
    print(
        f"\nStarting Grid Search optimization across {len(step_range)} step sizes and {len(levels_range)} level counts..."
    )
    print(f"Total parameter combinations to evaluate: {total_combinations}")
    start_t = time.time()

    tasks = [
        (step_size, num_levels)
        for step_size in step_range
        for num_levels in levels_range
    ]

    results = []
    for idx, (step_size, num_levels) in enumerate(tasks, 1):
        res = _evaluate_config(quotes, step_size, num_levels)
        results.append(res)
        if idx % 20 == 0 or idx == total_combinations:
            print(f"Progress: {idx}/{total_combinations} combinations evaluated...")

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="final_balance", ascending=False).reset_index(
        drop=True
    )

    elapsed = round(time.time() - start_t, 2)
    print(f"\nOptimization completed in {elapsed}s.")
    print(f"\n================ TOP {top_n} PARAMETER COMBINATIONS ================")
    print(results_df.head(top_n).to_string(index=False))
    print("====================================================================")

    results_df.to_csv("optimization_results.csv", index=False)
    print("\nFull optimization report saved to 'optimization_results.csv'\n")

    return results_df
