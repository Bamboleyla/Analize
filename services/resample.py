import pandas as pd


def resample_quotes(quotes: pd.DataFrame, timeframe: str = "1h") -> pd.DataFrame:
    """
    Resample OHLCV quotes to a specified timeframe (e.g. '1h' for 1 hour).
    """
    df = quotes.copy()
    df["dt"] = pd.to_datetime(df["DATE"])
    df = df.set_index("dt")
    resampled = (
        df.resample(timeframe)
        .agg(
            {
                "TICKER": "first",
                "OPEN": "first",
                "HIGH": "max",
                "LOW": "min",
                "CLOSE": "last",
                "VOLUME": "sum",
            }
        )
        .dropna(subset=["OPEN", "CLOSE", "HIGH", "LOW"])
        .reset_index()
    )
    resampled["DATE"] = resampled["dt"].dt.strftime("%Y%m%d %H:%M:%S")
    resampled = resampled.drop(columns=["dt"])
    return resampled
