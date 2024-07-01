from Helpers import *
from SQL import *

def beta_factor(start_date: str, end_date: str) -> pd.DataFrame:
    db_sp_daily, db_ret_daily = f'{DB_SP_RETURNS_PREFIX}d', f'{DB_PCT_RETURN_PREFIX}d'
    start_year, end_year = int(start_date[:4]), int(end_date[:4])

    sp_returns_df = fetch_sp_returns(start_year, end_year, db_sp_daily, 'd')
    ret_pct_df = fetch_stock_ret_pct(start_date, end_date, db_ret_daily)
    ret_pct_df = ret_pct_df.dropna(thresh=200, axis=1)

    sp_returns_df.columns = ['sp500']
    # Ensure proper alignment by date when joining dataframes
    ret_pct_df = ret_pct_df.join(sp_returns_df, how='inner')


    beta_data = []
    # Correcting formula to compute beta: covariance divided by variance of the market (S&P 500)
    for numid in ret_pct_df.columns[:-1]:  # Exclude the last column which is S&P 500
        stock = ret_pct_df[numid]
        market = ret_pct_df['sp500']
        covariance = stock.cov(market)
        market_variance = market.var()
        if market_variance != 0:  # To prevent division by zero
            beta = covariance / market_variance
        else:
            beta = None  # Assign None or suitable value if market variance is zero
        beta_data.append({'numid': numid, 'factor': beta})

    beta_df = pd.DataFrame(beta_data)
    
    return beta_df
