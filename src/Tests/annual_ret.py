from Helpers import *

def get_avrg_annual_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the average annual return for each decile.

    Parameters:
    df (pd.DataFrame): The dataframe containing the decile returns.

    Returns:
    pd.DataFrame: The average annual return for each decile.
    """
    
    start, end = df.index.year.min(), df.index.year.max()
    monthly_returns_df = df.copy()
    monthly_returns_df = monthly_returns_df[(monthly_returns_df.index.year >= start) & (monthly_returns_df.index.year <= end)]
    
    annual_returns = monthly_returns_df.groupby(monthly_returns_df.index.year).apply(lambda x: (1 + x).prod() - 1)
    
    return annual_returns