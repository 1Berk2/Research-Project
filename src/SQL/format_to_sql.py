from Helpers import *

def to_sql_stocks(data: list) -> dict:
    """
    Format the data into a list of stock names.

    Parameters:
    data (list): The data to format, expected to contain 'name'.

    Returns:
    list: The list of stock names.
    """
    return ', '.join([str(stock) for stock in data])

def to_sql_stock_ret(df: pd.DataFrame) -> str:
    """
    Transforms a pivoted DataFrame into a string of VALUES suitable for SQL insertion.

    Parameters:
    df (pd.DataFrame): The DataFrame to transform. Assumes 'date' as the index and stock IDs as column headers.
    col_name (str): The name of the column to insert.
    
    Returns:
    str: The string of VALUES for SQL insertion.
    """
    df = df.reset_index()
    melted_df = df.melt(id_vars=['date'], var_name='numid', value_name='pct_return')
    melted_df['numid'] = melted_df['numid'].astype(int)
    melted_df['pct_return'] = melted_df['pct_return'].apply(lambda x: 'NULL' if pd.isna(x) else str(x))
    melted_df['date'] = melted_df['date'].dt.strftime('%Y-%m-%d')

    values_str = ', '.join([f"('{row['date']}', {row['numid']}, {row['pct_return']})" for idx, row in melted_df.iterrows()])
    return values_str

def to_sql_stock_factor(df: pd.DataFrame) -> str:
    """
    Transforms a DataFrame into a string of VALUES suitable for SQL insertion.

    Parameters:
    df (pd.DataFrame): The DataFrame to transform. Assumes 'year' as a column and 'numid', 'factor' as other columns.

    Returns:
    str: The string of VALUES for SQL insertion.
    """
    melted_df = df.astype({'numid': int, 'factor': float})
    melted_df['factor'] = melted_df['factor'].apply(lambda x: 'NULL' if pd.isna(x) else str(x))    
    melted_df['year'] = melted_df['year'].astype(int)

    values_str = ', '.join([f"({row['year']}, {row['numid']}, {row['factor']})" for idx, row in melted_df.iterrows()])
    return values_str

def to_sql_deciles(df: pd.DataFrame) -> str:
    """
    Transforms a DataFrame into a string of VALUES suitable for SQL insertion.

    Parameters:
    df (pd.DataFrame): The DataFrame to transform. Assumes 'year' as a column and 'decile' as another column.

    Returns:
    str: The string of VALUES for SQL insertion.
    """
    melted_df = df.astype({'year': int, 'numid': int, 'decile': int})
    
    values_str = ', '.join([f"({row['year']}, {row['numid']}, {row['decile']})" for idx, row in melted_df.iterrows()])
    return values_str

def to_sql_decile_returns(df: pd.DataFrame) -> str:
    """
    Transforms a DataFrame into a string of VALUES suitable for SQL insertion.
    Assumes the DataFrame index is 'date' and columns are deciles.

    Parameters:
    df (pd.DataFrame): The DataFrame to transform.

    Returns:
    str: The string of VALUES for SQL insertion.
    """
    df = df.reset_index()
    melted_df = df.melt(id_vars=['date'], var_name='decile', value_name='pct_return')
    melted_df['decile'] = melted_df['decile'].apply(lambda x: int(x) if isinstance(x, str) and x.isdigit() else (int(x) if isinstance(x, int) else 0))
    melted_df['pct_return'] = melted_df['pct_return'].apply(lambda x: 'NULL' if pd.isna(x) else str(x))
    melted_df['date'] = melted_df['date'].dt.strftime('%Y-%m-%d')

    values_str = ', '.join([f"('{row['date']}', {row['decile']}, {row['pct_return']})" for _, row in melted_df.iterrows()])
    return values_str

