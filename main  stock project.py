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
