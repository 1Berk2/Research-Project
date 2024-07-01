from Helpers import *

def get_cumulative_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the cumulative returns for each decile.

    Parameters:
    df (pd.DataFrame): The data from which to calculate the cumulative returns.

    Returns:
    pd.DataFrame: The cumulative returns for each decile.
    """
    df = df.dropna()
    df = df.drop(columns=['sp500'])
    df = df + 1
    df = df.cumprod()
    return df