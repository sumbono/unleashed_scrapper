from libs import api_signature, currency_parser, customer_parser, invoice_parser, product_parser
import json, os, random, requests, time

class UnleashedScraper():
    def __init__(self) -> None:
        self.base_url = "https://api.unleashedsoftware.com/"
        self.API_ID = os.environ.get('API_ID') #,'7100746f-c193-4c95-9e8e-ee4a10fc30c4'
        self.API_KEY = os.environ.get('API_KEY') #,'ePXmVMSOs3T3zVSoAuJPc4K21s3ciFHCRnVzsZwF7lULSJayn4rb8eGEz9vWKMRMOB893UmrzpLSkS3kZQDaw=='
        if not (self.API_ID and self.API_KEY):
            raise Exception(f"API_ID / API_KEY not found on env variable!")
        
    def customer_parser(self,data):
        pass
        
    def invoice_parser(self,data):
        pass
    
    def get_headers(self,query_string=''):
        
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'api-auth-id': self.API_ID,
            'api-auth-signature': api_signature(query_string,self.API_KEY)
        }

    def req_crawler(self,url,headers):
        """_summary_
            The unleashed API fetcher.
        
        Args:
            url (str): wanted url in full format (with or without query params).
            headers (dict): the headers required for this request.

        Returns:
            tuple: (response,error) returning response of the request and the error (if any).
        """

        res = None
        error = None

        try:
            res = requests.get(url, headers=headers, timeout=20) #verify=False, 
        except requests.exceptions.HTTPError as err:
            error = f"HTTP ERROR - {err}"
        except requests.exceptions.SSLError as err:
            error = f"SSL ERROR - {err}"
        except requests.exceptions.RequestException as err:
            error = f"OTHER REQ ERROR - {err}"
        except Exception as err:
            error = f"OTHER ERROR - {err}"
        
        return res,error
    
    def endpoint_fetcher(self,endpoint,query_string=''):
        url = f"{self.base_url}/{endpoint}"
        return self.req_crawler(url,query_string)

    def ctrl(self,endpoint,endpoint_id=None,crawl_mode='all',page_num=None,page_size=None,qfilter_key=None,qfilter_val=None):
        """_summary_
            api fetcher controller.
            have 3 crawling mode: all, page, filter.
            - all: crawling all data on that endpoint.
            - page: crawling particular page on that endpoint.
            - filter: crawling particular filter by its key & value. 
        
        Args:
            endpoint (str): particular endpoint of unleashed API. See unleashed API docs for available endpoints.
            endpoint_id (str): ID of the particular element from the endpoint. Defaults to None.
            crawl_mode (str, optional): crawling mode: all, page, filter. Defaults to 'all'.
            page_num (int, optional): Defaults to None.
            page_size (int, optional): Defaults to None.
            qfilter_key (str, optional): query filter key, diferent for each endpoint. See unleashed API docs for more details. Defaults to None.
            qfilter_val (str, optional): query filter value. Defaults to None.
        """

        query_string = ''
        url = f"{self.base_url}/{endpoint}"
        
        if endpoint_id:
            url = f"{url}/{endpoint_id}"

        elif crawl_mode=='page':
            if page_num:
                if page_size:
                    url = f"{url}/{page_num}?pageSize={page_size}"
                    query_string = f"pageSize={page_size}"
                else:
                    url = f"{url}/{page_num}"
                
        elif crawl_mode=='filter' and all([qfilter_key,qfilter_val]):
            url = f"{url}/1?{qfilter_key}={qfilter_val}"
            query_string = f"{qfilter_key}={qfilter_val}"

        headers = self.get_headers(query_string)
        print(f"query_string: {query_string} \nheaders: {headers}")
        res,error = self.req_crawler(url,headers)
        if isinstance(res, requests.models.Response):
            if res.status_code == 200:
                data = res.json()
                # NumberOfItems = data['Pagination']['NumberOfItems']
                # PageSize = data['Pagination']['PageSize']
                # PageNumber = data['Pagination']['PageNumber']
                # NumberOfPages = data['Pagination']['NumberOfPages']
                # print(f"Pagination: {NumberOfItems},{PageSize},{PageNumber},{NumberOfPages}")

                with open(f"data/{endpoint}.json", "w") as write_file:
                    json.dump(data, write_file, indent=4)
            else:
                print(f"status_code: {res.status_code}")
                print(f"response_text: {res.text}")
        else:
            print(f"error: {error}")
            print(res.text)

if __name__ == "__main__":
    endpoints = {
        'Currencies':currency_parser, 
        'Products':product_parser, 
        'Customers':customer_parser, 
        'Invoices':invoice_parser,
    }
    
    us = UnleashedScraper()
    for k,v in endpoints.items():
        us.ctrl(k)
        with open(f"data/{k}.json", "r") as read_file:
            obj = json.load(read_file)
            v(obj['Items'])


