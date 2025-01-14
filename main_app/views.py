from django.shortcuts import render
from .models import (
    Graph,
    SalaryByYear, CountByYear, SalaryByCity, CountByCity,
    SalaryByYearProf, CountByYearProf, SalaryByCityProf, CountByCityProf,
    TopSkills
)


def home(request):
    return render(request, 'home.html')


def statistics(request):
    # Получение графиков
    graphs = Graph.objects.all()

    # Получение общих данных
    salary_by_year = SalaryByYear.objects.all().order_by('year')
    count_by_year = CountByYear.objects.all().order_by('year')
    salary_by_city = SalaryByCity.objects.all().order_by('-average_salary')[:10]
    count_by_city = CountByCity.objects.all().order_by('-vacancy_count')[:10]

    # Получение профессии специфичных данных
    salary_by_year_prof = SalaryByYearProf.objects.all().order_by('year')
    count_by_year_prof = CountByYearProf.objects.all().order_by('year')
    salary_by_city_prof = SalaryByCityProf.objects.all().order_by('-average_salary')[:10]
    count_by_city_prof = CountByCityProf.objects.all().order_by('-vacancy_count')[:10]
    top_skills = TopSkills.objects.all()

    context = {
        'graphs': graphs,
        'salary_by_year': salary_by_year,
        'count_by_year': count_by_year,
        'salary_by_city': salary_by_city,
        'count_by_city': count_by_city,
        'salary_by_year_prof': salary_by_year_prof,
        'count_by_year_prof': count_by_year_prof,
        'salary_by_city_prof': salary_by_city_prof,
        'count_by_city_prof': count_by_city_prof,
        'top_skills': top_skills,
    }
    return render(request, 'statistics.html', context)


def demand(request):
    # Для страницы "Востребованность" отображаем общие данные по зарплатам и вакансиям
    salary_by_year = SalaryByYear.objects.all().order_by('year')
    count_by_year = CountByYear.objects.all().order_by('year')

    context = {
        'salary_by_year': salary_by_year,
        'count_by_year': count_by_year,
    }
    return render(request, 'demand.html', context)


def geography(request):
    # Получение данных по географии
    salary_by_city = SalaryByCity.objects.all().order_by('-average_salary')[:10]
    count_by_city = CountByCity.objects.all().order_by('-vacancy_count')[:10]

    context = {
        'salary_by_city': salary_by_city,
        'count_by_city': count_by_city,
    }
    return render(request, 'geography.html', context)


def skills(request):
    # Получение данных по навыкам
    top_skills = TopSkills.objects.all()

    # Организация данных по годам
    skills_by_year = {}
    for skill in top_skills:
        skills_by_year.setdefault(skill.year, []).append({
            'skill': skill.skill,
            'count': skill.count
        })

    # Сортировка годов в порядке возрастания
    sorted_skills_by_year = dict(sorted(skills_by_year.items()))

    context = {
        'skills_by_year': sorted_skills_by_year
    }
    return render(request, 'skills.html', context)


def latest_vacancies(request):
    import requests
    from datetime import datetime, timedelta

    # Параметры API HH
    API_URL = 'https://api.hh.ru/vacancies'
    keywords = 'frontend,фронтенд,вёрстка,верстка,верста,front end,angular,html,css,react,vue'
    params = {
        'text': keywords,
        'area': '1',  # Пример: Москва (ID региона)
        'period': 1,  # за последний день
        'page': 0,
        'per_page': 10,
        'order_by': 'publication_time',
        'sort': 'publication_time'
    }

    response = requests.get(API_URL, params=params)
    vacancies = response.json().get('items', [])

    # Получение деталей вакансий
    detailed_vacancies = []
    for vac in vacancies:
        vac_detail = {
            'title': vac.get('name'),
            'company': vac.get('employer', {}).get('name'),
            'salary': format_salary(vac.get('salary')),
            'region': vac.get('area', {}).get('name'),
            'published_at': format_date(vac.get('published_at')),
            'url': vac.get('url')
        }
        # Дополнительные GET-запросы для описания и навыков
        vac_response = requests.get(vac.get('url'))
        if vac_response.status_code == 200:
            vac_data = vac_response.json()
            vac_detail['description'] = vac_data.get('description', '')  # Используйте safe фильтр в шаблоне
            skills = [skill['name'] for skill in vac_data.get('key_skills', [])]
            vac_detail['skills'] = ', '.join(skills)
        detailed_vacancies.append(vac_detail)

    context = {
        'vacancies': detailed_vacancies
    }
    return render(request, 'latest_vacancies.html', context)


def format_salary(salary):
    if salary:
        from_salary = salary.get('from')
        to_salary = salary.get('to')
        currency = salary.get('currency')
        if from_salary and to_salary:
            return f"{from_salary} - {to_salary} {currency}"
        elif from_salary:
            return f"от {from_salary} {currency}"
        elif to_salary:
            return f"до {to_salary} {currency}"
    return "Не указано"


def format_date(date_str):
    # Преобразование даты в удобный формат
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date.strftime('%d.%m.%Y')
    except ValueError:
        return date_str