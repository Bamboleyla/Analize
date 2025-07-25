"""This file contains the download_and_update_quotes function, which uploads and updates the quotes data"""

import os
from services.update_quotes import update_quotes


def download_and_update_quotes() -> None:
    """
    Downloads and updates quotes for specified tickers and indexes.

    This function iterates through a predefined list of tickers and indexes,
    downloads their respective quotes, and updates the corresponding CSV files.
    It also logs the progress and prints status messages to the console.

    Returns:
        pd.DataFrame: A DataFrame containing the updated quotes data.
        Note: The current implementation does not actually return a DataFrame.

    Raises:
        Any exceptions raised by the update_quotes function or file operations
        are not explicitly handled in this function.

    Note:
        - The function uses hardcoded lists for tickers (["SBER"]) and indexes (["IMOEX"]).
        - The progress percentage is calculated based on the total number of items to process.
        - File paths are constructed using the current file's location and predefined directory structure.
    """
    percent_step = 100 / (
        len(["SBER", "TATN", "BSPB", "MOEX", "ROSN", "YDEX", "MGNT"]) + len(["IMOEX"])
    )  # initial percentage
    percentage = 0.0

    print("Start downloading...")

    for ticker in ["SBER", "TATN", "BSPB", "MOEX", "ROSN", "YDEX", "MGNT"]:

        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)) + "\\tickers\\",
            ticker,
            "data.csv",
        )  # file path for ticker

        update_quotes(file_path, ticker)

        percentage += percent_step

        print(f"Downloaded {ticker} quotes, {percentage:.2f}% completed")

    for index in ["IMOEX"]:
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)) + "\\indexes\\",
            index,
            "data.csv",
        )  # file path for index

        update_quotes(file_path, index)

        percentage += percent_step

        print(f"Downloaded {index} quotes, {percentage:.2f}% completed")

    print("Downloading completed")
