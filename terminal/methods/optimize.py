"""

This module provides optimization functionality for terminal-based methods.
Contains functions to optimize calculations by iterating through parameter ranges
and generating reports.

The main function optimize_method() takes calculation and reporting functions
as input along with configuration parameters to perform iterative optimization
over a specified range of values. Results are saved to Excel files.
"""

import os
import pandas as pd


def optimize_method(
    calculate: callable,
    report: callable,
    directory: str,
    data: pd.DataFrame,
    var_take: dict,
) -> None:
    """
    Optimize a method by iteratively calculating and reporting results over a specified range.

    Args:
        calculate (callable): Function to calculate results for a given iteration.
        report (callable): Function to generate a report from calculation results.
        directory (str): Directory path to save the optimization results.
        data (pd.DataFrame): Input data for optimization.
        var_take (dict): Configuration dictionary with 'start', 'end', and 'step' keys.

    Returns:
        None: Saves optimization results to an Excel file in the specified directory.
    """

    start = var_take["start"]
    results = pd.DataFrame()

    while start <= var_take["end"]:
        data_copy = data.copy()
        result = calculate(data_copy, start)
        report = report(result, "optimization", start)
        results = pd.concat([results, report])

        start += var_take["step"]

    results.to_excel(os.path.join(directory, "optimization.xlsx"), index=False)
