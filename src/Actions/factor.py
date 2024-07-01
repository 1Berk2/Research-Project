from Helpers import *
from SQL import *

def calc_factor(start_year: int, end_year: int, factor_name: str, factor_function) -> bool:
    """
    Calculate the factor values of all stock in the database from start_year to end_year
    
    Parameters:
    start_year (int): The start year of the calculation
    end_year (int): The end year of the calculation
    
    Returns:
    bool: True if the calculation is successful, False otherwise
    """

    year_list = list(range(start_year-1, end_year))
    db_insert = f'{DB_FACTOR_PREFIX}{factor_name}'

    for index, year in enumerate(year_list):
        start_date, end_date = f'{year}-01-01', f'{year}-12-31'

        factor_values_df = factor_function(start_date, end_date)
        factor_values_df['year'] = year
        insert_stock_factor(factor_values_df, db_insert)
        

        progress = f"Progress: {index+1}/{len(year_list)} years completed for {factor_name} factor."
        sys.stdout.write("\r" + progress)
        sys.stdout.flush()
    print()
    return True