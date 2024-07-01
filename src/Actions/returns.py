from Helpers import *
from SQL import *

def calc_returns(start_year: int, end_year: int, freq: str) -> bool:
    """
    Calculate the returns of all stock in the database from start_year to end_year
    
    Parameters:
    start_year (int): The start year of the calculation
    end_year (int): The end year of the calculation
    
    Returns:
    bool: True if the calculation is successful, False otherwise
    """

    if freq not in ['d', 'm']:
        print('Invalid frequency, try d or m')
        return False
    
    year_list = list(range(start_year-1, end_year+1))
    db_tickers, db_returns, db_insert = f'{DB_SP_NUMIDS}', f'{DB_RI_PREFIX}{freq}', f'{DB_PCT_RETURN_PREFIX}{freq}'

    for index, year in enumerate(year_list):
        start_date, end_date = f'{year-1}-11-31', f'{year}-12-31'
        first_date_year = fetch_first_date_year(year, db_tickers)
        stocks_january = fetch_numids_jan(first_date_year, db_tickers)
    
        ret_index_df = fetch_stock_ret_index(stocks_january, start_date, end_date, db_returns)
        ret_pct_df = ret_index_df.pct_change(fill_method=None)
        ret_pct_df = ret_pct_df.dropna(axis=1, how='all')
        insert_stock_ret_pct(ret_pct_df, db_insert)

        progress = f"Progress: {index+1}/{len(year_list)} years completed for {freq} frequency."
        sys.stdout.write("\r" + progress)
        sys.stdout.flush()
    print()
    return True