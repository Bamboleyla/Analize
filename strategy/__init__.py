import pandas as pd

from .methods.plot_data import plot_data_method

__all__ = ["BigWaves"]


class BigWaves:
    def __init__(self, config: dict) -> None:
        self.name: str = "BigWaves"
        self._config = config

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def get_config(self) -> dict:
        pass

    def get_indicators_params(self) -> dict:
        pass

    def get_plot_data(self):
        return plot_data_method(self)
