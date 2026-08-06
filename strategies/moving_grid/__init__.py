import pandas as pd

from .methods.calculate import calculate_method
from .methods.plot_data import plot_data_method
from .methods.optimizer import optimize_moving_grid

__all__ = ["MovingGrid"]


class MovingGrid:
    def __init__(self, config: dict) -> None:
        self.name: str = "MovingGrid"
        self._config = config

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        return calculate_method(data=data, indicators=self._config["indicators"])

    def optimize(
        self,
        quotes: pd.DataFrame,
        step_range: list[int] = None,
        levels_range: list[int] = None,
        top_n: int = 10,
    ) -> pd.DataFrame:
        return optimize_moving_grid(
            quotes=quotes,
            step_range=step_range,
            levels_range=levels_range,
            top_n=top_n,
        )

    def get_config(self) -> dict:
        pass

    def get_indicators_params(self) -> dict:
        pass

    def get_plot_data(self):
        return plot_data_method(self)

