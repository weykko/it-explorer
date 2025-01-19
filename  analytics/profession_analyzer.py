import os
import django
import pandas as pd
from django.utils.html import escape

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_explorer.settings')
django.setup()

from main_app.models import Statistics


def convert_to_rub(row):
    if row['salary_currency'] == 'RUR':
        return row['average_salary']
    currency_data = currency_df[currency_df['date'] == row['published_at'][:7]]
    if not currency_data.empty:
        exchange_rate = currency_data[row['salary_currency']].values[0]
        if exchange_rate:
            return row['average_salary'] * exchange_rate
    return None


def salary_dynamics_by_year(df):
    df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
    df = df[(df['salary_from'] <= 10000000) & (df['salary_to'] <= 10000000)]
    df['average_salary'] = df[['salary_from', 'salary_to']].mean(axis=1)

    df['converted_salary'] = df.apply(convert_to_rub, axis=1)

    salary_by_year = df.groupby('year')['converted_salary'].mean().reset_index()

    html = "<table><tr><th>Год</th><th>Уровень зарплат</th></tr>"
    for index, row in salary_by_year.iterrows():
        html += f"<tr><td>{escape(int(row['year']))}</td><td>{escape(f'{row['converted_salary']:.0f}')}</td></tr>"
    html += "</table>"

    Statistics.objects.create(
        title="Уровень зарплат по годам",
        table_data=html
    )


def vacancies_count_by_year(df):
    df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
    vacancies_count = df.groupby('year').size().reset_index(name='vacancies_count')

    html = "<table><tr><th>Год</th><th>Количество вакансий</th></tr>"
    for index, row in vacancies_count.iterrows():
        html += f"<tr><td>{escape(str(row['year']))}</td><td>{escape(str(row['vacancies_count']))}</td></tr>"
    html += "</table>"

    Statistics.objects.create(
        title="Количество вакансий по годам",
        table_data=html
    )


def salary_by_city(df):
    df = df[(df['salary_from'] <= 10000000) & (df['salary_to'] <= 10000000)]
    df['average_salary'] = df[['salary_from', 'salary_to']].mean(axis=1)

    df['converted_salary'] = df.apply(convert_to_rub, axis=1)

    salary_by_city = df.groupby('area_name')['converted_salary'].mean().reset_index()
    salary_by_city = salary_by_city.sort_values(by='converted_salary', ascending=False).head(10)

    html = "<table><tr><th>Город</th><th>Уровень зарплат</th></tr>"
    for index, row in salary_by_city.iterrows():
        html += f"<tr><td>{escape(row['area_name'])}</td><td>{escape(f'{row['converted_salary']:.0f}')}</td></tr>"
    html += "</table>"

    Statistics.objects.create(
        title="Уровень зарплат по городам",
        table_data=html
    )


def vacancies_share_by_city(df):
    vacancies_count = df.groupby('area_name').size().reset_index(name='vacancies_count')
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


def main():
    df = pd.read_csv('vacancies.csv')
    keywords = ['frontend', 'фронтенд', 'вёрстка', 'верстка', 'верста', 'front end', 'angular', 'html', 'css', 'react',
                'vue']
    regex = '|'.join(keywords)
    prof_df = df[df['name'].str.contains(regex, case=False, na=False)]

    salary_dynamics_by_year(prof_df)
    vacancies_count_by_year(prof_df)
    salary_by_city(prof_df)
    vacancies_share_by_city(prof_df)


if __name__ == '__main__':
    currency_df = pd.read_csv('currency.csv')
    main()