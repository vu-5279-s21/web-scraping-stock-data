import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from pytz import timezone
import time
from django.shortcuts import render


def historical(request):
    '''
    Below is the scrapper of historical data which contains brief market information for the past year
    '''

    result = ''
    if 'company' in request.GET:
        stock_abbr = request.GET.get('company')
        driver = webdriver.Chrome('c:\\Program Files\\chromedriver.exe')
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
            if i % 6 == 0:
                tmp_val = stock_list[i].replace(',', '')
                tmp_dic = float(tmp_val)
                tmp_lst.append(tmp_dic)
            elif i % 6 == 1:
                tmp_val = stock_list[i].replace(',', '')
                tmp_dic = float(tmp_val)
                tmp_lst.append(tmp_dic)
            elif i % 6 == 2:
                tmp_val = stock_list[i].replace(',', '')
                tmp_dic = float(tmp_val)
                tmp_lst.append(tmp_dic)
            elif i % 6 == 3:
                tmp_val = stock_list[i].replace(',', '')
                tmp_dic = float(tmp_val)
                tmp_lst.append(tmp_dic)
            elif i % 6 == 4:
                tmp_val = stock_list[i].replace(',', '')
                tmp_dic = float(tmp_val)
                tmp_lst.append(tmp_dic)
                i += 1
                hist_data_table[dates_list[num_list_insert]] = tmp_lst
                num_list_insert += 1
                tmp_lst = []

        hist_data_frame = pd.DataFrame.from_dict(hist_data_table)
        hist_data_frame = hist_data_frame.astype(float)
        hist_data_frame.index = ['Open', 'High', 'Low', 'Close', 'Adj Close']
        hist_data_frame = hist_data_frame.T
        hist_data_frame = hist_data_frame.iloc[::-1]
        hist_data_frame.plot(grid='True')

        hist_data_frame['5-Day Moving Average'] = hist_data_frame.iloc[:, 4].rolling(window=5).mean()
        hist_data_frame['10-Day Moving Average'] = hist_data_frame.iloc[:, 4].rolling(window=10).mean()
        hist_data_frame['20-Day Moving Average'] = hist_data_frame.iloc[:, 4].rolling(window=20).mean()
        hist_data_frame['50-Day Moving Average'] = hist_data_frame.iloc[:, 4].rolling(window=50).mean()
        hist_data_frame['100-Day Moving Average'] = hist_data_frame.iloc[:, 4].rolling(window=100).mean()
        print(hist_data_frame)
        result = hist_data_frame.to_html()

        closingPrices = hist_data_frame.iloc[:, 4]

        gainPrices = []
        lossPrices = []
        j = 0
        while j < len(closingPrices):
            if j == 0:
                gainPrices.append(0)
                lossPrices.append(0)
            else:
                if (closingPrices[j] - closingPrices[j - 1]) > 0:
                    gainPrices.append(closingPrices[j] - closingPrices[j - 1])
                    lossPrices.append(0)
                else:
                    gainPrices.append(0)
                    lossPrices.append(closingPrices[j] - closingPrices[j - 1])
            j += 1

        gainsLosses = pd.DataFrame({
            'Daily Gains': gainPrices,
            'Daily Losses': lossPrices})
        gainsLosses.index = hist_data_frame.index
        gainsLosses = gainsLosses.astype(float)
        gainsLosses.plot(grid='True')

        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        gainsLossesImage = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()

        #plt.savefig('../../static/graphImages/gainsLosses.png')
        gainsLosses['gainsAvg'] = gainsLosses.iloc[:, 0].rolling(window=14).mean()
        gainsLosses['lossesAvg'] = gainsLosses.iloc[:, 1].rolling(window=14).mean().abs()
        gainsLosses['RS'] = gainsLosses['gainsAvg'] / gainsLosses['lossesAvg']
        gainsLosses['RSI'] = 100 - (100 / (1 + gainsLosses['RS']))
        RSI_graph = gainsLosses[['RSI']]

        ax = RSI_graph.plot(grid='True')
        ax.axhline(y=70, color='r', linestyle='--', lw=2)
        ax.axhline(y=30, color='g', linestyle='--', lw=2)
       # plt.savefig('../../static/graphImages/RSI_graph.png')
        # print(gainsLosses)

        five_day = hist_data_frame[['Adj Close', '5-Day Moving Average']]
        ten_day = hist_data_frame[['Adj Close', '10-Day Moving Average']]
        twenty_day = hist_data_frame[['Adj Close', '20-Day Moving Average']]
        fifty_day = hist_data_frame[['Adj Close', '50-Day Moving Average']]
        hundred_day = hist_data_frame[['Adj Close', '100-Day Moving Average']]
        short_long = hist_data_frame[['Adj Close', '20-Day Moving Average', '50-Day Moving Average', '100-Day Moving Average']]
        moving_averages = hist_data_frame[
            ['5-Day Moving Average', '10-Day Moving Average', '20-Day Moving Average', '50-Day Moving Average',
             '100-Day Moving Average']]
        five_day.plot()
        #plt.savefig('../../static/graphImages/five_day.png')
        ten_day.plot()
        #plt.savefig('../../static/graphImages/ten_day.png')
        twenty_day.plot()
        #plt.savefig('../../static/graphImages/twenty_day.png')
        fifty_day.plot()
        #plt.savefig('../../static/graphImages/fifty_day.png')
        hundred_day.plot()
        #plt.savefig('../../static/graphImages/hundred_day.png')
        short_long.plot()
        #plt.savefig('../../static/graphImages/short_long.png')
        moving_averages.plot()
        #plt.savefig('../../static/graphImages/moving_averages.png')
        # plt.show()

        return render(request, 'main/historical.html', {'result': result, 'gainsLossesImage': gainsLossesImage})
    else:
        return render(request, 'main/historical.html')
