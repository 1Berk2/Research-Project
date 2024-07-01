from Helpers import *
from SQL import *

def get_num_stocks_decile(start: int, end: int, factor: str) -> pd.DataFrame:
    """
    Get the number of individual stocks within each decile.

    Parameters:
    factor (str): The factor for which to get the number of stocks.

    Returns:
    pd.DataFrame: The number of individual stocks within each decile.
    """
    db_deciles = f'{DB_DECILES_PREFIX}{factor}'
    year_list = list(range(start, end))

    num_stocks_list = []
    for year in year_list:
        deciles_df = fetch_deciles(year, db_deciles)

        num_stocks = deciles_df.groupby('decile').size().reset_index(name='num_stocks')
        num_stocks['year'] = year
        num_stocks_list.append(num_stocks)

    # Concatenate all data frames in the list into a single data frame
    num_stocks_df = pd.concat(num_stocks_list, ignore_index=True)

    # reformat df so that the years are the columns and the deciles are the index with the number of stocks as the values
    num_stocks_df = num_stocks_df.pivot(index='decile', columns='year', values='num_stocks')

    return num_stocks_df
