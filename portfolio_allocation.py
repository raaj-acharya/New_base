import pandas as pd

portfolio = {}
def read_datafile(in_file):
    temp_portfolio = {}
    fp = open(in_file, "r")
    header = fp.readline().strip().split(",")

    for line in fp:
        portfolio_item = {}
        line_values = line.strip().split(",")
        for dict_key, dict_value in zip(header, line_values):
            if dict_key in ['symbol', 'Description']:
                portfolio_item[dict_key] = dict_value
            elif dict_key in ['price', 'shares']:
                portfolio_item[dict_key] = float(dict_value)
            else:
                portfolio_item[dict_key] = dict_value

        ticker = portfolio_item["symbol"]
        del portfolio_item['symbol']
        temp_portfolio[ticker] = portfolio_item
    # end loop
    return temp_portfolio

def validate_portfolio(portfolio_data):
    if not isinstance(portfolio_data, dict):
        raise ValueError("Portfolio must be a dictionary")

    if not portfolio_data:
        raise ValueError("Portfolio is empty")

    for ticker, portfolio_item in portfolio_data.items():
        if not isinstance(ticker, str) or ticker == '':
            raise ValueError(f"Invalid value for asset: < {ticker} >")
        elif not isinstance(portfolio_item['price'], (int, float)) or portfolio_item['price'] < 0:
            raise ValueError(f"Invalid value for asset: < {ticker}, price: {portfolio_item['price']} > need to be positive")
        elif not isinstance(portfolio_item['shares'], (int, float)) or (portfolio_item['shares'] < 0):
            raise ValueError(f"Invalid value for asset: < {ticker}, shares: {portfolio_item['shares']} > need to be positive")
        else:
            pass

def calculate_allocations(portfolio_data):
    normalized_allocations = {}
    portfolio_value = sum(holding['price'] * holding['shares'] for ticker, holding in portfolio_data.items())
    if portfolio_value == 0:
        raise ValueError("Total portfolio value cannot be zero")

    for ticker, portfolio_item in portfolio_data.items():
        temp_row = {'description': portfolio_item['Description'],
                    'shares': portfolio_item['shares'], "price": portfolio_item['price'],
                    'total': portfolio_item['price'] * portfolio_item['shares'],
                    'normal_allocation': (((portfolio_item['shares'] * portfolio_item['price']) / portfolio_value) * 100)}
        normalized_allocations[ticker] = temp_row
    return normalized_allocations


portfolio = read_datafile('myshares_data.csv')
validate_portfolio(portfolio)
computed_allocations = calculate_allocations(portfolio)

allocation_df = pd.DataFrame.from_dict(computed_allocations, orient='index' )
allocation_df.reset_index(inplace=True)
allocation_df.rename(columns={'index':'ticker'}, inplace=True)

# write report
allocation_df.to_csv('portfolio_allocations.csv', index=False)
