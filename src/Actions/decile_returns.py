from Helpers import *
from SQL import *

def calc_decile_returns(start_year: int, end_year: int, factor_name: str) -> bool:
    """
    Calculate the decile returns of all stock in the database from start_year to end_year
    
    Parameters:
    start_year (int): The start year of the calculation
    end_year (int): The end year of the calculation
    factor_name (str): The name of the factor
    
    Returns:
    bool: True if the calculation is successful, False otherwise
    """
    for freq in ['d', 'm']:
        year_list = list(range(start_year, end_year))
        db_deciles, db_returns, db_insert = f'{DB_DECILES_PREFIX}{factor_name}', f'{DB_PCT_RETURN_PREFIX}{freq}', f'{DB_DECILE_RETURNS_PREFIX}{factor_name}{freq}'

        for index, year in enumerate(year_list):
            start_date, end_date = f'{year}-01-01', f'{year}-12-31'
            first_date_year = fetch_first_date_year(year, 'snpeom')
            deciles_df = fetch_deciles(year, db_deciles)
            ret_pct_df = fetch_stock_ret_pct(start_date, end_date, db_returns)
            ret_pct_df = ret_pct_df[deciles_df['numid'].unique()]
            ret_pct_df = ret_pct_df.fillna(0)

            decile_returns_df = pd.DataFrame()
            for decile in range(10):
                decile_stocks = deciles_df[deciles_df['decile'] == decile]['numid']
                decile_stocks = decile_stocks.tolist()
                decile_ret_df = ret_pct_df[decile_stocks]
                decile_ret_df = decile_ret_df.mean(axis=1)
                decile_returns_df[decile] = decile_ret_df
            
            insert_decile_returns(decile_returns_df, db_insert)

            progress = f"Progress: {index+1}/{len(year_list)} years completed for {factor_name} factor decile portfolio returns at frequency {freq}."
            sys.stdout.write("\r" + progress)
            sys.stdout.flush()
        print()
    return True

