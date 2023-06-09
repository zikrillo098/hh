import requests
from bs4 import BeautifulSoup

job = input(str(':: '))
url = 'https://hh.ru/search/vacancy?text=python&'
params = {
    'L_save_area': 'true',
    'clusters': 'true',
    'search_field': 'name',
    'area': '1',
    'enable_snippets': 'true',
    'salary': '',
    'st': 'searchVacancy',
    'text': f'{job}',  # Здесь указываем поисковую фразу
    'page': '1'
}
print(params)
response = requests.get(url.replace('python', job), params=params)
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все элементы с классом "vacancy-serp-item"
vacancy_items = soup.find_all('div', {
    'class': "class=bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-13"})
print(vacancy_items)

vacancy = []  # Создаем объекты вакансий и отправляем их в бот
for item in vacancy_items:
    title = item.find('a', {'class': 'serp-item__title'}).text
    print(title)
    company = item.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'}).text
    salary = item.find('div', {'class': 'bloko-header-section-3'})
    if salary:
        salary = salary.text.replace(u'\xa0', u' ')
    else:
        salary = 'З/П не указана'
    print(title, company, salary)
    # Создаем объект вакансии и отправляем его в бот
    vacancy.append(f'Название вакансии: {title}\nКомпания: {company}\nЗарплата: {salary}\n---\n')
print(vacancy)
