import pandas as pd

__all__ = ["BigWaves"]


class BigWaves:
    def __init__(self, config: dict) -> None:
        self.name: str = "BigWaves"
        self.config = config

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def get_config(self) -> dict:
        pass

    def get_indicators_params(self) -> dict:
        pass

    def get_plot_data(self):
        pass
