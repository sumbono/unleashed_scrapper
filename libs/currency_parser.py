import json, pandas as pd

def currency_parser(currencies_data):

    if currencies_data:
        
        currencies = []
        for index,data in enumerate(currencies_data,start=1):
            data['CurrencyId'] = index
            currencies.append(data)

        if currencies:
            try:
                df_curr1 = pd.read_csv(f'data/Currencies.csv')
                df_curr2 = pd.DataFrame(currencies)
                df_curr_new = pd.concat([df_curr1, df_curr2], ignore_index=True)
            except:
                df_curr_new = pd.DataFrame(currencies)

            df_curr = df_curr_new.drop_duplicates(subset=['Guid'],keep='last')
            df_curr.to_csv(f'data/Currencies.csv', index=False, mode='w', header=True)
            print(df_curr.head())
            print(df_curr.info())


if __name__ == "__main__":
    endpoint = 'Currencies'
    with open(f"data/{endpoint}.json", "r") as read_file:
        obj = json.load(read_file)
        currencies_data = obj['Items']
        currency_parser(currencies_data)