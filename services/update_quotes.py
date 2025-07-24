"""In this file is the function update_quotes which updates the quotes"""

import logging
import os
from datetime import datetime, timezone, timedelta
import pandas as pd
from myLib.brokers import Alor

logger = logging.getLogger(__name__)


def update_quotes(file_path: str, ticker: str) -> None:
    """
    Update quotes for a given ticker in a CSV file.

    This function reads existing quotes from a file, fetches new quotes from a broker,
    and updates the file with the combined data. If the file doesn't exist, it creates one.

    Args:
        file_path (str): The path to the CSV file where quotes are stored.
        ticker (str): The ticker symbol for which to update quotes.

    Returns:
        None

    Side effects:
        - Creates a new file if it doesn't exist.
        - Updates the existing file with new quote data.
        - Prints a message if no new data is available for the ticker.
    """
    if not os.path.exists(file_path):  # if file with quotes doesn't exist
        with open(file_path, "w") as f:  # write first line
            f.write(
                "TICKER,DATE,OPEN,HIGH,LOW,CLOSE,VOLUME\n"
            )  # create date file in directory

    quotes = pd.read_csv(file_path, header=0)  # read quotes from file data.csv

    # get last date from file,
    # if there is no data then it will be firs minute of first day of previous month
    last_date: datetime

    if quotes.empty:
        last_date = datetime(
            2024, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=3))
        )  # Get first day of 2024 year
    else:
        # Return value from the last row of column 'date' in datetime format
        last_date = datetime.strptime(
            quotes.iloc[-1]["DATE"], "%Y%m%d %H:%M:%S"
        ).replace(tzinfo=timezone(timedelta(hours=3)))

    broker = Alor()  # create broker
    data = broker.downloader.get_quotes(
        ticker=ticker, start_date=last_date, tf=300
    )  # get data from last date to now

    if len(data) > 0:
        quotes = pd.concat([quotes[0:-1], data])  # update quotes
        quotes.to_csv(file_path, index=False)  # write quotes to file

    else:
        print(f"No data for {ticker}")
