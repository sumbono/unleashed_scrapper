# Unleashed API Scraper
- Scraping Customers & Invoices data from unleashed API.
- Store the data into csv.
- Use python 3.7+

### Clone the repo and install requirements
```
$ git clone https://github.com/sumbono/unleashed_scrapper.git
$ cd unleashed_scrapper/
$ pip install -r requirements.txt
```

### Running the scrapper
- copy your unleashed API_ID & API_KEY to .env.sample file.
- change the .env.sample to .env

```
$ cd unleashed_scrapper/
$ export $(cat .env | egrep -v "(^#.*|^$)" | xargs)
$ python scrapper.py
```
