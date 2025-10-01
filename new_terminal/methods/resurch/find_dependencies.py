import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from myLib.points import find_growth_points
from myLib.features.super_trend import line_lenght
from pyparsing import line
from scipy.stats import ttest_ind, mannwhitneyu, median_abs_deviation, bootstrap


def find_dependencies_method(self, quotes: pd.DataFrame) -> pd.DataFrame:
    # quotes = find_growth_points(data=quotes, tp=1.01, sl=0.999, max_lookhead=100)
    # quotes = line_lenght(
    #     data=quotes, upper_column="ST_UPPER_30_7", lower_column="ST_LOWER_30_7"
    # )
    # quotes.to_csv("prepared_data.csv", index=False)
    quotes = pd.read_csv("prepared_data.csv", header=0)
    df = quotes.copy()
    # df = df[~df["ST_UPPER_30_7"].notnull()].reset_index(drop=True)

    df["PREV_OPEN"] = df["OPEN"].shift(1)
    df["PREV_CLOSE"] = df["CLOSE"].shift(1)
    df["PREV_HIGH"] = df["HIGH"].shift(1)
    df["PREV_LOW"] = df["LOW"].shift(1)

    # Создаем новые признаки

    # df["ST_LOWER"] = np.where(df["ST_LOWER_30_7"].notnull(), 1, 0)  # 0.062285
    # df["ST_UPPER"] = np.where(df["ST_UPPER_30_7"].notnull(), 1, 0)  # -0.061573

    # df["DIFF_ST_DOWN_PC_LOW"] = np.where(
    #     df["ST_LOWER_30_7"].notnull(),
    #     round(df["ST_LOWER_30_7"] - df["PC_30_LOW"], 3),
    #     0,
    # ) # -0.040560

    # df["DIFF_ST_UP_PC_HIGH"] = np.where(
    #     df["ST_UPPER_30_7"].notnull(),
    #     round(df["ST_UPPER_30_7"] - df["PC_30_HIGH"], 3),
    #     0,
    # ) # -0.062933

    df["DIFF_PC_HIGH_AND_LOWER"] = round(df["PC_30_HIGH"] - df["LOW"], 3)
    # df["DIFF_PC_MID_AND_LOWER"] = round(df["PC_30_MID"] - df["LOW"], 3) # 0.049366
    df["DIFF_PC_LOW_AND_LOWER"] = round(df["LOW"] - df["PC_30_LOW"], 3)  # 0.055593
    df["DIFF_PC_HIGH_AND_PC_LOW"] = round(df["PC_30_HIGH"] - df["PC_30_LOW"], 3)

    # df["DIFF_LOW_AND_PREV_LOW"] = np.where(df["LOW"] < df["PREV_LOW"], 1, 0) # 0.004261
    # df["DIFF_LOW_AND_PREV_OPEN"] = np.where(df["LOW"] < df["PREV_OPEN"], 1, 0) # 0.002471
    # df["DIFF_LOW_AND_PREV_CLOSE"] = np.where(df["LOW"] < df["PREV_CLOSE"], 1, 0) # -0.002113
    # df["DIFF_LOW_AND_PREV_HIGH"] = np.where(df["LOW"] < df["PREV_HIGH"], 1, 0) # -0.006585

    # df["DIFF_OPEN_AND_PREV_OPEN"] = np.where(df["OPEN"] < df["PREV_OPEN"], 1, 0) # 0.015604
    # df["DIFF_OPEN_AND_PREV_CLOSE"] = np.where(df["OPEN"] < df["PREV_CLOSE"], 1, 0) # 0.007347
    # df["DIFF_OPEN_AND_PREV_HIGH"] = np.where(df["OPEN"] < df["PREV_HIGH"], 1, 0) # 0.009685
    # df["DIFF_OPEN_AND_PREV_LOW"] = np.where(df["OPEN"] < df["PREV_LOW"], 1, 0) # 0.004971

    # df["DIFF_HIGH_AND_PREV_OPEN"] = np.where(df["HIGH"] < df["PREV_OPEN"], 1, 0) # -0.001290
    # df["DIFF_HIGH_AND_PREV_CLOSE"] = np.where(df["HIGH"] < df["PREV_CLOSE"], 1, 0) # -0.010164
    # df["DIFF_HIGH_AND_PREV_HIGH"] = np.where(df["HIGH"] < df["PREV_HIGH"], 1, 0) # -0.014139
    # df["DIFF_HIGH_AND_PREV_LOW"] = np.where(df["HIGH"] < df["PREV_LOW"], 1, 0) # 0.008220

    # df["DIFF_CLOSE_AND_PREV_CLOSE"] = np.where(df["CLOSE"] < df["PREV_CLOSE"], 1, 0) # -0.047579
    # df["DIFF_CLOSE_AND_PREV_OPEN"] = np.where(df["CLOSE"] < df["PREV_OPEN"], 1, 0) # -0.024420
    # df["DIFF_CLOSE_AND_PREV_HIGH"] = np.where(df["CLOSE"] < df["PREV_HIGH"], 1, 0) # -0.051383
    # df["DIFF_CLOSE_AND_PREV_LOW"] = np.where(df["CLOSE"] < df["PREV_LOW"], 1, 0) # -0.019664

    # # Проводим t-тест

    # Разделяем данные на четыре группы
    group_0_low = df[(df["GROWTH_POINT"] == 0) & (df["ST_LOWER_30_7"].notnull())]
    group_1_low = df[(df["GROWTH_POINT"] == 1) & (df["ST_LOWER_30_7"].notnull())]
    # group_up_0 = df[(df["GROWTH_POINT"] == 0) & (df["ST_UPPER_30_7"].notnull())]
    # group_up_1 = df[(df["GROWTH_POINT"] == 1) & (df["ST_UPPER_30_7"].notnull())]

    # Сравнение средних значений
    print(
        "Средние значения LOWER_LINE_LENGTH для GROWTH_POINT при ST_LOWER",
        "\n0",
        group_0_low["LOWER_LINE_LENGTH"].mean(),
        "\n1",
        group_1_low["LOWER_LINE_LENGTH"].mean(),
        "\nМедианы:",
        "\n0",
        group_0_low["LOWER_LINE_LENGTH"].median(),
        "\n1",
        group_1_low["LOWER_LINE_LENGTH"].median(),
    )
    print(
        "Средние значения DIFF_PC_HIGH_AND_LOWER для GROWTH_POINT при ST_LOWER",
        "\n0",
        group_0_low["DIFF_PC_HIGH_AND_LOWER"].mean(),
        "\n1",
        group_1_low["DIFF_PC_HIGH_AND_LOWER"].mean(),
        "\nМедианы:",
        "\n0",
        group_0_low["DIFF_PC_HIGH_AND_LOWER"].median(),
        "\n1",
        group_1_low["DIFF_PC_HIGH_AND_LOWER"].median(),
    )
    print(
        "Средние значения DIFF_PC_LOW_AND_LOWER для GROWTH_POINT при ST_LOWER",
        "\n0",
        group_0_low["DIFF_PC_LOW_AND_LOWER"].mean(),
        "\n1",
        group_1_low["DIFF_PC_LOW_AND_LOWER"].mean(),
        "\nМедианы:",
        "\n0",
        group_0_low["DIFF_PC_LOW_AND_LOWER"].median(),
        "\n1",
        group_1_low["DIFF_PC_LOW_AND_LOWER"].median(),
    )
    print(
        "Средние значения DIFF_PC_HIGH_AND_PC_LOW для GROWTH_POINT при ST_LOWER",
        "\n0",
        group_0_low["DIFF_PC_HIGH_AND_PC_LOW"].mean(),
        "\n1",
        group_1_low["DIFF_PC_HIGH_AND_PC_LOW"].mean(),
        "\nМедианы:",
        "\n0",
        group_0_low["DIFF_PC_HIGH_AND_PC_LOW"].median(),
        "\n1",
        group_1_low["DIFF_PC_HIGH_AND_PC_LOW"].median(),
    )
    print(
        "Средние значения VOLUME для GROWTH_POINT при ST_LOWER",
        "\n0",
        group_0_low["VOLUME"].mean(),
        "\n1",
        group_1_low["VOLUME"].mean(),
        "\nМедианы:",
        "\n0",
        group_0_low["VOLUME"].median(),
        "\n1",
        group_1_low["VOLUME"].median(),
    )

    group_0 = group_0_low["VOLUME"]
    group_1 = group_1_low["VOLUME"]
    # Пример для 'VOLUME'
    stat, p_value = mannwhitneyu(group_0, group_1)
    print(f"stat = {stat:.5f}, p-value = {p_value:.10f}")

    mad = median_abs_deviation(np.concatenate([group_0, group_1]))
    effect_size = (np.median(group_1) - np.median(group_0)) / mad
    print(f"Размер эффекта = {effect_size:.3f}")

    def median_ci(x):
        return np.median(x)

    ci_0 = bootstrap((group_0,), median_ci, method="percentile").confidence_interval
    ci_1 = bootstrap((group_1,), median_ci, method="percentile").confidence_interval
    print(
        f"Медиана группы 0: {np.median(group_0):.0f} [95% CI: {ci_0.low:.0f}, {ci_0.high:.0f}]"
    )
    print(
        f"Медиана группы 1: {np.median(group_1):.0f} [95% CI: {ci_1.low:.0f}, {ci_1.high:.0f}]"
    )

    sns.boxplot(x="GROWTH_POINT", y="VOLUME", data=df, showfliers=False)
    plt.yscale("log")  # Логарифмическая шкала
    plt.title("Распределение VOLUME по группам (без выбросов)")
    plt.show()

    # # Проводим t-тест
    # result = ttest_ind(group_0, group_1)
    # print(result)  # TtestResult(statistic=-8.0, pvalue=0.0002, df=6)

    # Удаляем ненужные столбцы
    df.drop(
        columns=[
            "TICKER",
            "DATE",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "PC_30_HIGH",
            "PC_30_LOW",
            "PC_30_MID",
            "ST_LOWER_30_7",
            "ST_UPPER_30_7",
            "BUY_PRICE",
            "PREV_OPEN",
            "PREV_CLOSE",
            "PREV_HIGH",
            "PREV_LOW",
        ],
        inplace=True,
    )

    # Явное преобразование типов
    # df["VOLUME"] = pd.to_numeric(df["VOLUME"], errors="coerce")
    df.fillna(0, inplace=True)

    df.to_csv("features.csv", index=False)
    # data = df.dropna()

    # data.to_csv("features.csv", index=False)

    # Вычисляем корреляцию
    # corr_matrix = data.corr(numeric_only=True)

    # Убедимся, что корреляции являются числами
    # growth_corr = corr_matrix["GROWTH_POINT"].astype(float).sort_values(ascending=False)

    # print("Корреляция с GROWTH_POINT:")
    # print(growth_corr)

    # # Визуализация - используем явный бар-плот
    # plt.figure(figsize=(10, 6))

    # # Удаляем целевую переменную из списка признаков
    # if "GROWTH_POINT" in growth_corr.index:
    #     features = growth_corr.index.drop("GROWTH_POINT")
    #     values = growth_corr.drop("GROWTH_POINT").values
    # else:
    #     features = growth_corr.index
    #     values = growth_corr.values

    # # Проверяем, что все значения числовые
    # if any(not isinstance(v, (int, float)) for v in values):
    #     print("Обнаружены нечисловые значения в корреляциях:")
    #     print(values)
    #     raise TypeError("Корреляции содержат нечисловые значения")

    # # Создаем бар-плот вручную
    # plt.bar(features, values, color="skyblue")
    # plt.title("Корреляция признаков с GROWTH_POINT")
    # plt.xticks(rotation=45)
    # plt.axhline(y=0, color="gray", linestyle="--")
    # plt.tight_layout()
    # plt.show()

    # quotes.drop(columns=["GROWTH_POINT"], inplace=True)
    return quotes
