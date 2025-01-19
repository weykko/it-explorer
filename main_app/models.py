from django.db import models


# Create your models here.

class Statistics(models.Model):
    title = models.CharField(max_length=255)
    table_data = models.TextField()  # HTML representation of the table
    # graph = models.ImageField(upload_to='graphs/')

    def __str__(self):
        return self.title


# class Graph(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='graphs/')
#     description = models.TextField(blank=True)
#
#     def __str__(self):
#         return self.title
#
#
# # Модели для общего анализа
# class SalaryByYear(models.Model):
#     year = models.IntegerField(unique=True)
#     average_salary = models.FloatField()
#
#     def __str__(self):
#         return f"{self.year}: {self.average_salary} руб"
#
#
# class CountByYear(models.Model):
#     year = models.IntegerField(unique=True)
#     vacancy_count = models.IntegerField()
#
#     def __str__(self):
#         return f"{self.year}: {self.vacancy_count} вакансий"
#
#
# class SalaryByCity(models.Model):
#     city = models.CharField(max_length=100, unique=True)
#     average_salary = models.FloatField()
#
#     def __str__(self):
#         return f"{self.city}: {self.average_salary} руб"
#
#
# class CountByCity(models.Model):
#     city = models.CharField(max_length=100, unique=True)
#     vacancy_count = models.IntegerField()
#     share = models.FloatField()
#
#     def __str__(self):
#         return f"{self.city}: {self.vacancy_count} вакансий, доля {self.share:.2%}"
#
#
# # Модели для анализа профессии
# class SalaryByYearProf(models.Model):
#     year = models.IntegerField(unique=True)
#     average_salary = models.FloatField()
#
#     def __str__(self):
#         return f"{self.year}: {self.average_salary} руб"
#
#
# class CountByYearProf(models.Model):
#     year = models.IntegerField(unique=True)
#     vacancy_count = models.IntegerField()
#
#     def __str__(self):
#         return f"{self.year}: {self.vacancy_count} вакансий"
#
#
# class SalaryByCityProf(models.Model):
#     city = models.CharField(max_length=100, unique=True)
#     average_salary = models.FloatField()
#
#     def __str__(self):
#         return f"{self.city}: {self.average_salary} руб"
#
#
# class CountByCityProf(models.Model):
#     city = models.CharField(max_length=100, unique=True)
#     vacancy_count = models.IntegerField()
#     share = models.FloatField()
#
#     def __str__(self):
#         return f"{self.city}: {self.vacancy_count} вакансий, доля {self.share:.2%}"
#
#
# class TopSkills(models.Model):
#     year = models.IntegerField()
#     skill = models.CharField(max_length=100)
#     count = models.IntegerField()
#
#     class Meta:
#         unique_together = ('year', 'skill')
#         ordering = ['-year', '-count']
#
#     def __str__(self):
#         return f"{self.year} - {self.skill}: {self.count}"
