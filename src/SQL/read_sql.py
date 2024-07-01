from Helpers import *
from .interact_sql import *
from .format_from_sql import *
from .format_to_sql import *

def fetch_first_date_year(year: int, db: str) -> str:
    """
    Get the first date of the year from the specified database.
    
    Parameters:
    year (int): The year for which to retrieve the data.
    db (str): The database from which to retrieve the data.
    
    Returns:
    list of dict: The first date of the year from the specified database.
    """
    query = f"""
        SELECT
            MIN(date) AS start_date
        FROM
            {DB_READ}.{db}
        WHERE
            YEAR(date) = {year}
    """
    data = fetch_data(query)
    formatted_data = from_sql_first_date(data)

    return formatted_data 


def fetch_numids_jan(first_date: str, db: str) -> list:
    """
    Get the number of unique ids in January of a given year.

    Parameters:
    first_date (str): The first date of the year.
    db (str): The database from which to retrieve the data.

    Returns:
    list of dict: The number of unique ids in January of a given year.
    """
    query = f"""
        SELECT
            DISTINCT numid
        FROM
            {DB_READ}.{db}
        WHERE
            date = '{first_date}'
    """
    data = fetch_data(query)
    formatted_data = from_sql_numids(data)

    return formatted_data
    
def fetch_stock_ret_index(stocks: list, start_date: str, end_date: str, db: str) -> pd.DataFrame:
    """
    Get the stock return index for given stocks.

    Parameters:
    stocks (list): The stocks for which to retrieve the data.
    start_date (str): The start date of the data.
    end_date (str): The end date of the data.
    db (str): The database from which to retrieve the data.

    Returns:
    pd.DataFrame: The stock return index for the given stocks.
    """
    stocks_sql_format = to_sql_stocks(stocks)
    query = f"""
        SELECT
            date, 
            numid,
            RI
        FROM
            {DB_READ}.{db}
        WHERE
            numid IN ({stocks_sql_format})
            AND date BETWEEN '{start_date}' AND '{end_date}'
    """
    data = fetch_data(query)
    formatted_data = from_sql_ret_index(data)

    return formatted_data

def fetch_stock_ret_pct(start_date: str, end_date: str, db: str) -> pd.DataFrame:
    """
    Get the stock return percentage for each stock.

    Parameters:
    start_date (str): The start date of the data.
    end_date (str): The end date of the data.
    db (str): The database from which to retrieve the data.

    Returns:
    pd.DataFrame: The stock return percentage for each stock.
    """
    query = f"""
        SELECT
            date, 
            numid,
            pct_ret
        FROM
            {DB_WRITE}.{db}
        WHERE
            date BETWEEN '{start_date}' AND '{end_date}'
    """
    data = fetch_data(query)
    formatted_data = from_sql_ret_pct(data)

    return formatted_data

def fetch_factor_values(year: int, db_factor: str) -> pd.DataFrame:
    """
    Get the factor values for a given year.

    Parameters:
    year (int): The year for which to retrieve the data.
    db_factor (str): The database from which to retrieve the data.

    Returns:
    pd.DataFrame: The factor values for the given year.
    """
    query = f"""
        SELECT
            year,
            numid,
            factor
        FROM
            {DB_WRITE}.{db_factor}
        WHERE
            year = {year}
    """
    data = fetch_data(query)
    formatted_data = from_sql_factor_values(data)

    return formatted_data

def fetch_deciles(year: int, db_deciles: str) -> pd.DataFrame:
    """
    Get the deciles for a given year.
    
    Parameters:
    year (int): The year for which to retrieve the data.
    db_deciles (str): The database from which to retrieve the data.
    
    Returns:
    pd.DataFrame: The deciles for the given year.
    """
    query = f"""
        SELECT
            year,
            numid,
            decile
        FROM
            {DB_WRITE}.{db_deciles}
        WHERE
            year = {year}
    """
    data = fetch_data(query)
    formatted_data = from_sql_deciles(data)

    return formatted_data

def fetch_decile_returns(start_year: int, end_year: int, db_decile_returns: str, freq: str) -> pd.DataFrame:
    """
    Get the decile returns for a given range of years.

    Parameters:
    start_year (int): The start year for which to retrieve the data.
    end_year (int): The end year for which to retrieve the data.
    db_decile_returns (str): The database from which to retrieve the data.

    Returns:
    pd.DataFrame: The decile returns for the given range of years.
    """
    query = f"""
        SELECT
            date,
            decile,
            pct_ret
        FROM
            {DB_WRITE}.{db_decile_returns}
        WHERE
            year(date) BETWEEN {start_year} AND {end_year}
    """
    data = fetch_data(query)
    formatted_data = from_sql_decile_returns(data, freq)

    return formatted_data

def fetch_sp_returns(start_year: int, end_year: int, db_sp_returns: str, freq: str) -> pd.DataFrame:
    """
    Get the S&P 500 returns for a given range of years.

    Parameters:
    start_year (int): The start year for which to retrieve the data.
    end_year (int): The end year for which to retrieve the data.
    db_sp_returns (str): The database from which to retrieve the data.

    Returns:
    pd.DataFrame: The S&P 500 returns for the given range of years.
    """
    query = f"""
        SELECT
            date,
            SPCOMPRI_RET
        FROM
            {DB_READ}.{db_sp_returns}
        WHERE
            year(date) BETWEEN {start_year} AND {end_year}
    """
    data = fetch_data(query)
    formatted_data = from_sql_sp_returns(data, freq)

    return formatted_data

def fetch_accounting_data(column_name: str, db_accounting: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Get the accounting data for a given stock.

    Parameters:
    numid (int): The stock for which to retrieve the data.
    column_name (str): The column name for the data.
    start_date (str): The start date for the data.
    end_date (str): The end date for the data.

    Returns:
    pd.DataFrame: The accounting data for the given stock.
    """
    query = f"""
        SELECT
            DATADATE,
            numid,
            {column_name}
        FROM
            {DB_READ}.{db_accounting}
        WHERE
            DATADATE BETWEEN '{start_date}' AND '{end_date}'
    """
    data = fetch_data(query)
    formatted_data = from_sql_accounting_data(data)

    return formatted_data

def fetch_market_price(db_returns: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Get the market price for a given stock.

    Parameters:
    numid (int): The stock for which to retrieve the data.
    start_date (str): The start date for the data.
    end_date (str): The end date for the data.

    Returns:
    pd.DataFrame: The market price for the given stock.
    """
    query = f"""
        SELECT
            date,
            numid,
            UP
        FROM
            {DB_READ}.{db_returns}
        WHERE
            date BETWEEN '{start_date}' AND '{end_date}'
    """
    data = fetch_data(query)
    formatted_data = from_sql_market_price(data)

    return formatted_data