import json, pandas as pd

def product_parser(products_data):
    """_summary_
        Products data parser.
        For test purpose, only took 3 product fields: ProductCode, ProductDescription, & Guid
    Args:
        products_data (list): list of product details dictionary.
    """

    if products_data:
        
        products = []
        for data in products_data:
            products.append({
                "ProductCode": data["ProductCode"],
                "ProductDescription": data["ProductDescription"],
                "Guid": data["Guid"]
                # "LastModifiedOn": data["LastModifiedOn"]
            })

        if products:
            try:
                dfc1 = pd.read_csv(f'data/Products.csv')
                dfc2 = pd.DataFrame(products)
                dfc_new = pd.concat([dfc1, dfc2], ignore_index=True)
            except:
                dfc_new = pd.DataFrame(products)
            
            dfc = dfc_new.drop_duplicates(subset=['Guid'],keep='last')
            dfc.to_csv(f'data/Products.csv', index=False, mode='w', header=True)
            print(dfc.head())
            print(dfc.info())


if __name__ == "__main__":
    endpoint = 'Products'
    with open(f"data/{endpoint}.json", "r") as read_file:
        obj = json.load(read_file)
        products_data = obj['Items']
        product_parser(products_data)