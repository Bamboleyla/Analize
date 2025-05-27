"""Calculate trading report with account balance and P/L tracking.

Args:
    default_take (float): Default take profit value
    directory (str): Directory path for data
    data (pd.DataFrame): DataFrame containing trading data
    mode (str, optional): Trading mode. Defaults to "default"
    var_take (float, optional): Variable take profit value. Defaults to None

Returns:
    pd.DataFrame: DataFrame with trading report including:
        - TICKER: Stock symbol
        - DATE: Trade date
        - SIGNAL: Trading signal
        - BUY_PRICE: Entry price
        - SELL_PRICE: Exit price
        - COMMISSION: Trading commission
        - P/L: Profit/Loss
        - ACCOUNT: Account balance after trade
"""

import os
import pandas as pd


def report_method(
    default_take: float,
    directory: str,
    data: pd.DataFrame,
    mode: str = "default",
    var_take: float = None,
) -> pd.DataFrame:
    """
    Calculate a trading report with account balance and profit/loss tracking.

    Args:
        default_take (float): Default take profit value
        directory (str): Directory path for saving report data
        data (pd.DataFrame): DataFrame containing trading data
        mode (str, optional): Trading mode. Defaults to "default"
        var_take (float, optional): Variable take profit value. Defaults to None

    Returns:
        pd.DataFrame: Trading performance report with metrics including:
            - Number of trades
            - Loss and profit counts
            - Win rate
            - Account start and end balance
            - Overall trading result percentage
    """

    if var_take is None:
        var_take = default_take
    # list of deals
    deals = pd.DataFrame()  # create empty DataFrame
    # add columns
    deals[["TICKER", "DATE", "SIGNAL", "BUY_PRICE", "SELL_PRICE"]] = data[
        ["TICKER", "DATE", "SIGNAL", "BUY_PRICE", "SELL_PRICE"]
    ]
    deals = deals[deals["SIGNAL"].notnull()]
    deals = deals.assign(COMMISSION=None, **{"P/L": None}, ACCOUNT=None)  # add columns

    init = 3000  # initial capital
    account = init  # current capital
    commission = 0.00005  # commission
    last_buy_price = 0  # last buy price
    trades = 0  # number of trades

    for index, row in deals.iterrows():
        if not pd.isnull(row["BUY_PRICE"]):
            deals.loc[index, "COMMISSION"] = round(
                10 * row["BUY_PRICE"] * commission, 2
            )
            account -= round(
                (10 * row["BUY_PRICE"]) + deals.loc[index, "COMMISSION"], 2
            )
            deals.loc[index, "ACCOUNT"] = account
            last_buy_price = row["BUY_PRICE"]

        elif not pd.isnull(row["SELL_PRICE"]):
            deals.loc[index, "COMMISSION"] = round(
                10 * row["SELL_PRICE"] * commission, 2
            )
            account += round(
                (10 * row["SELL_PRICE"]) - deals.loc[index, "COMMISSION"], 2
            )
            deals.loc[index, "ACCOUNT"] = account
            deals.loc[index, "P/L"] = (row["SELL_PRICE"] - last_buy_price) * 10
            last_buy_price = 0
            trades += 1
    if mode == "default":
        deals.to_excel(os.path.join(directory, "deals.xlsx"), index=False)

    loss = len(deals[deals["P/L"] < 0])  # number of losses
    profit = len(deals[deals["P/L"] > 0])  # number of profits
    win_rate = str(round((profit / (loss + profit)) * 100, 2)) + "%"  # win rate
    result = (account - init) / init * 100  # result in %

    # report
    report = pd.DataFrame(
        columns=[
            "var_take",
            "trades",
            "loss",
            "profit",
            "win_rate",
            "account_start",
            "account_end",
            "result",
        ]
    )
    report.loc[len(report)] = [
        var_take,
        trades,
        loss,
        profit,
        win_rate,
        init,
        round(account, 2),
        str(round(result, 2)) + "%",
    ]
    print(report)

    return report
