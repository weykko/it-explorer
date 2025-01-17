import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def get_rates(date_str, currencies):
    response = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_str}")
    soup = BeautifulSoup(response.content, 'xml')
    rates = {'date': date_str}

    for currency in currencies:
        rates[currency] = pd.NA
        valute = soup.find('CharCode', string=currency)
        if valute is not None:
            rate = valute.find_next_sibling('VunitRate').get_text()
            if currency == 'BYR':
                rate = valute.find_next_sibling('Value').get_text()
            rates[currency]=round(float(rate.replace(',', '.')),8)

    return rates

date_sequence = pd.date_range(start='2003-01-01', end='2023-12-31', freq='MS')
currencies = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL', 'BYN']
data=[]
for date in date_sequence:
    date_str = date.strftime('%d/%m/%Y')
    rates = get_rates(date_str, currencies)
    data.append(rates)
pd.DataFrame(data).to_csv('rates.csv',index=False)