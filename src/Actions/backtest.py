from Helpers import *
from Tests import *
from SQL import *

def calc_backtest(start_year: int, end_year: int, factor: str) -> None:
    db_sp_monthly = f'{DB_SP_RETURNS_PREFIX}m'
    db_sp_daily = f'{DB_SP_RETURNS_PREFIX}d'
    db_decile_returns_daily = f"{DB_DECILE_RETURNS_PREFIX}{factor}d"
    db_decile_returns_monthly = f"{DB_DECILE_RETURNS_PREFIX}{factor}m"

    # Fetch S&P returns for daily and monthly frequencies
    sp_returns_df_daily = fetch_sp_returns(start_year, end_year, db_sp_daily, 'd')
    sp_returns_df_monthly = fetch_sp_returns(start_year, end_year, db_sp_monthly, 'm')
    sp_returns_df_daily.columns = ['sp500']
    sp_returns_df_monthly.columns = ['sp500']

    # Fetch decile returns for daily and monthly frequencies
    daily_decile_returns_df = fetch_decile_returns(start_year, end_year, db_decile_returns_daily, 'd')
    monthly_decile_returns_df = fetch_decile_returns(start_year, end_year, db_decile_returns_monthly, 'm')

    # Join S&P and decile returns
    backtest_df_daily = sp_returns_df_daily.join(daily_decile_returns_df, how='inner')
    backtest_df_monthly = sp_returns_df_monthly.join(monthly_decile_returns_df, how='inner')

    # Calculate and plot average monthly returns
    avrg_monthly_returns = get_avrg_monthly_return(monthly_decile_returns_df)
    plot_avrg_monthly_returns(avrg_monthly_returns, factor)

    # Calculate and plot cumulative returns
    daily_cum_returns = get_cumulative_returns(backtest_df_daily)
    daily_cum_returns.index = pd.to_datetime(daily_cum_returns.index)
    plot_cumulative_returns(daily_cum_returns, factor)

    monthly_cum_returns = get_cumulative_returns(backtest_df_monthly)
    monthly_cum_returns.index = pd.to_datetime(monthly_cum_returns.index.strftime('%Y-%m'))
    plot_cumulative_returns(monthly_cum_returns, factor)

    # Calculate and plot average annual returns
    annual_returns_backtest = get_avrg_annual_returns(backtest_df_monthly)
    plot_avrg_annual_returns(annual_returns_backtest, 'low', factor)
    plot_avrg_annual_returns(annual_returns_backtest, 'high', factor)

    # Plot joint probability density function
    plot_joint_pdf(backtest_df_daily, factor)

    # get first and last date from the df in terms of year as an int
    start, end = backtest_df_daily.index.year.min(), backtest_df_daily.index.year.max()

    # Descriptive statistics
    print("Descriptive statistics for the daily backtest dataframe:")
    print("-"*55)
    num_rows = backtest_df_daily.shape[0]
    print(f'Number of rows in the dataframe: {num_rows}')
    print(f"Number of rows in a year: {round(num_rows / (end - start + 1))}\n")
    # get first and last date in the df
    first_date = backtest_df_daily.index[0].strftime('%Y-%m-%d')
    last_date = backtest_df_daily.index[-1].strftime('%Y-%m-%d')
    print(f'First date in the dataframe: {first_date}')
    print(f'Last date in the dataframe: {last_date}')
    print("-"*55, end='\n\n')

    print("Average returns and number of portfolios in each decile:")
    print("-"*150)
    # get number of individual stocks within each decile
    num_stocks = get_num_stocks_decile(start, end, factor)
    # format this nicely to print
    num_stocks = num_stocks.to_string()
    print(f'Number of stocks in each decile:\n{num_stocks}', end='\n\n')

    print_extreme_factor_values_decile(start, end, factor)
    print("-"*150, end='\n\n')


