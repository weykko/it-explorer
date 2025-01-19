from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Главная страница
    path('general-statistics/', views.general_view, name='general_statistics'),  # Общая статистика
    path('demand/', views.demand_view, name='demand'),  # Востребованность
    path('geography/', views.geography_view, name='geography'),  # География
    path('skills/', views.skills_view, name='skills'),  # Навыки
]