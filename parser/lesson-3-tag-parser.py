from bs4 import BeautifulSoup as bs4
from pprint import pprint
import requests as rq
import re
import os


"""
1) Необходимо собрать информацию о вакансиях на должность программиста или разработчика с сайта superjob.ru или hh.ru. (Можно с обоих сразу) 
Приложение должно анализировать несколько страниц сайта. Получившийся список должен содержать в себе: 
• Наименование вакансии, 
• Предлагаемую зарплату,
• Ссылку на саму вакансию

2) Доработать приложение таким образом, чтобы можно было искать разработчиков на разные языки программирования (Например Python, Java, C++)
"""

link_hh = 'https://hh.ru/search/vacancy'
get_params = {'area':1, 'text':'программист', 'page':1}

def get_page_data(page_url: str, params={}, headers={}):
    html_page = rq.get(page_url, params=params, headers=headers)
    return html_page

def write_result_to_file(text: str, file_name: str, params = {'mode':'w'}):
    with open(file_name, params['mode'], encoding="utf-8") as file:
        file_bytes = file.write(text)
    return file_bytes

def search_data(data, params = {}):
    soup = bs4(data)
    vacancies = soup.findAll('div',{'class':'vacancy-serp-item'})
    if len(vacancies) > 0:
        for v in vacancies:
            name_v = v.find('a', {'data-qa':'vacancy-serp__vacancy-title'}).string
            salary_v = v.find('div', {'data-qa':'vacancy-serp__vacancy-compensation'})
            if salary_v != None:
                salary_v = salary_v.text
            href_v = v.find('a',{'data-qa':'vacancy-serp__vacancy-title'}).get('href')
            vacancies_text = f'''
            =================================\n
            Наименование вакансии: {name_v}\n'
            Предлагаемая зарплата: {salary_v}\n
            Ссылка на вакансию: {href_v}\n
            =======================================\n
            '''
            print(vacancies_text)
            write_result_to_file(vacancies_text, file_vacancies,  {'mode':'a'})

def execute_request_write_to_file(link: str, num_page: int, params={}, headers={}):
    files = []
    for num_page in range(1,num_page+1):
        bytes_in_file = 0
        file_name = f'parser/data/html/hh_page_{num_page}.html'
        params['page'] = num_page
        html_page = get_page_data(link, params, headers)
        bytes_in_file = write_result_to_file(html_page.text,file_name)
        if bytes_in_file > 0:
            files.append((file_name, bytes_in_file))
    return files

def get_data(file_name):
    with open(file_name, 'r', encoding="utf-8") as file:
        file = file.read()
    return file

def get_num_file(path):
    return sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))

search_vacancy = 'программист'
path_to_files ='parser/data/html'
path_to_vacancies = 'parser/data/vacancies'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
file_vacancies = 'parser/data/vacancies/hh_vacancies.txt'

if __name__ == '__main__':
    
    files_count = get_num_file(path_to_files)
    
    if files_count == 0:
        print('Делаем запрос к ресурсу и получаем страницы =============================\n')
        params = get_params
        params['text'] = search_vacancy
        files = execute_request_write_to_file(link_hh, 10, params, headers)
        print('Сохраненнные страницы запроса:\n')
        pprint(files)
        print('\n=========================================================================\n')
    
    write_result_to_file('', file_vacancies)

    print('\nПарсинг необходимой информации ========================================\n')
    for file_name in os.listdir(path_to_files):
        data = get_data(path_to_files+"/"+file_name)
        search_data(data, params = {})

    print('\nОкончание программы ========================================\n')