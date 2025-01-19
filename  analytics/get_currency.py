import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta


def fetch_currency_data(start_date, end_date, url, currencies):
    date = start_date
    rows = []

    while date <= end_date:
        params = {'date_req': date.strftime('%d/%m/%Y')}
        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)
        row = {'date': date.strftime('%Y-%m')}

        for element in root.findall('Valute'):
            currency = element.find('CharCode').text
            if currency in currencies:
                value = float(element.find('Value').text.replace(',', '.'))
                nominal = int(element.find('Nominal').text)
                row[currency] = round(value / nominal, 8)

        rows.append(row)
        date = (date + timedelta(days=31)).replace(day=1)

    return rows


def save_to_csv(data, filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)


if __name__ == '__main__':
    start_date = datetime(2003, 1, 1)
    end_date = datetime(2024, 12, 1)
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    currencies = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']
    data = fetch_currency_data(start_date, end_date, url, currencies)
    save_to_csv(data, 'currency.csv')