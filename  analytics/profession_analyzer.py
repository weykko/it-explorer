import os
import django
import pandas as pd
from django.utils.html import escape
import matplotlib.pyplot as plt
from io import BytesIO
from django.core.files.base import ContentFile

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

    df['salary'] = df.apply(convert_to_rub, axis=1)

    salary_by_year = df.groupby('year')['salary'].mean().reset_index()

    html = "<table><tr><th>Год</th><th>Уровень зарплат</th></tr>"
    for index, row in salary_by_year.iterrows():
        html += f"<tr><td>{escape(int(row['year']))}</td><td>{escape(f'{row['salary']:.0f}')}</td></tr>"
    html += "</table>"

    statistic = Statistics.objects.create(
        title="Динамика уровня зарплат по годам для frontend-разработчика",
        table_data=html
    )

    plt.figure(figsize=(10, 8))
    plt.plot(
        salary_by_year['year'],
        salary_by_year['salary'],
        marker='o',
        color='#576cf7',
        linestyle='-',
        linewidth=2,
        markersize=6
    )
    plt.xlabel('Годы', fontsize=12)
    plt.ylabel('Зарплата (руб)', fontsize=12)
    plt.grid(True)
    plt.xticks(salary_by_year['year'], rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    statistic.graph.save('salary_dynamics_by_year.png', ContentFile(buffer.read()), save=True)
    buffer.close()


def vacancies_count_by_year(df):
    df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
    vacancies_count = df.groupby('year').size().reset_index(name='count')

    html = "<table><tr><th>Год</th><th>Количество вакансий</th></tr>"
    for index, row in vacancies_count.iterrows():
        html += f"<tr><td>{escape(str(row['year']))}</td><td>{escape(str(row['count']))}</td></tr>"
    html += "</table>"

    statistic = Statistics.objects.create(
        title="Динамика количества вакансий по годам для frontend-разработчика",
        table_data=html
    )

    plt.figure(figsize=(10, 8))
    plt.plot(
        vacancies_count['year'],
        vacancies_count['count'],
        marker='o',
        color='#49d14d',
        linestyle='-',
        linewidth=2,
        markersize=6
    )
    plt.xlabel('Годы', fontsize=12)
    plt.ylabel('Количество вакансий', fontsize=12)
    plt.grid(True)
    plt.xticks(df['Год'], rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    statistic.graph.save('vacancies_count_by_year.png', ContentFile(buffer.read()), save=True)
    buffer.close()


def salary_by_city(df):
    df = df[(df['salary_from'] <= 10000000) & (df['salary_to'] <= 10000000)]
    df['average_salary'] = df[['salary_from', 'salary_to']].mean(axis=1)

    df['salary'] = df.apply(convert_to_rub, axis=1)

    total_vacancies = len(df)

    city_stats = df.groupby('area_name').agg(
        salary=('salary', 'mean'),
        count=('area_name', 'count')
    ).reset_index()

    city_stats['share'] = city_stats['count'] / total_vacancies
    filtered_cities = city_stats[city_stats['share'] >= 0.01]
    salary_by_city = filtered_cities.sort_values(by='salary', ascending=False).head(10)

    html = "<table><tr><th>Город</th><th>Уровень зарплат</th></tr>"
    for index, row in salary_by_city.iterrows():
        html += f"<tr><td>{escape(row['area_name'])}</td><td>{escape(f'{row['salary']:.0f}')}</td></tr>"
    html += "</table>"

    statistic = Statistics.objects.create(
        title="Уровень зарплат по городам для для frontend-разработчика",
        table_data=html
    )

    plt.figure(figsize=(10, 8))
    plt.bar(
        salary_by_city['area_name'],
        salary_by_city['salary'],
        color='#c689fa',
        edgecolor='black'
    )
    plt.xlabel('Город', fontsize=12)
    plt.ylabel('Зарплата (руб)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    statistic.graph.save('salary_by_city.png', ContentFile(buffer.read()), save=True)
    buffer.close()


def vacancies_share_by_city(df):
    vacancies_count = df.groupby('area_name').size().reset_index(name='count')
    total_vacancies = vacancies_count['count'].sum()
    vacancies_count['share'] = (vacancies_count['count'] / total_vacancies) * 100
    vacancies_count = vacancies_count.sort_values(by='share', ascending=False)

    other_cities = vacancies_count.tail(len(vacancies_count) - 10)
    other_cities_share = other_cities['share'].sum()
    top_cities = vacancies_count.head(10)
    top_cities.loc[10] = {'area_name': 'Другие города', 'share': other_cities_share}

    html = "<table><tr><th>Город</th><th>Доля вакансий</th></tr>"
    for index, row in top_cities.iterrows():
        html += f"<tr><td>{escape(row['area_name'])}</td><td>{escape(f'{row['share']:.2f}')}</td></tr>"
    html += "</table>"

    statistic = Statistics.objects.create(
        title="Доля вакансий по городам для frontend-разработчика",
        table_data=html
    )

    plt.figure(figsize=(10, 8))
    plt.pie(
        df['Доля вакансий (%)'],
        labels=df['Город'],
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Pastel2.colors
    )
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    statistic.graph.save('vacancies_share_by_city.png', ContentFile(buffer.read()), save=True)
    buffer.close()


def main():
    df = pd.read_csv('vacancies.csv', dtype = {
        'name': 'str',
        'key_skills': 'str',
        'salary_from': 'float',
        'salary_to': 'float',
        'salary_currency': 'str',
        'area_name': 'str',
        'published_at': 'str'
    })
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