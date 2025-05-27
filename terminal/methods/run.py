"""
Run method to process and calculate SuperTrend indicators.

This function handles reading data from CSV, checking if SuperTrend indicators exist,
calculating new indicators if needed, and managing data updates.

Args:
    directory (str): Path to the directory containing the explore.csv file
    super_trends (dict[str, str]): Dictionary containing SuperTrend parameters (period and multiplier)
    quotes (pd.DataFrame): DataFrame containing price data with OHLC columns

Returns:
    pd.DataFrame: DataFrame containing the original data with calculated SuperTrend indicators
"""

import os
import pandas as pd
import talib

from indicators import super_trend


def run_method(
    directory: str, super_trends: dict[str, str], quotes: pd.DataFrame
) -> pd.DataFrame:
    """
    Read data from 'explore.csv' file, calculate SuperTrend indicators if they are not already in the data and return the result.

    If the SuperTrend indicators are already in the data, read the data from the file and return it. Otherwise, calculate the SuperTrend indicators
    and save the result to the 'explore.csv' file.
    """
    with open(os.path.join(directory, "explore.csv"), "r") as f:
        data = pd.read_csv(f, header=0)
        max_period = 0
        for indicator in super_trends:
            # check if the SuperTrend indicators not are already in the data
            if (
                f'ST {indicator["period"]} {indicator["multiplier"]} UP'
                not in data.columns
                or f'ST {indicator["period"]} {indicator["multiplier"]} LOW'
                not in data.columns
            ):
                # calculate the SuperTrend indicators
                copy = quotes[["TICKER", "DATE", "OPEN", "HIGH", "LOW", "CLOSE"]].copy()
                copy["EMA 50"] = talib.EMA(quotes["CLOSE"].values, timeperiod=50)
                copy["EMA 50"] = copy["EMA 50"].round(2)

                # return the calculated SuperTrend indicators
                return super_trend(super_trends, copy)

            # Update max_period with the maximum period from the indicators
            max_period = max(max_period, indicator["period"])

        # Calculate 50-period EMA for the closing prices
        quotes["EMA 50"] = talib.EMA(quotes["CLOSE"].values, timeperiod=50)
        quotes["EMA 50"] = quotes["EMA 50"].round(2)

        # Extract the data corresponding to the last max_period entries
        empty_data = quotes.iloc[len(data) - max_period :]

        # Get the last max_period data from existing data
        last_data = data.iloc[-max_period:]

        # Calculate new SuperTrend indicators
        new_data = super_trend(super_trends, empty_data, last_data)

        # Remove the 'volume' column from the new data
        new_data = new_data.drop(columns=["VOLUME"])

        # Concatenate the existing data with the newly calculated data, excluding the initial max_period entries
        return pd.concat([data, new_data.iloc[max_period:]], ignore_index=True)
