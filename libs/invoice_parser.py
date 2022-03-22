import json, pandas as pd
endpoint = 'Invoices'

def add_new_address(data):
    pass

def add_new_customer(data):
    # columns = [
    #     Addresses,Contacts,TaxCode,TaxRate,CustomerCode,CustomerName,GSTVATNumber,BankName,BankBranch,BankAccount,Website,PhoneNumber,FaxNumber,MobileNumber,DDINumber,TollFreeNumber,Email,EmailCC,Currency,Notes,Taxable,XeroContactId,SalesPerson,DiscountRate,PrintPackingSlipInsteadOfInvoice,PrintInvoice,StopCredit,Obsolete,XeroSalesAccount,XeroCostOfGoodsAccount,SellPriceTier,SellPriceTierReference,CustomerType,PaymentTerm,ContactFirstName,ContactLastName,SourceId,CreatedBy,CreatedOn,LastModifiedBy,Guid,LastModifiedOn,CurrencyId
    # ]
    pass

def add_new_product(data):
    pass

def customer_guid(cust_code):
    df_cust = pd.read_csv(f'data/Customers.csv')
    df_cust.set_index('CustomerCode',inplace=True)
    return df_cust.loc[cust_code,'Guid']

def deliveryaddr_ccg(AddressUid):
    df_cust = pd.read_csv(f'data/Addresses.csv')
    df_cust.set_index('AddressUid',inplace=True)
    return df_cust.loc[AddressUid,'CustomerCodeGuid']

def product_guid(ProductCode):
    df_product = pd.read_csv(f'data/Products.csv')
    df_product.set_index('ProductCode',inplace=True)
    return df_product.loc[ProductCode,'Guid']

def invoice_parser(invoice_data):
    
    if invoice_data:
        invoice_lines = []
        invoices = []

        for data in invoice_data:
            CustomerCodeGuid = f"{data['Customer']['CustomerCode']}_{data['Customer']['Guid']}"
            
            # check the Customer's Guid
            if not customer_guid(data['Customer']['CustomerCode'])==data['Customer']['Guid']:
                add_new_customer(data['Customer'])
            data['Customer'] = data['Customer']['Guid']

            # Check the DeliveryAddress uid
            if data['DeliveryAddress']:
                if data['DeliveryAddress']['AddressType'] and data['DeliveryAddress']['AddressName']:
                    AddressUid = f"{data['DeliveryAddress']['AddressType']}_{data['DeliveryAddress']['AddressName']}_{CustomerCodeGuid}"
                    if not deliveryaddr_ccg(AddressUid)==CustomerCodeGuid:
                        add_new_address(data['DeliveryAddress'])
                    data['DeliveryAddress'] = CustomerCodeGuid
                else:
                    data['DeliveryAddress'] = None
            else:
                data['DeliveryAddress'] = None

            if data['InvoiceLines']:
                invoice_guid = data['Guid']
                for iline in data['InvoiceLines']:
                    #check the product guid
                    if not product_guid(iline['Product']['ProductCode'])==iline['Product']['Guid']:
                        add_new_product(iline['Product'])
                    
                    iline['Product'] = iline['Product']['Guid']
                    iline['InvoiceGuid'] = invoice_guid
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
    