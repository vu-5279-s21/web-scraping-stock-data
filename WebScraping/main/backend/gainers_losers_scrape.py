import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_top_stocks(my_url):
    gainers_page = requests.get(my_url)

    ganiers_soup = BeautifulSoup(gainers_page.content, 'html.parser')
    gainers_table = ganiers_soup.find(class_='W(100%)')
    gainers_row = gainers_table.find_all(class_='simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor) ')

    gainers_companies = gainers_table.find_all(class_='Va(m) Ta(start) Px(10px) Fz(s)')
    gainers_price_change_percent = gainers_table.find_all(class_='Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)')
    gainers_vol_avg_PEratio = gainers_table.find_all(class_='Va(m) Ta(end) Pstart(20px) Fz(s)')
    gainers_marketcap = gainers_table.find_all(class_='Va(m) Ta(end) Pstart(20px) Pend(10px) W(120px) Fz(s)')

    my_symbol =[tick.get_text() for tick in gainers_companies]
    my_price_change_percent =[tick.get_text() for tick in gainers_price_change_percent]
    my_vol_avg = [tick.get_text() for tick in gainers_vol_avg_PEratio]
    my_marketcap = [tick.get_text() for tick in gainers_marketcap]

    gainers_dict = {}
    gainers_info_lst = []
    for i in range(len(my_symbol)):
        tmp_lst = []
        tmp_lst.append(my_price_change_percent[3*i])
        tmp_lst.append(my_price_change_percent[3*i+1])
        tmp_lst.append(my_price_change_percent[3 * i + 2])
        tmp_lst.append(my_vol_avg[3*i])
        tmp_lst.append(my_vol_avg[3*i+1])
        tmp_lst.append(my_marketcap[i])
        tmp_lst.append(my_vol_avg[3 * i+2])
        gainers_dict[my_symbol[i]] = tmp_lst

    gainers_data_frame = pd.DataFrame.from_dict(gainers_dict)
    gainers_data_frame.index = ['Price (Intraday)', 'Change', '%Change', 'Volume', 'Avg Vol (3 months)', 'Market Cap', 'PE Ratio (TTM)']
    gainers_data_frame = gainers_data_frame.T
    print(gainers_data_frame)


get_top_stocks('https://finance.yahoo.com/gainers')
get_top_stocks('https://finance.yahoo.com/losers')