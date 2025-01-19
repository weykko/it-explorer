import os
import django
import pandas as pd
from django.utils.html import escape

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_explorer.settings')
django.setup()

from main_app.models import Statistics

vacancies_df = pd.read_csv('vacancies.csv')
currency_df = pd.read_csv('currency.csv')

def convert_to_rub(salary, currency, date):
    if currency == 'RUR': return salary
    currency_data = currency_df[currency_df['date'] == date[:7]]
    if not currency_data.empty:
        exchange_rate = currency_data[currency].values[0]
        if exchange_rate:
            return salary * exchange_rate
    return salary


def salary_dynamics_by_year(vacancies_df):
    vacancies_df['year'] = pd.to_datetime(vacancies_df['published_at'], utc=True).dt.year
    vacancies_df = vacancies_df[(vacancies_df['salary_from'] <= 10000000) & (vacancies_df['salary_to'] <= 10000000)]
    vacancies_df['average_salary'] = vacancies_df[['salary_from', 'salary_to']].mean(axis=1)

    vacancies_df['currency'] = vacancies_df['salary_currency'].apply(lambda x: x if x in currency_df.columns else 'RUR')
    vacancies_df['converted_salary'] = vacancies_df.apply(
        lambda row: convert_to_rub(row['average_salary'], row['currency'], row['published_at']), axis=1)

    salary_by_year = vacancies_df.groupby('year')['converted_salary'].mean().reset_index()

    html = "<table><tr><th>Год</th><th>Уровень зарплат</th></tr>"
    for index, row in salary_by_year.iterrows():
        html += f"<tr><td>{escape(int(row['year']))}</td><td>{escape(f'{row['converted_salary']:.2f}')}</td></tr>"
    html += "</table>"

    Statistics.objects.create(
        title="Уровень зарплат по годам",
        table_data=html
    )


def vacancies_count_by_year(vacancies_df):
    vacancies_df['year'] = pd.to_datetime(vacancies_df['published_at'], utc=True).dt.year
    vacancies_count = vacancies_df.groupby('year').size().reset_index(name='vacancies_count')

    html = "<table><tr><th>Год</th><th>Количество вакансий</th></tr>"
    for index, row in vacancies_count.iterrows():
        html += f"<tr><td>{escape(str(row['year']))}</td><td>{escape(str(row['vacancies_count']))}</td></tr>"
    html += "</table>"

    Statistics.objects.create(
        title="Количество вакансий по годам",
        table_data=html
    )


def salary_by_city(vacancies_df):
    vacancies_df = vacancies_df[(vacancies_df['salary_from'] <= 10000000) & (vacancies_df['salary_to'] <= 10000000)]
    vacancies_df['average_salary'] = vacancies_df[['salary_from', 'salary_to']].mean(axis=1)

    vacancies_df['currency'] = vacancies_df['salary_currency'].apply(lambda x: x if x in currency_df.columns else 'RUR')
    vacancies_df['converted_salary'] = vacancies_df.apply(
        lambda row: convert_to_rub(row['average_salary'], row['currency'], row['published_at']), axis=1)

    salary_by_city = vacancies_df.groupby('area_name')['converted_salary'].mean().reset_index()
    salary_by_city = salary_by_city.sort_values(by='converted_salary', ascending=False).head(10)

    html = "<table><tr><th>Город</th><th>Уровень зарплат</th></tr>"
    for index, row in salary_by_city.iterrows():
        html += f"<tr><td>{escape(row['area_name'])}</td><td>{escape(f'{row['converted_salary']:.2f}')}</td></tr>"
    html += "</table>"

    Statistics.objects.create(
        title="Уровень зарплат по городам",
        table_data=html
    )


def vacancies_share_by_city(vacancies_df):
    vacancies_count = vacancies_df.groupby('area_name').size().reset_index(name='vacancies_count')
    total_vacancies = vacancies_count['vacancies_count'].sum()
    vacancies_count['share'] = (vacancies_count['vacancies_count'] / total_vacancies) * 100
    vacancies_count = vacancies_count.sort_values(by='share', ascending=False)

    other_cities = vacancies_count.tail(len(vacancies_count) - 10)
    other_cities_share = other_cities['share'].sum()
    top_cities = vacancies_count.head(10)
    top_cities.loc[10] = {'area_name': 'Другие города', 'share': other_cities_share}

    html = "<table><tr><th>Город</th><th>Доля вакансий</th></tr>"
    for index, row in top_cities.iterrows():
        html += f"<tr><td>{escape(row['area_name'])}</td><td>{escape(f'{row['share']:.2f}')}</td></tr>"
    html += "</table>"

    Statistics.objects.create(
        title="Доля вакансий по городам",
        table_data=html
    )


salary_dynamics_by_year(vacancies_df)
vacancies_count_by_year(vacancies_df)
salary_by_city(vacancies_df)
vacancies_share_by_city(vacancies_df)