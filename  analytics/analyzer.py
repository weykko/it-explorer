import os
import django
import pandas as pd
import matplotlib.pyplot as plt

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_explorer.settings')
django.setup()

from main_app.models import (
    Graph,
    SalaryByYear, CountByYear, SalaryByCity, CountByCity,
    SalaryByYearProf, CountByYearProf, SalaryByCityProf, CountByCityProf,
    TopSkills
)


def convert_to_rub(salary_from, salary_to, currency):
    if currency in ['RUR', 'RUB']:
        return (salary_from + salary_to) / 2
    else:
        currency_rates = {'USD': 75, 'EUR': 90}
        rate = currency_rates.get(currency, 1)
        return ((salary_from + salary_to) / 2) * rate


def analyze_vacancies(csv_path):
    df = pd.read_csv(csv_path)

    keywords = ['frontend', 'фронтенд', 'вёрстка', 'верстка', 'верста', 'front end',
                'angular', 'html', 'css', 'react', 'vue']
    pattern = '|'.join(keywords)
    df_filtered = df[df['name'].str.contains(pattern, case=False, na=False)]

    df_filtered['salary_rub'] = df_filtered.apply(
        lambda row: convert_to_rub(row['salary_from'], row['salary_to'], row['salary_currency']),
        axis=1
    )

    df_filtered = df_filtered[df_filtered['salary_rub'] <= 10_000_000]

    df_filtered['published_at'] = pd.to_datetime(df_filtered['published_at'])
    df_filtered['year'] = df_filtered['published_at'].dt.year
    df_filtered['month'] = df_filtered['published_at'].dt.month

    return df_filtered


def create_graph(title, x, y, graph_path, graph_type='line'):
    plt.figure(figsize=(10, 6))
    if graph_type == 'line':
        plt.plot(x, y, marker='o')
    elif graph_type == 'bar':
        plt.bar(x, y)
    elif graph_type == 'barh':
        plt.barh(x, y)
    plt.title(title)
    if graph_type != 'barh':
        plt.xlabel('Год' if 'год' in title.lower() else 'Город')
        plt.ylabel(
            'Средняя зарплата (руб)' if 'зарплата' in title.lower() else 'Доля (%)' if 'доля' in title.lower() else 'Количество вакансий')
    else:
        plt.xlabel('Средняя зарплата (руб)' if 'зарплата' in title.lower() else 'Доля (%)')
        plt.ylabel('Город')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()


def save_graph(title, graph_path, description=''):
    graph_rel_path = os.path.relpath(graph_path, 'analyze_scripts/graphs/')
    graph = Graph.objects.create(
        title=title,
        image=graph_rel_path.replace('\\', '/'),  # Для Windows путей
        description=description
    )
    return graph


def save_salary_by_year(df_filtered):
    salary_by_year = df_filtered.groupby('year')['salary_rub'].mean().reset_index()
    csv_path = 'analyze_scripts/output/csvs/salary_by_year.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    salary_by_year.to_csv(csv_path, index=False)

    # Создание графика
    graph_path = 'analyze_scripts/output/graphs/salary_by_year.png'
    create_graph(
        title='Динамика уровня зарплат по годам',
        x=salary_by_year['year'],
        y=salary_by_year['average_salary'],
        graph_path=graph_path,
        graph_type='line'
    )

    # Сохранение данных в модель
    for _, row in salary_by_year.iterrows():
        salary_record, created = SalaryByYear.objects.update_or_create(
            year=row['year'],
            defaults={'average_salary': row['average_salary']}
        )
        # Создание и привязка графика
        if created:
            graph = save_graph('Динамика уровня зарплат по годам', graph_path, 'Средняя зарплата по годам.')
            salary_record.graph = graph
            salary_record.save()


def save_count_by_year(df_filtered):
    count_by_year = df_filtered.groupby('year').size().reset_index(name='vacancy_count')
    csv_path = 'analyze_scripts/output/csvs/count_by_year.csv'
    count_by_year.to_csv(csv_path, index=False)

    # Создание графика
    graph_path = 'analyze_scripts/output/graphs/count_by_year.png'
    create_graph(
        title='Динамика количества вакансий по годам',
        x=count_by_year['year'],
        y=count_by_year['vacancy_count'],
        graph_path=graph_path,
        graph_type='bar'
    )

    # Сохранение данных в модель
    for _, row in count_by_year.iterrows():
        count_record, created = CountByYear.objects.update_or_create(
            year=row['year'],
            defaults={'vacancy_count': row['vacancy_count']}
        )
        # Создание и привязка графика
        if created:
            graph = save_graph('Динамика количества вакансий по годам', graph_path, 'Количество вакансий по годам.')
            count_record.graph = graph
            count_record.save()


def save_salary_by_city(df_filtered):
    salary_by_city = df_filtered.groupby('area_name')['salary_rub'].mean().reset_index()
    salary_by_city = salary_by_city.sort_values(by='salary_rub', ascending=False).head(10)
    csv_path = 'analyze_scripts/output/csvs/salary_by_city.csv'
    salary_by_city.to_csv(csv_path, index=False)

    # Создание графика
    graph_path = 'analyze_scripts/output/graphs/salary_by_city.png'
    create_graph(
        title='Уровень зарплат по городам',
        x=salary_by_city['average_salary'],
        y=salary_by_city['area_name'],
        graph_path=graph_path,
        graph_type='barh'
    )

    # Сохранение данных в модель
    for _, row in salary_by_city.iterrows():
        salary_record, created = SalaryByCity.objects.update_or_create(
            city=row['area_name'],
            defaults={'average_salary': row['salary_rub']}
        )
        # Создание и привязка графика
        if created:
            graph = save_graph('Уровень зарплат по городам', graph_path, 'Средняя зарплата по городам.')
            salary_record.graph = graph
            salary_record.save()


def save_count_by_city(df_filtered):
    count_by_city = df_filtered['area_name'].value_counts().reset_index()
    count_by_city.columns = ['city', 'vacancy_count']
    total_vacancies = count_by_city['vacancy_count'].sum()
    count_by_city['share'] = (count_by_city['vacancy_count'] / total_vacancies) * 100
    count_by_city = count_by_city.head(10)
    csv_path = 'analyze_scripts/output/csvs/count_by_city.csv'
    count_by_city.to_csv(csv_path, index=False)

    # Создание графика
    graph_path = 'analyze_scripts/output/graphs/count_by_city.png'
    create_graph(
        title='Доля вакансий по городам',
        x=count_by_city['share'],
        y=count_by_city['city'],
        graph_path=graph_path,
        graph_type='barh'
    )

    # Сохранение данных в модель
    for _, row in count_by_city.iterrows():
        count_record, created = CountByCity.objects.update_or_create(
            city=row['city'],
            defaults={
                'vacancy_count': row['vacancy_count'],
                'share': row['share']
            }
        )
        # Создание и привязка графика
        if created:
            graph = save_graph('Доля вакансий по городам', graph_path, 'Доля вакансий по городам.')
            count_record.graph = graph
            count_record.save()


def save_salary_by_year_prof(df_filtered):
    salary_by_year = df_filtered.groupby('year')['salary_rub'].mean().reset_index()
    csv_path = 'analyze_scripts/output/csvs/salary_by_year_prof.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    salary_by_year.to_csv(csv_path, index=False)

    # Создание графика
    graph_path = 'analyze_scripts/output/graphs/salary_by_year_prof.png'
    create_graph(
        title='Динамика уровня зарплат по годам (Профессия)',
        x=salary_by_year['year'],
        y=salary_by_year['average_salary'],
        graph_path=graph_path,
        graph_type='line'
    )

    # Сохранение данных в модель
    for _, row in salary_by_year.iterrows():
        salary_record, created = SalaryByYearProf.objects.update_or_create(
            year=row['year'],
            defaults={'average_salary': row['salary_rub']}
        )
        # Создание и привязка графика
        if created:
            graph = save_graph('Динамика уровня зарплат по годам (Профессия)', graph_path,
                               'Средняя зарплата по годам для выбранной профессии.')
            salary_record.graph = graph
            salary_record.save()


def save_count_by_year_prof(df_filtered):
    count_by_year = df_filtered.groupby('year').size().reset_index(name='vacancy_count')
    csv_path = 'analyze_scripts/output/csvs/count_by_year_prof.csv'
    count_by_year.to_csv(csv_path, index=False)

    # Создание графика
    graph_path = 'analyze_scripts/output/graphs/count_by_year_prof.png'
    create_graph(
        title='Динамика количества вакансий по годам (Профессия)',
        x=count_by_year['year'],
        y=count_by_year['vacancy_count'],
        graph_path=graph_path,
        graph_type='bar'
    )

    # Сохранение данных в модель
    for _, row in count_by_year.iterrows():
        count_record, created = CountByYearProf.objects.update_or_create(
            year=row['year'],
            defaults={'vacancy_count': row['vacancy_count']}
        )
        # Создание и привязка графика
        if created:
            graph = save_graph('Динамика количества вакансий по годам (Профессия)', graph_path,
                               'Количество вакансий по годам для выбранной профессии.')
            count_record.graph = graph
            count_record.save()


def save_salary_by_city_prof(df_filtered):
    salary_by_city = df_filtered.groupby('area_name')['salary_rub'].mean().reset_index()
    salary_by_city = salary_by_city.sort_values(by='salary_rub', ascending=False).head(10)
    csv_path = 'analyze_scripts/output/csvs/salary_by_city_prof.csv'
    salary_by_city.to_csv(csv_path, index=False)

    # Создание графика
    graph_path = 'analyze_scripts/output/graphs/salary_by_city_prof.png'
    create_graph(
        title='Уровень зарплат по городам (Профессия)',
        x=salary_by_city['average_salary'],
        y=salary_by_city['area_name'],
        graph_path=graph_path,
        graph_type='barh'
    )

    # Сохранение данных в модель
    for _, row in salary_by_city.iterrows():
        salary_record, created = SalaryByCityProf.objects.update_or_create(
            city=row['area_name'],
            defaults={'average_salary': row['salary_rub']}
        )
        # Создание и привязка графика
        if created:
            graph = save_graph('Уровень зарплат по городам (Профессия)', graph_path,
                               'Средняя зарплата по городам для выбранной профессии.')
            salary_record.graph = graph
            salary_record.save()


def save_count_by_city_prof(df_filtered):
    count_by_city = df_filtered['area_name'].value_counts().reset_index()
    count_by_city.columns = ['city', 'vacancy_count']
    total_vacancies = count_by_city['vacancy_count'].sum()
    count_by_city['share'] = (count_by_city['vacancy_count'] / total_vacancies) * 100
    count_by_city = count_by_city.head(10)
    csv_path = 'analyze_scripts/output/csvs/count_by_city_prof.csv'
    count_by_city.to_csv(csv_path, index=False)

    # Создание графика
    graph_path = 'analyze_scripts/output/graphs/count_by_city_prof.png'
    create_graph(
        title='Доля вакансий по городам (Профессия)',
        x=count_by_city['share'],
        y=count_by_city['city'],
        graph_path=graph_path,
        graph_type='barh'
    )

    # Сохранение данных в модель
    for _, row in count_by_city.iterrows():
        count_record, created = CountByCityProf.objects.update_or_create(
            city=row['city'],
            defaults={
                'vacancy_count': row['vacancy_count'],
                'share': row['share']
            }
        )
        # Создание и привязка графика
        if created:
            graph = save_graph('Доля вакансий по городам (Профессия)', graph_path,
                               'Доля вакансий по городам для выбранной профессии.')
            count_record.graph = graph
            count_record.save()


def save_top_skills(df_filtered):
    years = df_filtered['year'].unique()
    for year in years:
        skills = df_filtered[df_filtered['year'] == year]['key_skills'].dropna().str.split(', ').explode()
        top_skills = skills.value_counts().head(20).reset_index()
        top_skills.columns = ['skill', 'count']

        csv_path = f'analyze_scripts/output/csvs/top_skills_{year}.csv'
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        top_skills.to_csv(csv_path, index=False)

        # Создание графика
        graph_path = f'analyze_scripts/output/graphs/top_skills_{year}.png'
        create_graph(
            title=f'TOP-20 навыков Frontend-разработчиков в {year} году',
            x=top_skills['count'],
            y=top_skills['skill'],
            graph_path=graph_path,
            graph_type='barh'
        )

        # Сохранение данных в модель
        for _, row in top_skills.iterrows():
            TopSkills.objects.update_or_create(
                year=year,
                skill=row['skill'],
                defaults={'count': row['count']}
            )

        # Создание и привязка графика
        # Предполагаем, что каждый график связан с несколькими навыками, поэтому не привязываем его к модели TopSkills
        # Если необходимо, можно создать отдельную модель для хранения связи между TopSkills и Graph


def main():
    # Путь к CSV файлу
    csv_path = 'analyze_scripts/input/vacancies_2024.csv'  # Замените на актуальный путь

    # Проверка существования файла
    if not os.path.exists(csv_path):
        print(f"Файл {csv_path} не найден.")
        return

    # Анализ данных
    df_filtered = analyze_vacancies(csv_path)

    # Сохранение данных в модели
    save_salary_by_year(df_filtered)
    save_count_by_year(df_filtered)
    save_salary_by_city(df_filtered)
    save_count_by_city(df_filtered)
    save_salary_by_year_prof(df_filtered)
    save_count_by_year_prof(df_filtered)
    save_salary_by_city_prof(df_filtered)
    save_count_by_city_prof(df_filtered)
    save_top_skills(df_filtered)

    print("Анализ данных завершён и сохранён в базе данных.")


if __name__ == '__main__':
    main()
