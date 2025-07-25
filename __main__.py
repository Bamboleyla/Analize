"""Main file for the project"""

import os
import time
import pandas as pd

from new_terminal import NewTerminal
from services.download_and_update_quotes import download_and_update_quotes
from services.get_history_from_t import get_history_from_t
from services.manager import Manager
from myLib.strategies import PriceChanelGrid
from myLib.brokers import DemoBroker


if __name__ == "__main__":

    MESSAGE = """Choose mode:
1 - download historical data from Alor;
2 - show PriceChanelGrid;
0 - exit;
                        
Please, enter mode:"""

    # Choose mode
    mode = int(input(MESSAGE))
    # Download historical data from Alor broker
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
    # Exit
    elif mode == 0:
        print("Program exit")
    else:
        print("Invalid mode. Stopping the program. Exiting...")
