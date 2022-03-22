import json, pandas as pd

def add_new_address(data):
    """_summary_
        - adding new address if this address currently not exist on data/Addresses.csv.
        - For next development.
    Args:
        data (dict): new address details.
    """
    pass

def add_new_customer(data):
    """_summary_
        - adding new customer if this customer currently not exist on data/Customers.csv.
        - For next development.
    Args:
        data (dict): new customer details.
    """
    pass

def add_new_product(data):
    """_summary_
        - adding new product if this product currently not exist on data/Products.csv.
        - For next development.
    Args:
        data (dict): new product details.
    """
    pass

def customer_guid(CustomerCode):
    """_summary_
        Get customer Guid from existing data on data/Customers.csv.
    Args:
        CustomerCode (str): CustomerCode.

    Returns:
        str: Guid of this CustomerCode.
    """

    df_cust = pd.read_csv(f'data/Customers.csv')
    df_cust.set_index('CustomerCode',inplace=True)
    return df_cust.loc[CustomerCode,'Guid']

def deliveryaddr_ccg(AddressUid):
    """_summary_
        Get address CustomerCodeGuid from existing data on data/Addresss.csv.
    Args:
        AddressUid (str): AddressUid.

    Returns:
        str: CustomerCodeGuid of this addressUid.
    """
    
    df_cust = pd.read_csv(f'data/Addresses.csv')
    df_cust.set_index('AddressUid',inplace=True)
    return df_cust.loc[AddressUid,'CustomerCodeGuid']

def product_guid(ProductCode):
    """_summary_
        Get Product Guid from existing data on data/Products.csv.
    Args:
        ProductCode (str): ProductCode.

    Returns:
        str: Guid of this ProductCode.
    """

    df_product = pd.read_csv(f'data/Products.csv')
    df_product.set_index('ProductCode',inplace=True)
    return df_product.loc[ProductCode,'Guid']

def invoice_parser(invoice_data):
    """_summary_
        - Invoices raw data parser.
        - parsed data save to csv.
    Args:
        invoice_data (dict): raw data of Invoices.
    """
    
    if invoice_data:
        invoice_lines = []
        invoices = []

        for data in invoice_data:
            
            if data['Customer']:
                for k,v in data['Customer'].items():
                    data[f'Customer.{k}'] = v
                data.pop('Customer')
            else:
                data.pop('Customer')

            if data['DeliveryAddress']:
                for k,v in data['DeliveryAddress'].items():
                    data[f'DeliveryAddress.{k}'] = v
                data.pop('DeliveryAddress')
            else:
                data.pop('DeliveryAddress')

            if data['InvoiceLines']:
                invoice_guid = data['Guid']
                for iline in data['InvoiceLines']:
                    if iline['Product']:
                        for k,v in iline['Product'].items():
                            iline[f'Product.{k}'] = v
                        iline.pop('Product')
                    else:
                        iline.pop('Product')
                    
                    iline['ParentID'] = invoice_guid
                    invoice_lines.append(iline)

                data['InvoiceLines'] = invoice_guid

            invoices.append(data)

        if invoices:
            try:
                dfi1 = pd.read_csv(f'data/Invoices.csv')
                dfi2 = pd.DataFrame(invoices)
                dfi_new = pd.concat([dfi1, dfi2], ignore_index=True)
            except:
                dfi_new = pd.DataFrame(invoices)
            
            dfi = dfi_new.drop_duplicates(subset=['Guid'],keep='last')
            dfi.to_csv(f'data/Invoices.csv', index=False, mode='w', header=True)
            print(dfi.head())
            print(dfi.info())

        if invoice_lines:
            try:
                dfil1 = pd.read_csv(f'data/InvoiceLines.csv')
                dfil2 = pd.DataFrame(invoice_lines)
                dfil_new = pd.concat([dfil1, dfil2], ignore_index=True)
            except:
                dfil_new = pd.DataFrame(invoice_lines)
            
            dfil = dfil_new.drop_duplicates(subset=['Guid'],keep='last')
            dfil.to_csv(f'data/InvoiceLines.csv', index=False, mode='w', header=True)
            print(dfil.head())
            print(dfil.info())

if __name__ == "__main__":
    endpoint = 'Invoices'
    with open(f"data/{endpoint}.json", "r") as read_file:
        obj = json.load(read_file)
        invoices_data = obj['Items']
        invoice_parser(invoices_data)
    