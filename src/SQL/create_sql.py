from Helpers import *
from .interact_sql import *

def create_table_stock_ret(db: str) -> None:
    """
    Create a table for stock return percentage data in the specified database.

    Parameters:
    db (str): The database in which to create the table.

    Returns:
    None
    """
    query = f"""
        CREATE TABLE IF NOT EXISTS s4a_data_intern.{db} (
            date DATE,
            numid INT,
            pct_ret FLOAT
        )
    """
    return write_data(query)

def create_table_stock_factor(db: str) -> None:
    """
    Create a table for stock factor data in the specified database.

    Parameters:
    db (str): The database in which to create the table.

    Returns:
    None
    """
    query = f"""
        CREATE TABLE IF NOT EXISTS s4a_data_intern.{db} (
            year INT,
            numid INT,
            factor FLOAT
        )
    """
    return write_data(query)

def create_table_deciles(db: str) -> None:
    """
    Create a table for decile data in the specified database.

    Parameters:
    db (str): The database in which to create the table.

    Returns:
    None
    """
    query = f"""
        CREATE TABLE IF NOT EXISTS s4a_data_intern.{db} (
            year INT,
            numid INT,
            decile INT
        )
    """
    return write_data(query)

def create_table_decile_returns(db: str) -> None:
    """
    Create a table for decile returns data in the specified database.

    Parameters:
    db (str): The database in which to create the table.

    Returns:
    None
    """
    query = f"""
        CREATE TABLE IF NOT EXISTS s4a_data_intern.{db} (
            date DATE,
            decile INT,
            pct_ret FLOAT
        )
    """
    return write_data(query)