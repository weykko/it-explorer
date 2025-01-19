import pandas as pd
import matplotlib.pyplot as plt
import django
import os
from io import BytesIO
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_explorer.settings')
django.setup()

from main_app.models import Statistics


def top_skills(df):
    df = df.dropna(subset='key_skills')
    df['year'] = df['published_at'].str.partition('-')[0].astype(int)

    key_skills = df['key_skills'].tolist()
    for i in range(len(key_skills)):
        key_skills[i] = key_skills[i].split('\n')

    skills_dict = dict()

    for skills in key_skills:
        for skill in skills:
            if skill in skills_dict:
                skills_dict[skill] = skills_dict[skill] + 1
            else:
                skills_dict[skill] = 1

    skills_df = pd.DataFrame.from_dict(skills_dict, orient='index', columns=['count'])
    skills_df.index.rename('Навык', inplace=True)
    skills_df = skills_df.sort_values(by=['count'], ascending=False).head(20)
    top20 = skills_df.index.values.tolist()

    key_skillses = []
    for year in range(2015, 2025):
        df = df.loc[df['year'] == year]
        key_skills = df['key_skills'].tolist()
        key_skillses.append(key_skills)

    table = pd.DataFrame()
    for key_skills in key_skillses:
        for i in range(len(key_skills)):
            key_skills[i] = key_skills[i].split('\n')

        skills_dict = dict()

        for skills in key_skills:
            for skill in skills:
                if skill in skills_dict and skill in top20:
                    skills_dict[skill] = skills_dict[skill] + 1
                else:
                    skills_dict[skill] = 1

        df = pd.DataFrame.from_dict(skills_dict, orient='index', columns=['count'])
        df.index.rename('skill', inplace=True)
        df = df.reset_index()
        df = df.sort_values(by=['count'], ascending=False).head(20)
        res = (df
               .assign(n=df.groupby('skill').cumcount())
               .pivot_table(index="n", columns='skill', values='count')
               .rename_axis(None))
        table = pd.concat([table, res])

    table.reset_index()
    table['year'] = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

    html = "<table border='1'>\n<tr><th>year</th>"
    for skill in top20:
        html += f"<th>{skill}</th>"
    html += "</tr>\n"
    table[top20] = table[top20].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    for index, row in table.iterrows():
        html += "<tr>"
        html += f"<td>{row['year']}</td>"
        for skill in top20:
            html += f"<td>{row[skill]}</td>"
        html += "</tr>\n"

    html += "</table>"

    statistic = Statistics.objects.create(
        title="Динамика ТОП-20 навыков по годам",
        table_data=html
    )

    fig, ax = plt.subplots(figsize=(10, 8))
    years = table['year']
    colors = plt.cm.tab20.colors
    for i, column in enumerate(table.columns[1:]):
        plt.plot(table['year'], table[column], label=column, color=colors[i % len(colors)])

    ax.legend(loc='upper left', fontsize=10)
    ax.set_xlabel('Год', fontsize=12)
    ax.set_ylabel('Количество упоминаний', fontsize=12)
    ax.grid(True)
    ax.set_xticks(years)

    plt.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    statistic.graph.save('skills_dynamic_by_year.png', ContentFile(buffer.read()), save=True)
    buffer.close()


def top_skills_prof(df):
    df = df.dropna(subset='key_skills')
    df['year'] = df['published_at'].str.partition('-')[0].astype(int)

    key_skills = df['key_skills'].tolist()
    for i in range(len(key_skills)):
        key_skills[i] = key_skills[i].split('\n')

    skills_dict = dict()

    for skills in key_skills:
        for skill in skills:
            if skill in skills_dict:
                skills_dict[skill] = skills_dict[skill] + 1
            else:
                skills_dict[skill] = 1

    skills_df = pd.DataFrame.from_dict(skills_dict, orient='index', columns=['count'])
    skills_df.index.rename('Навык', inplace=True)
    skills_df = skills_df.sort_values(by=['count'], ascending=False).head(20)
    top20 = skills_df.index.values.tolist()

    key_skillses = []
    for year in range(2015, 2025):
        df = df.loc[df['year'] == year]
        key_skills = df['key_skills'].tolist()
        key_skillses.append(key_skills)

    table = pd.DataFrame()
    for key_skills in key_skillses:
        for i in range(len(key_skills)):
            key_skills[i] = key_skills[i].split('\n')

        skills_dict = dict()

        for skills in key_skills:
            for skill in skills:
                if skill in skills_dict and skill in top20:
                    skills_dict[skill] = skills_dict[skill] + 1
                else:
                    skills_dict[skill] = 1

        df = pd.DataFrame.from_dict(skills_dict, orient='index', columns=['count'])
        df.index.rename('skill', inplace=True)
        df = df.reset_index()
        df = df.sort_values(by=['count'], ascending=False).head(20)
        res = (df
               .assign(n=df.groupby('skill').cumcount())
               .pivot_table(index="n", columns='skill', values='count')
               .rename_axis(None))
        table = pd.concat([table, res])

    table.reset_index()
    table['year'] = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

    html = "<table border='1'>\n<tr><th>year</th>"
    for skill in top20:
        html += f"<th>{skill}</th>"
    html += "</tr>\n"
    table[top20] = table[top20].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    for index, row in table.iterrows():
        html += "<tr>"
        html += f"<td>{row['year']}</td>"
        for skill in top20:
            html += f"<td>{row[skill]}</td>"
        html += "</tr>\n"

    html += "</table>"

    statistic = Statistics.objects.create(
        title="Динамика ТОП-20 навыков по годам для frontend-разработчика",
        table_data=html
    )

    fig, ax = plt.subplots(figsize=(10, 8))
    years = table['year']
    colors = plt.cm.tab20b.colors
    for i, column in enumerate(table.columns[1:]):
        plt.plot(table['year'], table[column], label=column, color=colors[i % len(colors)])

    ax.legend(loc='upper left', fontsize=10)
    ax.set_xlabel('Год', fontsize=12)
    ax.set_ylabel('Количество упоминаний', fontsize=12)
    ax.grid(True)
    ax.set_xticks(years)

    plt.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    statistic.graph.save('skills_dynamic_by_year_frontend.png', ContentFile(buffer.read()), save=True)
    buffer.close()


def main():
    df = pd.read_csv('vacancies_2024.csv', dtype = {
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

    top_skills(df)
    top_skills_prof(prof_df)


if __name__ == '__main__':
    currency_df = pd.read_csv('currency.csv')
    main()