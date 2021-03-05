import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from pytz import timezone

'''
Below is the scrapper of historical data which contains brief market information for the past year
'''
stock_abbr = 'TSLA'
historical_data_page = requests.get('https://finance.yahoo.com/quote/' + stock_abbr + '/history?p=' + stock_abbr)

historical_soup = BeautifulSoup(historical_data_page.content, 'html.parser')
historical_table = historical_soup.find(class_='W(100%) M(0)')
dates_past_year = historical_table.find_all(class_='Py(10px) Ta(start) Pend(10px)')
stock_price_volume = historical_table.find_all(class_='Py(10px) Pstart(10px)')

dates_list = [date.get_text() for date in dates_past_year]
stock_list = [stock.get_text() for stock in stock_price_volume]

# Generates a table with dates as keys and stock price info as values stored in lists
hist_data_table = {}
num_list_insert = 0
tmp_lst = []
for i in range(len(stock_list)):
    if i%6 == 0:
        tmp_dic = {'Open': stock_list[i]}
        tmp_lst.append(tmp_dic)
    elif i%6 == 1:
        tmp_dic = {'High': stock_list[i]}
        tmp_lst.append(tmp_dic)
    elif i%6 == 2:
        tmp_dic = {'Low': stock_list[i]}
        tmp_lst.append(tmp_dic)
    elif i%6 == 3:
        tmp_dic = {'Close': stock_list[i]}
        tmp_lst.append(tmp_dic)
    elif i%6 == 4:
        tmp_dic = {'Adj Close': stock_list[i]}
        tmp_lst.append(tmp_dic)
    elif i%6 == 5:
        tmp_dic = {'Volume': stock_list[i]}
        tmp_lst.append(tmp_dic)
        hist_data_table[dates_list[num_list_insert]] = tmp_lst
        num_list_insert += 1
        tmp_lst = []

print(hist_data_table)