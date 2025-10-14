"""Main file for the project"""

import os
import time
import pandas as pd

from terminal import Terminal
from strategies.big_waves import BigWaves
from strategies.moving_grid import MovingGrid
from services.download_and_update_quotes import download_and_update_quotes
from services.manager import Manager

if __name__ == "__main__":

    MESSAGE = """Choose mode:
1 - download historical data from Alor;
2 - show BigWaves;
3 - launch grid strategy;
0 - exit;
                        
Please, enter mode:"""

    # Choose mode
    mode = int(input(MESSAGE))
    # Download historical data from Alor broker
    if mode == 1:
        download_and_update_quotes()

    elif mode == 2:
        # Show Big Waves
        start_time = time.time()
        manager = Manager("SBER")
        quotes = manager.get_quotes()
        quotes_completed = time.time()
        print(
            "Quotes completed..." + str(round(quotes_completed - start_time, 3)) + "s"
        )

        directory = manager.get_directory()

        config = {
            "indicators": [
                {"type": "price_chanel", "period": 30},
                {"type": "super_trend", "period": 30, "multiplier": 7},
            ],
        }
        strategy = BigWaves(config)
        terminal = Terminal(strategy)

        # Calculate data
        prepared_data = terminal.prepare(quotes=quotes)
        # Write DataFrame to file
        prepared_data.to_csv(os.path.join(directory, "prepared_data.csv"), index=False)
        data_prepared = time.time()
        print(
            "Data completed..." + str(round(data_prepared - quotes_completed, 3)) + "s"
        )

        explore_date = terminal.calculate(prepared_data)
        calculate_completed = time.time()
        print(
            "Calculate completed..."
            + str(round(calculate_completed - data_prepared, 3))
            + "s"
        )
        explore_date.to_csv(
            os.path.join(directory, "price_chanel_report.csv"), index=False
        )
        terminal.report(explore_date)
        terminal.show(explore_date)
    elif mode == 3:
        # Show Grid Strategy
        start_time = time.time()
        manager = Manager("SBER")
        quotes = manager.get_quotes()
        quotes_completed = time.time()
        print(
            "Quotes completed..." + str(round(quotes_completed - start_time, 3)) + "s"
        )

        directory = manager.get_directory()

        config = {
            "indicators": [
                {
                    "type": "grid_chanel",
                    "steps": [1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12, 13.5, 15],
                },
            ],
        }
        strategy = MovingGrid(config)
        terminal = Terminal(strategy)

        # Calculate data
        prepared_data = terminal.prepare(quotes=quotes)
        # prepared_data = pd.read_csv(
        #     os.path.join("c:\\Users\\user\\python\\analize\\", "grid_chanel.csv"),
        #     header=0,
        # )

        data_prepared = time.time()
        print(
            "Data prepared..." + str(round(data_prepared - quotes_completed, 3)) + "s"
        )

        explore_date = strategy.calculate(prepared_data)

        # Write DataFrame to file
        explore_date.to_excel("result_grid.xlsx", index=False)

        calculate_completed = time.time()
        print(
            "Calculate completed..."
            + str(round(calculate_completed - data_prepared, 3))
            + "s"
        )

        # terminal.report(explore_date)
        terminal.show(explore_date)

    # Exit
    elif mode == 0:
        print("Program exit")
    else:
        print("Invalid mode. Stopping the program. Exiting...")
