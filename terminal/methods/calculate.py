"""
Calculate method for executing trading strategies.

This module provides functionality to calculate trading signals and execute orders
using a double super trend strategy implementation.

Functions:
    calculate_method: Executes trading calculations using specified parameters.
"""

from datetime import datetime
import pandas as pd
from myLib.brokers import Brokers
from myLib.strategies import Strategies


def calculate_method(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate trading method using double super trend strategy.

    Args:
        default_take (float): Default take profit value.
        indicators_aleases (dict[str, str]): Dictionary of indicator aliases.
        data (pd.DataFrame): Input trading data DataFrame.
        var_take (float, optional): Variable take profit value. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame with added order log information.

    Executes a trading strategy using demo broker and double super trend method,
    processing each row of input data and generating market orders based on strategy logic.
    """

    broker = Brokers()
    demo_broker = broker.demo

    strategies = Strategies()
    with_dt = strategies.double_super_trend(demo_broker)

    for index, row in data.iterrows():
        demo_broker.run(row, index)
        if index == 0:
            continue
        elif index == len(data) - 1 and demo_broker.get_positions()["size"] > 0:
            demo_broker.create_order(
                {
                    "id": datetime.now().timestamp(),
                    "strategy": with_dt.name,
                    "signal": "LONG_SELL",
                    "order": "MARKET_SELL",
                    "price": row["OPEN"],
                }
            )

        with_dt.run(row)

    order_list = demo_broker.get_orders_log()

    return data.join(order_list), with_dt.get_plot_data()
