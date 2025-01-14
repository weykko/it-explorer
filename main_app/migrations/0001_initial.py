# Generated by Django 5.1.5 on 2025-01-14 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountByCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, unique=True)),
                ('vacancy_count', models.IntegerField()),
                ('share', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CountByCityProf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, unique=True)),
                ('vacancy_count', models.IntegerField()),
                ('share', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CountByYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('vacancy_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CountByYearProf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('vacancy_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='graphs/')),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryByCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, unique=True)),
                ('average_salary', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SalaryByCityProf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, unique=True)),
                ('average_salary', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SalaryByYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('average_salary', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SalaryByYearProf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('average_salary', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TopSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('skill', models.CharField(max_length=100)),
                ('count', models.IntegerField()),
            ],
            options={
                'ordering': ['-year', '-count'],
                'unique_together': {('year', 'skill')},
            },
        ),
    ]
