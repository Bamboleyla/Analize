import pandas as pd

from .methods.calculate import calculate_method
from .methods.plot_data import plot_data_method

__all__ = ["MovingGrid"]


class MovingGrid:
    def __init__(self, config: dict) -> None:
        self.name: str = "MovingGrid"
        self._config = config

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        return calculate_method(data=data, indicators=self._config["indicators"])

    def get_config(self) -> dict:
        pass

    def get_indicators_params(self) -> dict:
        pass

    def get_plot_data(self):
        return plot_data_method(self)
