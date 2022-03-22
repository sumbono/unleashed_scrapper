import json, pandas as pd

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
