from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Statistics
from datetime import datetime, timedelta
import requests


def home_view(request):
    return render(request, 'home.html', {'title': 'Главная'})


def general_view(request):
    context = {
        'salary_trends': get_object_or_404(Statistics, title='Динамика уровня зарплат по годам'),
        'vacancy_trends': get_object_or_404(Statistics, title='Динамика количества вакансий по годам'),
        'salary_by_city': get_object_or_404(Statistics, title='Уровень зарплат по городам'),
        'vacancy_share_by_city': get_object_or_404(Statistics, title='Доля вакансий по городам'),
        'top_skills': get_object_or_404(Statistics, title='Динамика ТОП-20 навыков по годам'),
        'title': 'Общая статистика'
    }
    return render(request, 'general.html', context)


def demand_view(request):
    context = {
        'salary_trends': get_object_or_404(Statistics, title='Динамика уровня зарплат по годам для frontend-разработчика'),
        'vacancy_trends': get_object_or_404(Statistics, title='Динамика количества вакансий по годам для frontend-разработчика'),
        'title': 'Востребованность'
    }
    return render(request, 'demand.html', context)


def geography_view(request):
    context = {
        'salary_by_city': get_object_or_404(Statistics, title='Уровень зарплат по городам для frontend-разработчика'),
        'vacancy_share_by_city': get_object_or_404(Statistics, title='Доля вакансий по городам для frontend-разработчика'),
        'title': 'География'
    }
    return render(request, 'geography.html', context)


def skills_view(request):
    context = {
        'top_skills': get_object_or_404(Statistics, title='Динамика ТОП-20 навыков по годам для frontend-разработчика'),
        'title': 'Навыки'
    }
    return render(request, 'skills.html', context)


def get_hh_vacancies():
    # Параметры запроса к API HH
    url = "https://api.hh.ru/vacancies"

    # Установка временных рамок (последние 24 часа)
    date_from = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')

    params = {
        "text": 'frontend',  # Поиск по ключевым словам
        'search_field': 'name',
        "date_from": date_from,
        "per_page": 10,  # Максимум 10 вакансий
        "order_by": "publication_time"  # Сортировка по дате публикации
    }

    response = requests.get(url, params=params)
    vacancies = response.json().get('items', [])

    result = []
    for vacancy in vacancies:

        vacancy_details = requests.get(vacancy['url']).json()

        result.append({
            "name": vacancy.get("name"),
            "description": vacancy_details.get("description"),
            "skills": ", ".join([skill.get("name") for skill in vacancy_details.get("key_skills", [])]),
            "company": vacancy.get("employer", {}).get("name"),
            "salary": parse_salary(vacancy.get("salary")),
            "region": vacancy.get("area", {}).get("name"),
            "published_at": vacancy.get("published_at")[:10],
        })
    return result


def parse_salary(salary):
    if not salary:
        return "Не указано"
    if not salary['from']:
        return f"{salary['to']} {salary['currency']}"
    if not salary['to']:
        return f"{salary['from']} {salary['currency']}"
    return f"{salary['from']} - {salary['to']} {salary['currency']}"


def latest_vacancies_view(request):
    return render(request, "latest_vacancies.html", {'title': 'Вакансии'})


def get_hh_vacancies_json(request):
    vacancies = get_hh_vacancies()
    return JsonResponse({"vacancies": vacancies})