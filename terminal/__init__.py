import logging
import os
import pandas as pd
import json

from .methods.run import run_method
from .methods.calculate import calculate_method
from .methods.report import report_method
from .methods.show import show_method
from .methods.optimize import optimize_method

__all__ = ["Terminal"]

logger = logging.getLogger(__name__)


class Terminal:
    """
    A class representing a Double Super Trend (Terminal) trading strategy implementation.

    This class provides methods for running, calculating, reporting, visualizing,
    and optimizing trading strategies using super trend indicators.

    Attributes:
        __directory (str): Path to the configuration directory.
        __indicators_aleases (dict): Mapping of indicator aliases for fast and slow super trends.
        __var_take (float): Default take profit value from configuration.
        __super_trends (dict): Super trend indicator configurations.

    Methods:
        run: Execute super trend analysis on input quotes.
        calculate: Calculate trading indicators and metrics.
        report: Generate a trading report.
        show: Display trading visualizations or reports.
        optimize: Optimize trading strategy parameters.
    """

    def __init__(self, directory: str):
        self.__directory = directory

        with open(os.path.join(self.__directory, "config.json"), "r") as f:
            config = json.load(f)
            self.__var_take = config["var_take"]
            self.__super_trends = config["indicators"]["super_trends"]

    def run(self, quotes: pd.DataFrame) -> pd.DataFrame:
        """
        Execute the run method for super trend analysis on the given quotes.

        Args:
            quotes (pd.DataFrame): Input DataFrame containing financial quotes data.

        Returns:
            pd.DataFrame: Processed DataFrame with run method results.
        """
        return run_method(
            directory=self.__directory, super_trends=self.__super_trends, quotes=quotes
        )

    def calculate(self, data: pd.DataFrame, var_take: float = None) -> pd.DataFrame:
        """
        Calculate trading indicators and metrics based on the input DataFrame.

        Args:
            data (pd.DataFrame): Input DataFrame containing financial quotes data.
            var_take (float, optional): Custom take profit value. Defaults to None.

        Returns:
            pd.DataFrame: Processed DataFrame with calculated trading indicators and metrics.
        """

        return calculate_method(
            data=data,
        )

    def report(
        self, data: pd.DataFrame, mode: str = "default", var_take: float = None
    ) -> pd.DataFrame:
        """
        Generate a trading report based on the input DataFrame.

        Args:
            data (pd.DataFrame): Input DataFrame containing financial quotes data.
            mode (str, optional): Report generation mode. Defaults to "default".
            var_take (float, optional): Custom take profit value. Defaults to None.

        Returns:
            pd.DataFrame: Processed DataFrame containing the generated trading report.
        """

        return report_method(
            default_take=self.__var_take,
            directory=self.__directory,
            data=data,
            mode=mode,
            var_take=var_take,
        )

    def show(self, data: pd.DataFrame, config: dict) -> None:
        """
        Display a visualization or report based on the input DataFrame.

        Args:
            data (pd.DataFrame): Input DataFrame containing financial quotes data.

        Returns:
            None: Generates a visualization or report without returning a value.
        """
        show_method(
            create_report=self.report,
            data=data,
            config=config,
        )

    def optimize(self, data: pd.DataFrame, var_take: dict) -> None:
        """
        Optimize trading strategy parameters based on input data.

        Args:
            data (pd.DataFrame): Input DataFrame containing financial quotes data.
            var_take (dict): Dictionary of take profit parameters for optimization.

        Returns:
            None: Performs optimization without returning a value.
        """
        optimize_method(
            calculate=self.calculate,
            report=self.report,
            directory=self.__directory,
            data=data,
            var_take=var_take,
        )
