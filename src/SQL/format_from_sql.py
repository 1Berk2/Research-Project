from Helpers import *

def from_sql_first_date(data: list) -> dict:
    """
    Format the first object of the data list.
    
    Parameters:
    data (list): The data to format.
    
    Returns:
    str: The first object in list of dict.
    """
    return data[0][0].strftime('%Y-%m-%d')

def from_sql_numids(data: list) -> dict:
    """
    Format the first object of the data list.
    
    Parameters:
    data (list): The data to format.
    
    Returns:
    list: The list of numids.
    """
    return [numid for numid, in data] 

import pandas as pd

def from_sql_ret_index(data: list) -> pd.DataFrame:
    """
    Format the data into a pandas DataFrame with dates as rows and stocks as columns.

    Parameters:
    data (list): The data to format, expected to contain 'date', 'numid', and 'RI' (Return Index).

    Returns:
    pd.DataFrame: The formatted data where each column represents a different stock's return index.
    """
    if not data:
        return pd.DataFrame()
    try:
        df = pd.DataFrame(data, columns=['date', 'numid', 'RI'])
    except AssertionError as e:
        print(f"Error in data format: {e}")
        return pd.DataFrame()

    df['date'] = pd.to_datetime(df['date'])
    df_pivoted = df.pivot(index='date', columns='numid', values='RI')
    df_pivoted.columns = [int(col) for col in df_pivoted.columns]

    return df_pivoted


def from_sql_ret_pct(data: list) -> pd.DataFrame:
    """
    Format the data into a pandas DataFrame with dates as rows and stocks as columns.

    Parameters:
    data (list): The data to format, expected to contain 'date', 'numid', and 'pct_ret' (Return Percentage).

    Returns:
    pd.DataFrame: The formatted data where each column represents a different stock's return percentage.
    """
    if not data:
        return pd.DataFrame()
    try:
        df = pd.DataFrame(data, columns=['date', 'numid', 'pct_ret'])
    except AssertionError as e:
        print(f"Error in data format: {e}")
        return pd.DataFrame()

    df['date'] = pd.to_datetime(df['date'])
    df = df.drop_duplicates(subset=['date', 'numid'])
    df_pivoted = df.pivot(index='date', columns='numid', values='pct_ret')
    df_pivoted.columns = [int(col) for col in df_pivoted.columns]

    return df_pivoted

def from_sql_factor_values(data: list) -> pd.DataFrame:
    """
    Format the data into a pandas DataFrame with years as rows and stocks as columns.

    Parameters:
    data (list): The data to format, expected to contain 'year', 'numid', and 'factor'.

    Returns:
    pd.DataFrame: The formatted data where each column represents a different stock's factor value.
    """
    if not data:
        return pd.DataFrame()
    try:
        df = pd.DataFrame(data, columns=['year', 'numid', 'factor'])
    except AssertionError as e:
        print(f"Error in data format: {e}")
        return pd.DataFrame()

    return df

def from_sql_deciles(data: list) -> pd.DataFrame:
    """
    Format the data into a pandas DataFrame with years as rows and stocks as columns.

    Parameters:
    data (list): The data to format, expected to contain 'year', 'numid', and 'decile'.

    Returns:
    pd.DataFrame: The formatted data where each column represents a different stock's decile value.
    """
    if not data:
        return pd.DataFrame()
    try:
        df = pd.DataFrame(data, columns=['year', 'numid', 'decile'])
    except AssertionError as e:
        print(f"Error in data format: {e}")
        return pd.DataFrame()

    return df

def from_sql_decile_returns(data: list, freq: str) -> pd.DataFrame:
    """
    Format the data into a pandas DataFrame with years as rows and deciles as columns.

    Parameters:
    data (list): The data to format, expected to contain 'year', 'decile', and 'ret'.

    Returns:
    pd.DataFrame: The formatted data where each column represents a different decile's return.
    """
    if not data:
        return pd.DataFrame()
    try:
        df = pd.DataFrame(data, columns=['date', 'decile', 'pct_ret'])
        if freq == 'm':
            df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
        elif freq == 'd':
            df['date'] = pd.to_datetime(df['date'])
        df = df.pivot(index='date', columns='decile', values='pct_ret')
    except Exception as e:
        print(f"Error in data format: {e}")
        return pd.DataFrame()

    return df

def from_sql_sp_returns(data: list, freq:str) -> pd.DataFrame:
    """
    Format the data into a pandas DataFrame with dates as rows and the S&P 500 return as a column.

    Parameters:
    data (list): The data to format, expected to contain 'date' and 'pct_ret'.

    Returns:
    pd.DataFrame: The formatted data where each row represents a different date and the column is the S&P 500 return.
    """
    if not data:
        return pd.DataFrame()
    try:
        df = pd.DataFrame(data, columns=['date', 'pct_ret'])
        if freq == 'm':
            df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
        elif freq == 'd':
            df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
    except Exception as e:
        print(f"Error in data format: {e}")
        return pd.DataFrame()

    return df

def from_sql_accounting_data(data: list) -> pd.DataFrame:
    """
    Format the data into a pandas DataFrame with dates as rows and the accounting data as columns.

    Parameters:
    data (list): The data to format, expected to contain 'date', 'numid', and 'column_name'.

    Returns:
    pd.DataFrame: The formatted data where each row represents a different date and the columns are the accounting data for each numid.
    """
    if not data:
        return pd.DataFrame()

    try:
        df = pd.DataFrame(data, columns=['date', 'numid', 'accounting_data'])
        df['date'] = pd.to_datetime(df['date'])
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['date', 'numid'])
        
        # Pivot the DataFrame
        df = df.pivot(index='date', columns='numid', values='accounting_data')
        
    except Exception as e:
        print(f"Error in data format: {e}")
        return pd.DataFrame()

    return df

def from_sql_market_price(data: list) -> pd.DataFrame:
    """
    Format the data into a pandas DataFrame with dates as rows and the market price as a column.

    Parameters:
    data (list): The data to format, expected to contain 'date', 'numid', and 'market_price'.

    Returns:
    pd.DataFrame: The formatted data where each row represents a different date and the column is the market price.
    """
    if not data:
        return pd.DataFrame()
    try:
        df = pd.DataFrame(data, columns=['date', 'numid', 'market_price'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.pivot(index='date', columns='numid', values='market_price')
    except Exception as e:
        print(f"Error in data format: {e}")
        return pd.DataFrame()

    return df