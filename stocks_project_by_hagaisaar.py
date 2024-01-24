import pandas as pd
from urllib.request import Request, urlopen


def get_data():
    """gets a dataframe of ticker data with all israeli stocks

    :return: dataframe, ticker data with all israeli stocks
    """
    tables = []
    i = 1
    base_url = r'https://finviz.com/screener.ashx?v=141&f=geo_israel'

    while True:
        new_url = f'{base_url}&r={i}'

        req = Request(
            url=new_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req).read()
        table = pd.read_html(webpage)[-2]

        num = int(table.loc[0, 'No.'])
        if num != i:
            break

        tables.append(table)
        i += 20

    data = pd.concat(tables).reset_index(drop=True)
    return data.set_index('No.')


# function that extracts information about one stock from the website (stock => pandas table)
def get_data_by_ticker(table, ticker):
    ticker_data = table[table['Ticker'] == ticker]
    return ticker_data


# function that extracts information about Stocks & categories from the website (stock => pandas table)
def get_data_by_list(table, tickers):
    return table[table['Ticker'].isin(tickers)]


# a function that gets the growth estiame table from yahoo finance, given a ticker
def get_est_table_by_ticker(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}'
    req = Request(
                url=url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
    webpage = urlopen(req).read()
    return pd.read_html(webpage)[-1].iloc[:, :2]


def get_est_by_list(tickers, est_range):
    """gets a dictionary with the estimated growth of a list of tickers, given the desired growth estimate

    :param tickers: a list of tickers
    :param est_range: a string representing the range of estimate required (can be: 'Current Qtr.', 'Next Qtr.',
    'Current Year', 'Next Year', 'Next 5 Years (per annum)', 'Past 5 Years (per annum)')

    :return: dict, a dictionary of ticker names and growth estimates (all strings)
    """
    d = {}
    for ticker in tickers:
        df = get_est_table_by_ticker(ticker)
        d[ticker] = df[df['Growth Estimates'] == est_range].iloc[0, 1]

    return d


def main():
    # show all israeli stocks
    df = get_data()
    print(df)

    print()

    # show data only of specific tickers
    df2 = get_data_by_list(df, ['ALAR', 'ALLT', 'AUDC'])
    print(df2)

    print()

    # get growth estimate data on a list of specific tickers
    d = get_est_by_list(['ALAR', 'ZIM'], 'Next Year')
    print(d)


main()
