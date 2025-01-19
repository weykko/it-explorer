from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Statistics

def home_view(request):
    return render(request, 'home.html')


def general_view(request):
    context = {
        'salary_trends': get_object_or_404(Statistics, title='Динамика уровня зарплат по годам'),
        'vacancy_trends': get_object_or_404(Statistics, title='Динамика количества вакансий по годам'),
        'salary_by_city': get_object_or_404(Statistics, title='Уровень зарплат по городам'),
        'vacancy_share_by_city': get_object_or_404(Statistics, title='Доля вакансий по городам'),
        'top_skills': get_object_or_404(Statistics, title='ТОП-20 навыков по годам'),
    }
    return render(request, 'general_statistics.html', context)


def demand_view(request):
    context = {
        'salary_trends': get_object_or_404(Statistics, title='Динамика уровня зарплат по годам для выбранной профессии'),
        'vacancy_trends': get_object_or_404(Statistics, title='Динамика количества вакансий по годам для выбранной профессии'),
    }
    return render(request, 'demand.html', context)


def geography_view(request):
    context = {
        'salary_by_city': get_object_or_404(Statistics, title='Уровень зарплат по городам для выбранной профессии'),
        'vacancy_share_by_city': get_object_or_404(Statistics, title='Доля вакансий по городам для выбранной профессии'),
    }
    return render(request, 'geography.html', context)


def skills_view(request):
    context = {
        'top_skills': get_object_or_404(Statistics, title='ТОП-20 навыков по годам для выбранной профессии'),
    }
    return render(request, 'skills.html', context)