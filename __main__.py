"""Main file for the project"""

import os
import time
import pandas as pd

from terminal import Terminal
from strategies.big_waves import BigWaves
from strategies.moving_grid import MovingGrid
from strategies.price_chanel import PriceChanel
from services.download_and_update_quotes import download_and_update_quotes
from services.manager import Manager
from services.resample import resample_quotes

if __name__ == "__main__":

    MESSAGE = """Choose mode:
1 - download historical data from Alor;
2 - show BigWaves;
3 - show Grid strategy;
4 - show PriceChanel (SBER, period 40, 1h TF);
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
        # MovingGrid Strategy
        print("\n--- Стратегия: MovingGrid ---")
        print("1 - Рассчитать бэктест и показать график/отчет")
        print("2 - Запустить модуль оптимизации параметров (шаг и количество уровней)")
        sub_mode_input = input("Выберите действие [1 по умолчанию]: ").strip()
        sub_mode = int(sub_mode_input) if sub_mode_input.isdigit() else 1

        start_time = time.time()
        manager = Manager("BANE")
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
                    "steps": [
                        30,
                        60,
                        90,
                        120,
                        150                       
                    ],
                },
            ],
        }
        strategy = MovingGrid(config)

        if sub_mode == 2:
            strategy.optimize(quotes=quotes)
        else:
            terminal = Terminal(strategy)

            # Calculate data
            prepared_data = terminal.prepare(quotes=quotes)

            data_prepared = time.time()
            print(
                "Data prepared..." + str(round(data_prepared - quotes_completed, 3)) + "s"
            )

            calc_start = time.time()
            explore_date = strategy.calculate(prepared_data)
            calculate_completed = time.time()
            print(
                "Calculate completed..."
                + str(round(calculate_completed - calc_start, 3))
                + "s"
            )

            # Write DataFrame to file
            export_start = time.time()
            explore_date.to_csv("result_grid.csv", index=False)
            export_completed = time.time()
            print(
                "Export completed..."
                + str(round(export_completed - export_start, 3))
                + "s"
            )

            terminal.show(explore_date)
            terminal.report(explore_date)

    elif mode == 4:
        # Show PriceChanel (SBER, period 40, 1h TF)
        start_time = time.time()
        manager = Manager("SBER")
        quotes = manager.get_quotes()
        quotes = resample_quotes(quotes, timeframe="1h")
        quotes_completed = time.time()
        print(
            "Quotes completed..." + str(round(quotes_completed - start_time, 3)) + "s"
        )

        directory = manager.get_directory()

        config = {
            "indicators": [
                {"type": "price_chanel", "period": 40},
            ],
        }
        strategy = PriceChanel(config)
        terminal = Terminal(strategy)

        # Calculate data
        prepared_data = terminal.prepare(quotes=quotes)
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
        terminal.show(explore_date)
        terminal.report(explore_date)

    # Exit
    elif mode == 0:
        print("Program exit")
    else:
        print("Invalid mode. Stopping the program. Exiting...")
