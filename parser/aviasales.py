from pprint import pprint
import requests
import sys
import json
import re
import yaml
from urllib.request import urlopen

"""
Определяем ip адрес пользователя для опредления местоположения
"""
def get_public_ip():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

"""
Поиск билетов по направлению
"""
def get_ticket_matrix(from_city_iata:str, to_city_iata:str):
    link = f'{service}origin={from_city_iata}&destination={to_city_iata}&one_way=true'
    print(f'Link get ticket from to: {link}\n')
    req = requests.get(link)
    data = json.loads(req.text)
    for i in data['best_prices']:
        print(i['value'],i['depart_date'],i['return_date'],i['gate'])

"""
Определение кода IATA
"""
def get_iata_code(from_city:str, to_city:str):
    link = f'{service_iata}q=from {from_city} to {to_city}'
    print(f'Link get iata code: {link}\n')
    req = requests.get(link)
    data = json.loads(req.text)
    return (data['origin']['iata'], data['destination']['iata'])

"""
Определение местоположения пользователя по ip
"""
def get_locate_by_ip(user_ip):
    link = f'{service_get_locate_by_ip}locale=ru&callback=user_location_iata&ip={user_ip}'
    print(f'Link get location by ip: {link}\n')
    req = requests.get(link)
    user_location = json.loads(re.findall('(\{.*\})', req.text)[0])
    return (user_location['name'],user_location['iata'])

"""
Задаем задаем адреса GET запросов API для получения необходимых данных
"""
# Адрес GET запроса поиска стоимоти билетов
service = 'http://min-prices.aviasales.ru/calendar_preload?'

# Адрес GET запроса для определения кода IATA по названию города
service_iata = 'https://www.travelpayouts.com/widgets_suggest_params?'

# Адрес GET запроса для определения местоположния по ip пользователя
service_get_locate_by_ip = 'http://www.travelpayouts.com/whereami?'

print(f'START =========================================================================\n')

city_from = 'Москва'
city_to = 'Бангкок'
user_ip = get_public_ip()
print(f'User ip: {user_ip}\n')
user_city_from, user_iata_loc = get_locate_by_ip(user_ip)
print(f'User iata location code: {user_iata_loc}\n')
if user_iata_loc !=None and user_city_from !=None:
        from_city_iata = user_iata_loc
        city_from = user_city_from
from_city_iata, to_city_iata = get_iata_code(city_from, city_to)
print(f'From: City - {city_from}, City iata - {from_city_iata}\n')
print(f'To: City - {city_to}, City iata - {to_city_iata}\n')
get_ticket_matrix(from_city_iata, to_city_iata)

print(f'END =========================================================================\n')


