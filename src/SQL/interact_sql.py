from Helpers import *

def connect_to_mysql():
    """
    Connect to the MySQL server.

    Returns:
    mysql.connector.connection.MySQLConnection: Connection to the MySQL server.
    """
    config = SQL_CONFIG
    try:
        cnx = mysql.connector.connect(**config)
        return cnx

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None


def fetch_data(query: str):
    """
    Fetch data from the MySQL server.

    Args:
    query (str): The query to execute.

    Returns:
    list of dict: The data fetched from the MySQL server. (unformatted data)
    """
    try:
        cnx = connect_to_mysql()
        cursor = cnx.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error fetching data from MySQL server: {err}")
        return None
    return data


def write_data(query: str):
    """
    Write data to the MySQL server.

    Args:
    query (str): The query to execute.

    Returns:
    bool: True if the data was successfully written, False otherwise.
    """
    try:
        cnx = connect_to_mysql()
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error writing data to MySQL server: {err}")
        return False
    return True