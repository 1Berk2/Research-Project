from Helpers import *
from SQL import *

def volatility_factor(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Calculate the volatility factor for each stock.

    Parameters:
    start_date (str): The start date of the data.
    end_date (str): The end date of the data.

    Returns:
    pd.DataFrame: The volatility factor for each stock.
    """
    ret_pct_df = fetch_stock_ret_pct(start_date, end_date, 'pct_ret_d')
    # check for at least 200 trading days (records in the dataframe) drop the column if less
    ret_pct_df = ret_pct_df.dropna(thresh=200, axis=1)

    vol_df = ret_pct_df.std()
    vol_df = vol_df.reset_index()
    vol_df.columns = ['numid', 'factor']
    return vol_df    