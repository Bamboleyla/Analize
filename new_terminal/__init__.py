import pandas as pd

from .methods.prepare import prepare_method


__all__ = ["NewTerminal"]


class NewTerminal:
    """
    New Terminal class for price channel grid strategy.
    """

    def __init__(self, strategy) -> None:
        self.strategy = strategy

    def prepare(self, quotes: pd.DataFrame) -> pd.DataFrame:
        return prepare_method(
            quotes=quotes, indicators=self.strategy.config["indicators"]
        )

    def calculate(self, quotes: pd.DataFrame) -> pd.DataFrame:
        return quotes

    def show(self, quotes: pd.DataFrame) -> None:
        pass

    def report(self, quotes: pd.DataFrame) -> None:
        pass
