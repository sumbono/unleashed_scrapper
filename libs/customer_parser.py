import json, pandas as pd

def customer_parser(customers_data):

    if customers_data:
        
        addresses = []
        customers = []
        contacts = []

        for data in customers_data:
            
            if data['Addresses']:
                for addr in data['Addresses']:
                    addr['ParentID'] = data['Guid']
                    addresses.append(addr)
                data['Addresses'] = data['Guid']
            else:
                data['Addresses'] = None
                
            if data['Contacts']:
                """_summary_
                    Because there are no information on the docs about this field, 
                    the Contacts schema will be considered to follow the Salespersons schema, example:
                    {
                        "FullName": "John Smith",
                        "Email": "john.smith@acme.co",
                        "Obsolete": false,
                        "Guid": "224ae802-88d3-43c1-b9cc-208d5d6d0ccf",
                        "LastModifiedOn": "/Date(1459218946890)/"
                    }
                """
                for contact in data['Contacts']:
                    contact['ParentID'] = data['Guid']
                    contacts.append(contact)
                data['Contacts'] = data['Guid']
            else:
                data['Contacts'] = None
            
            if data['Currency']:
                for k,v in data['Currency'].items():
                    data[f'Currency.{k}'] = v
                data.pop('Currency')
            else:
                data.pop('Currency')
            
            customers.append(data)

        if customers:
            try:
                dfc1 = pd.read_csv(f'data/Customers.csv')
                dfc2 = pd.DataFrame(customers)
                dfc_new = pd.concat([dfc1, dfc2], ignore_index=True)
            except:
                dfc_new = pd.DataFrame(customers)
            
            dfc = dfc_new.drop_duplicates(subset=['Guid','CustomerCode'],keep='last')
            dfc.to_csv(f'data/Customers.csv', index=False, mode='w', header=True)
            print(dfc.head())
            print(dfc.info())

        if addresses:
            try:
                dfa1 = pd.read_csv(f'data/Addresses.csv')
                dfa2 = pd.DataFrame(addresses)
                dfa_new = pd.concat([dfa1, dfa2], ignore_index=True)
            except:
                dfa_new = pd.DataFrame(addresses)

            dfa = dfa_new.drop_duplicates(subset=['AddressUid'],keep='last')
            dfa.to_csv(f'data/Addresses.csv', index=False, mode='w', header=True)
            print(dfa.head())
            print(dfa.info())

        if contacts:
            try:
                df_contact1 = pd.read_csv(f'data/Contacts.csv')
                df_contact2 = pd.DataFrame(contacts)
                df_contact_new = pd.concat([df_contact1, df_contact2], ignore_index=True)
            except:
                df_contact_new = pd.DataFrame(contacts)
            
            df_contact = df_contact_new.drop_duplicates(subset=['CustomerContactUid'],keep='last')
            df_contact.to_csv(f'data/Contacts.csv', index=False, mode='w', header=True)
            print(df_contact.head())
            print(df_contact.info())


if __name__ == "__main__":
    endpoint = 'Customers'
    with open(f"data/{endpoint}.json", "r") as read_file:
        obj = json.load(read_file)
        customers_data = obj['Items']
        customer_parser(customers_data)
