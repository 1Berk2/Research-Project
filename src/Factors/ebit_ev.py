from Helpers import *
from SQL import *

def ebit_ev_factor(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Calculate the EV/EBIT ratio of returns for each numid using a more memory-efficient approach.
    
    Args:
    start_date (str): The start date for the data fetching.
    end_date (str): The end date for the data fetching.
    
    Returns:
    pd.DataFrame: The DataFrame containing EV/EBIT data for each numid.
    """

    db_accounting = f"{DB_ACCOUNTING_PREFIX}"
    db_price = f"{DB_RI_PREFIX}d"
    db_returns = f"{DB_PCT_RETURN_PREFIX}d"

    df_name_col_map = {
        'ebit': 'WC18191A',
        'num_shares': 'WC05301A',
        'current_liabilities': 'WC03101A',
        'long_term_debt': 'WC03251A',
        'preferred_stock': 'WC03451A',
        'cash_and_cash_equivalents': 'WC02005A'
    }

    ebit_evs = []

    returns_df = fetch_stock_ret_pct(start_date, end_date, db_returns)
    returns_df = returns_df.dropna(thresh=200, axis=1)
    numids = returns_df.columns.tolist()
    year_end = end_date.split('-')[0]

    ebit = fetch_accounting_data(df_name_col_map['ebit'], db_accounting, year_end)
    num_shares = fetch_accounting_data(df_name_col_map['num_shares'], db_accounting, year_end)
    current_liabilities = fetch_accounting_data(df_name_col_map['current_liabilities'], db_accounting, year_end)
    long_term_debt = fetch_accounting_data(df_name_col_map['long_term_debt'], db_accounting, year_end)
    preferred_stock = fetch_accounting_data(df_name_col_map['preferred_stock'], db_accounting, year_end)
    cash_and_cash_equivalents = fetch_accounting_data(df_name_col_map['cash_and_cash_equivalents'], db_accounting, year_end)
    market_price = fetch_market_price(db_price, start_date, end_date)

    # Ensure valid numids
    valid_numids = [numid for numid in numids if not pd.isna(numid) and not np.isinf(numid)]

    for numid in valid_numids:
        try:
            # Check if numid exists in each dataframe
            if (numid not in ebit.columns or numid not in num_shares.columns or numid not in market_price.columns or
                numid not in current_liabilities.columns or numid not in long_term_debt.columns or 
                numid not in preferred_stock.columns or numid not in cash_and_cash_equivalents.columns):
                ebit_evs.append({'numid': numid, 'factor': None})
                continue
            
            # Get the most recent data point for the numid
            ebit_data = ebit[numid].dropna().tail(1)
            num_shares_data = num_shares[numid].dropna().tail(1)
            current_liabilities_data = current_liabilities[numid].dropna().tail(1)
            long_term_debt_data = long_term_debt[numid].dropna().tail(1)
            preferred_stock_data = preferred_stock[numid].dropna().tail(1)
            cash_and_cash_equivalents_data = cash_and_cash_equivalents[numid].dropna().tail(1)
            market_price_data = market_price[numid].dropna().tail(1)
            returns_data = returns_df[numid].dropna()

            if ebit_data.empty or num_shares_data.empty or market_price_data.empty:
                ebit_evs.append({'numid': numid, 'factor': None})
                continue

            ebit_value = ebit_data.values[0]
            num_shares_value = num_shares_data.values[0]
            market_price_value = market_price_data.values[0]

            current_liabilities_value = current_liabilities_data.values[0]
            long_term_debt_value = long_term_debt_data.values[0]
            preferred_stock_value = preferred_stock_data.values[0] if not preferred_stock_data.empty else 0
            cash_and_cash_equivalents_value = cash_and_cash_equivalents_data.values[0]

            if returns_data.empty:
                ebit_evs.append({'numid': numid, 'factor': None})
                continue

            # Calculate Enterprise Value (EV)
            if num_shares_value == 0 or market_price_value == 0:
                ebit_evs.append({'numid': numid, 'factor': None})
                continue

            enterprise_value = (market_price_value * num_shares_value + current_liabilities_value + 
                                long_term_debt_value + preferred_stock_value - cash_and_cash_equivalents_value)
            
            if enterprise_value == 0 or ebit_value == 0:
                ev_ebit = None  # Avoid division by zero
            else:
                ev_ebit = ebit_value / enterprise_value

            if pd.isna(ev_ebit) or np.isinf(ev_ebit):
                ev_ebit = None

            ebit_evs.append({'numid': numid, 'factor': ev_ebit})
        
        except Exception:
            ebit_evs.append({'numid': numid, 'factor': None})

    ebit_ev_df = pd.DataFrame(ebit_evs)
    ebit_ev_df.dropna(subset=['factor'], inplace=True)  # Ensure no NaN values in the 'factor' column

    return ebit_ev_df
