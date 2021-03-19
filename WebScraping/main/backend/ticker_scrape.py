import pandas as pd
import requests
from bs4 import BeautifulSoup

page = requests.get('https://stockanalysis.com/stocks/')

soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find(class_='no-spacing')

tickers_companies = table.find_all("a")

my_data =[tick.get_text() for tick in tickers_companies]

my_tickers = [data.partition('-')[0].strip() for data in my_data]
my_companies = [data.partition('-')[2].strip() for data in my_data]

ticker_table = pd.DataFrame({
            'ticker_symbol': my_tickers,
            'company_name': my_companies
})

print(ticker_table)