from Helpers import *
from .interact_sql import *
from .format_from_sql import *
from .format_to_sql import *
from .create_sql import *

def insert_stock_ret_pct(data: pd.DataFrame, db: str) -> None:
    """
    Insert stock return percentage data into the specified database.

    Parameters:
    data (pd.DataFrame): The data to insert.
    db (str): The database into which to insert the data.

    Returns:
    None
    """
    create_table_stock_ret(db)
    
    formatted_data = to_sql_stock_ret(data)
    query = f"""
        INSERT INTO s4a_data_intern.{db} (date, numid, pct_ret)
        VALUES {formatted_data}
    """
    return write_data(query)

def insert_stock_factor(data: pd.DataFrame, db: str) -> None:
    """
    Insert stock factor data into the specified database.

    Parameters:
    data (pd.DataFrame): The data to insert.
    db (str): The database into which to insert the data.

    Returns:
    None
    """
    create_table_stock_factor(db)

    formatted_data = to_sql_stock_factor(data)
    query = f"""
        INSERT INTO s4a_data_intern.{db} (year, numid, factor)
        VALUES {formatted_data}
    """
    return write_data(query)

def insert_deciles(data: pd.DataFrame, db: str) -> None:
    """
    Insert decile data into the specified database.

    Parameters:
    data (pd.DataFrame): The data to insert.
    db (str): The database into which to insert the data.

    Returns:
    None
    """
    create_table_deciles(db)

    formatted_data = to_sql_deciles(data)
    query = f"""
        INSERT INTO s4a_data_intern.{db} (year, numid, decile)
        VALUES {formatted_data}
    """
    return write_data(query)

def insert_decile_returns(decile_returns_df: pd.DataFrame, db_insert: str) -> None:
    """
    Insert decile returns data into the specified database.

    Parameters:
    decile_returns_df (pd.DataFrame): The data to insert.
    db_insert (str): The database into which to insert the data.

    Returns:
    None
    """
    create_table_decile_returns(db_insert)

    formatted_data = to_sql_decile_returns(decile_returns_df)
    query = f"""
        INSERT INTO s4a_data_intern.{db_insert} (date, decile, pct_ret)
        VALUES {formatted_data}
    """
    return write_data(query)