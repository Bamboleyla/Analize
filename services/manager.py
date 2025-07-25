import os
import pandas as pd
import talib

from indicators.super_trend import super_trend

__all__ = ["Manager"]


class Manager:
    def __init__(self, ticker: str):
        self.__dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)) + "\\tickers\\", ticker
        )  # file path to ticker directory

    def get_quotes(self) -> pd.DataFrame:
        quotes = pd.read_csv(self.__dir + "\\data.csv", header=0)
        return quotes

    def get_directory(self) -> str:
        return self.__dir

    def get_terminal_path(self) -> str:
        return os.path.join(self.__dir, "explore.csv")

    def get_terminal_data(self) -> pd.DataFrame:
        """
        Returns the terminal data for the ticker.

        If the terminal data does not exist, it is calculated and saved to a file.
        """
        terminal_file = os.path.join(self.__dir, "terminal.csv")
        if not os.path.exists(terminal_file):
            quotes = self.get_quotes()
            quotes["EMA_50"] = talib.EMA(quotes["close"].values, timeperiod=50)
            quotes["EMA_50"] = quotes["EMA_50"].round(2)

            terminal_data = super_trend(self.__super_trends, quotes)
            terminal_data.to_csv(terminal_file, index=False)
            return terminal_data

        return pd.read_csv(terminal_file, header=0)
