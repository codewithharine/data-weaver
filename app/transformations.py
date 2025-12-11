import pandas as pd

def merge_crypto_and_quakes(
    btc_df: pd.DataFrame, eq_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Join Bitcoin and earthquake data on date.
    """
    merged = pd.merge(btc_df, eq_df, on="date", how="left").fillna(
        {"eq_count": 0, "avg_mag": 0}
    )
    return merged


def compute_correlations(df: pd.DataFrame):
    """
    Compute simple correlations between BTC price and earthquake metrics.
    """
    corr_price_count = df["price_usd"].corr(df["eq_count"]) if "eq_count" in df else None
    corr_price_mag = df["price_usd"].corr(df["avg_mag"]) if "avg_mag" in df else None
    return corr_price_count, corr_price_mag
