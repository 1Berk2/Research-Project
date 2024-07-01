from Helpers import *
from SQL import *

def get_extreme_factor_values_decile(start: int, end: int, factor: str) -> pd.DataFrame:
    """
    Calculate the highest and lowest factor values for each decile for each year.

    Parameters:
    start (int): The start year.
    end (int): The end year.
    factor (str): The factor name.

    Returns:
    pd.DataFrame: A DataFrame with rows as deciles (low and high) and columns as years.
    """
    db_deciles = f'{DB_DECILES_PREFIX}{factor}'
    db_factor = f'{DB_FACTOR_PREFIX}{factor}'

    year_list = list(range(start, end + 1))  # Ensure it includes the end year

    # Dictionary to store high and low values for each decile and year
    decile_dict = {('low', decile): [] for decile in range(0, 10)}
    decile_dict.update({('high', decile): [] for decile in range(0, 10)})

    for year in year_list:
        deciles_df = fetch_deciles(year, db_deciles)
        factor_df = fetch_factor_values(year-1, db_factor)

        merged_df = pd.merge(deciles_df, factor_df, on='numid', how='inner')

        for decile in range(0, 10):
            decile_data = merged_df[merged_df['decile'] == decile]
            high_value = decile_data['factor'].max()
            low_value = decile_data['factor'].min()
            
            decile_dict[('low', decile)].append(low_value)
            decile_dict[('high', decile)].append(high_value)

    # Creating a DataFrame from the dictionary
    rows = []
    for decile in range(0, 10):
        rows.append([round(decile), 'low'] + decile_dict[('low', decile)])
        rows.append([round(decile), 'high'] + decile_dict[('high', decile)])

    columns = ['Decile', 'Type'] + year_list
    factor_values_df = pd.DataFrame(rows, columns=columns)

    factor_values_df = factor_values_df.round(4)

    return factor_values_df

def print_extreme_factor_values_decile(start: int, end: int, factor: str):
    """
    Print the highest and lowest factor values for each decile for each year.

    Parameters:
    start (int): The start year.
    end (int): The end year.
    factor (str): The factor name.
    """
    extreme_factor_values_decile = get_extreme_factor_values_decile(start, end, factor)
    extreme_factor_values_decile_str = extreme_factor_values_decile.to_string(index=False)
    print(f'Highest and Lowest factor values for each decile:\n{extreme_factor_values_decile_str}', end='\n\n')
