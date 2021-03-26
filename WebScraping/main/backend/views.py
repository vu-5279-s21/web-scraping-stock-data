from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.template.defaultfilters import safe
from pytz import timezone
import pandas as pd

# Create your views here.

# Grabs the text
def get_text(company):
    page = requests.get('https://finance.yahoo.com/quote/' + company + '?p=' + company).text
    return page

def home(request):
    result = ''
    # if we submit form then all attributes will be stored here
    if 'company' in request.GET:
        # Scraper for yahoo finance
        company = request.GET.get('company')
        page = get_text(company)
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find(
            class_='D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) '
                   'smartphone_BdY smartphone_Bdc($seperatorColor)')
        table2 = soup.find(class_='D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) '
                                  'smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)')

        # Current stock price (constantly changing) and EST date/time of retrieval
        current_stock_price = soup.find(class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').get_text()
        tz = timezone('EST')
        date_time = datetime.now(tz)

        # names is a list containing the names of the metric;
        # values is a list containing the values of the associated metric
        names = table.find_all(class_='C($primaryColor) W(51%)')
        values = table.find_all(class_='Ta(end) Fw(600) Lh(14px)')

        names2 = table2.find_all(class_='C($primaryColor) W(51%)')
        values2 = table2.find_all(class_='Ta(end) Fw(600) Lh(14px)')

        metric_names1 = [name.get_text() for name in names]
        metric_values1 = [value.get_text() for value in values]

        metric_names2 = [name2.get_text() for name2 in names2]
        metric_values2 = [value2.get_text() for value2 in values2]

        metric_names = metric_names1 + metric_names2
        metric_values = metric_values1 + metric_values2

        metric_names = ["Date and Time", "Current Stock Price"] + metric_names
        metric_values = [str(date_time), current_stock_price] + metric_values
        table_dict = {}
        for i in range(len(metric_names)):
            table_dict[metric_names[i]] = metric_values[i]

        # print(table_dict)

        stock_data = pd.DataFrame({
            'name': metric_names,
            'value': metric_values
        })

        result = stock_data.to_html(header=False, index=False)
        return render(request, 'main/results.html', {'result': result})
    else:
        return render(request, 'main/home.html')

def recApp(request):
    # We can likely put our algorithm for the recommendation system here
    # or in a helper method
    return render(request, 'main/recApp.html')

def about(request):
    # Just render the html if we want an about page
    return render(request, 'main/about.html')

def results(request):
    return render(request, 'main/results.html')

