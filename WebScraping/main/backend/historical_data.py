import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from pytz import timezone
import time

'''
Below is the scrapper of historical data which contains brief market information for the past year
'''
driver = webdriver.Chrome('c:\\Program Files\\chromedriver.exe')
stock_abbr = 'TSLA'
driver.get('https://finance.yahoo.com/quote/' + stock_abbr + '/history?p=' + stock_abbr)

for i in range(0, 3):
    driver.execute_script("window.scrollBy(0,5000)")
    time.sleep(2)

html_page = driver.page_source
driver.quit()

historical_soup = BeautifulSoup(html_page, 'html.parser')
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