from Helpers import *

def get_avrg_monthly_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the geometric mean of monthly returns for each decile.

    Parameters:
    df (pd.DataFrame): The dataframe containing the decile returns.

    Returns:
    pd.DataFrame: The geometric mean monthly return for each decile.
    """
    df = df.dropna()
    
    # Convert returns to logarithmic returns
    log_returns = np.log1p(df)

    # Calculate the mean of logarithmic returns
    mean_log_returns = log_returns.mean()

    # Convert back to normal returns
    geom_mean_returns = np.expm1(mean_log_returns)

    geom_mean_returns = geom_mean_returns.reset_index()
    geom_mean_returns.columns = ['decile', 'avrg_ret']
    
    return geom_mean_returns