from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),
    path('demand/', views.demand, name='demand'),
    path('geography/', views.geography, name='geography'),
    path('skills/', views.skills, name='skills'),
    path('latest_vacancies/', views.latest_vacancies, name='latest_vacancies'),
]
