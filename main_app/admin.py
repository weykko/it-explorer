from django.contrib import admin
from .models import (SalaryByYear, SalaryByCity, CountByYear, CountByCity, SalaryByYearProf, SalaryByCityProf,
                     CountByYearProf, CountByCityProf, Graph, TopSkills)

admin.site.register(SalaryByYear)
admin.site.register(SalaryByCity)
admin.site.register(CountByYear)
admin.site.register(CountByCity)
admin.site.register(SalaryByYearProf)
admin.site.register(SalaryByCityProf)
admin.site.register(CountByYearProf)
admin.site.register(CountByCityProf)
admin.site.register(Graph)
admin.site.register(TopSkills)