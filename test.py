import friartuck

if __name__ == "__main__":
    ft = friartuck.FriarTuck()
    r = ft.option_market_data_by_id("f574d5b2-eebc-4c72-9994-cdf3f67cf6cd")
    print(r)