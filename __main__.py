"""Main file for the project"""

import logging
import os
import json
import time
from logging.handlers import RotatingFileHandler
import pandas as pd

from new_terminal import NewTerminal
from services.download_and_update_quotes import download_and_update_quotes
from services.manager import Manager
from terminal import Terminal
from myLib.strategies import PriceChanelGrid
from myLib.brokers import DemoBroker

logger = logging.getLogger(__name__)


def prepare_logs() -> None:
    """Prepare logging system for the bot.

    This function does the following:
        - Ensure "logs/" directory exists in the current working directory.
        - Set up basic configuration for the logging module.
        - Configure a rotating file handler which logs to robot.log in the logs/ directory.
    """
    # Ensure "logs/" directory exists in the current working directory
    if not os.path.exists("logs/"):
        # Create "logs/" directory
        os.makedirs("logs/")

    # Set up basic configuration for the logging module
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        handlers=[
            RotatingFileHandler(
                "logs/robot.log", maxBytes=100000000, backupCount=10, encoding="utf-8"
            )
        ],
        encoding="utf-8",
    )


def prepare_tickers() -> None:
    """This function checks the existence of directory and files with configuration for tickers"""

    for ticker in ["SBER"]:
        # Check ticker directory
        if not os.path.exists("tickers/" + ticker + "/"):
            # Create ticker directory
            os.makedirs("tickers/" + ticker + "/")

        # Check config file
        if not os.path.exists("tickers/" + ticker + "/config.json"):
            # Create default config
            default = {
                "indicators": {
                    "super_trends": [
                        {"period": 10, "multiplier": 3},
                        {"period": 20, "multiplier": 5},
                    ]
                },
                "var_take": 1.5,
            }
            # Create config file
            with open("tickers/" + ticker + "/config.json", "w", encoding="utf-8") as f:
                json.dump(default, f)


if __name__ == "__main__":

    prepare_logs()  # Prepare logging system
    logger.info("Program start")

    prepare_tickers()  # Prepare directories for tickers (if they don't exist)

    MESSAGE = """Choose mode:
1 - download historical data;
2 - show PriceChanelGrid;
3 - show WithDoubleTrend;
4 - optimize;
0 - exit;
                        
Please, enter mode:"""

    # Choose mode
    mode = int(input(MESSAGE))
    # Download historical data
    if mode == 1:
        download_and_update_quotes()
    elif mode == 2:
        # Show PriceChanelGrid
        start_time = time.time()
        manager = Manager("SBER")
        quotes = manager.get_quotes()
        quotes_completed = time.time()
        print(
            "Quotes completed..." + str(round(quotes_completed - start_time, 3)) + "s"
        )

        directory = manager.get_directory()
        broker = DemoBroker()

        config = {
            "indicators": [
                {"type": "price_chanel", "period": 30},
                {"type": "super_trend", "period": 30, "multiplier": 7},
            ],
            "share": {"tiker": "SBER", "figi": "BBG004730N88"},
        }
        strategy = PriceChanelGrid(broker, config)
        terminal = NewTerminal(strategy)

        # Create empty DataFrame with columns
        explore_date = pd.DataFrame(
            columns=["TICKER", "DATE", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
        )
        # Calculate data
        explore_date = terminal.prepare(quotes=quotes)
        # Write DataFrame to file
        explore_date.to_csv(
            os.path.join(directory, "price_chanel_grid.csv"), index=False
        )
        data_completed = time.time()
        print(
            "Data completed..." + str(round(data_completed - quotes_completed, 3)) + "s"
        )

        explore_date = terminal.calculate(explore_date)
        calculate_completed = time.time()
        print(
            "Calculate completed..."
            + str(round(calculate_completed - data_completed, 3))
            + "s"
        )
        explore_date.to_csv(
            os.path.join(directory, "price_chanel_report.csv"), index=False
        )
        terminal.report(explore_date)
        terminal.show(explore_date)
    # Show SuperTrends strategy
    elif mode == 3:
        start_time = time.time()
        manager = Manager("SBER")
        quotes = manager.get_quotes()
        quotes_completed = time.time()
        print(
            "Quotes completed..." + str(round(quotes_completed - start_time, 3)) + "s"
        )

        directory = manager.get_directory()
        terminal = Terminal(directory)

        # Check if file with data exists
        if os.path.exists(os.path.join(directory, "explore.csv")):
            # Read data from file
            explore_date = pd.read_csv(os.path.join(directory, "explore.csv"), header=0)
        else:
            # Create empty DataFrame with columns
            explore_date = pd.DataFrame(
                columns=["TICKER", "DATE", "OPEN", "HIGH", "LOW", "CLOSE"]
            )
            # Write DataFrame to file
            explore_date.to_csv(os.path.join(directory, "explore.csv"), index=False)
            # Calculate data
            explore_date = terminal.run(quotes)

        # If the data and quotes have the same last dates, then there is no point in recalculating
        data = (
            explore_date
            if (explore_date["DATE"].iloc[-1] == str(quotes["DATE"].iloc[-1]))
            else terminal.run(quotes)
        )
        data.to_csv(
            os.path.join(directory, "explore.csv"), index=False
        )  # write data to file
        data_completed = time.time()
        print(
            "Data completed..." + str(round(data_completed - quotes_completed, 3)) + "s"
        )

        data, config = terminal.calculate(data)
        calculate_completed = time.time()
        print(
            "Calculate completed..."
            + str(round(calculate_completed - data_completed, 3))
            + "s"
        )

        print("Start show...")
        terminal.show(data=data, config=config)
    # Optimize
    elif mode == 4:
        manager = Manager("SBER")

        data = pd.read_csv(manager.get_terminal_path(), header=0)

        terminal = Terminal(manager.get_directory())
        terminal.optimize(data, {"start": 1.0, "step": 0.1, "end": 3.0})
    # Exit
    elif mode == 0:
        print("Program exit")
    else:
        print("Invalid mode. Stopping the program. Exiting...")
