import pandas as pd

from .methods.report import report_method
from .methods.show import show_method
from .methods.prepare import prepare_method


__all__ = ["NewTerminal"]


class NewTerminal:
    """
    New Terminal class for price channel grid strategy.
    """

    def __init__(self, strategy) -> None:
        self.strategy = strategy
        self.strategy_config = strategy.get_config()

    def prepare(self, quotes: pd.DataFrame) -> pd.DataFrame:
        return prepare_method(
            quotes=quotes, indicators=self.strategy_config["indicators"]
        )

    def calculate(self, quotes: pd.DataFrame) -> pd.DataFrame:
        return self.strategy.calculate(quotes)

    def show(self, quotes: pd.DataFrame) -> None:
        show_method(data=quotes, config=self.strategy.get_plot_data())

    def report(self, quotes: pd.DataFrame) -> None:
        report_method(data=quotes)
