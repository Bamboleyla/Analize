import os
import pandas as pd

__all__ = ["Manager"]


class Manager:
    def __init__(self, ticker: str):
        self.__dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)) + "\\data\\", ticker
        )  # file path to ticker directory

    def get_quotes(self) -> pd.DataFrame:
        quotes = pd.read_csv(self.__dir + "\\data.csv", header=0)
        return quotes

    def get_directory(self) -> str:
        return self.__dir
