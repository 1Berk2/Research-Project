from Helpers import *
from SQL import *

def calc_deciles(start_year: int, end_year: int, factor_name: str) -> bool:
    year_list = list(range(start_year, end_year))
    db_deciles, db_factor = f'{DB_DECILES_PREFIX}{factor_name}', f'{DB_FACTOR_PREFIX}{factor_name}'

    for index, year in enumerate(year_list):
        start_date, end_date = f'{year}-01-01', f'{year}-12-31'
        first_date_year = fetch_first_date_year(year, 'snpeom')

        factor_values_df = fetch_factor_values(year-1, db_factor)  # Fetching factor values for the given year
        valid_stocks = fetch_numids_jan(first_date_year, 'snpeom')
        factor_values_df = factor_values_df[factor_values_df['numid'].isin(valid_stocks)]

        # Assign deciles using qcut, ensuring each decile has an equal number of observations
        factor_values_df['decile'] = pd.qcut(factor_values_df['factor'], q=10, labels=False, duplicates='drop')

        factor_values_df = factor_values_df.drop(columns=['factor'])
        factor_values_df['year'] = year        

        insert_deciles(factor_values_df, db_deciles)

        progress = f"Progress: {index+1}/{len(year_list)} years completed for {factor_name} decile portfolios."
        sys.stdout.write("\r" + progress)
        sys.stdout.flush()
    print()
    return True
