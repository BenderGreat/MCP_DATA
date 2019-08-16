from pprint import pprint
import requests
import re

def get_link(topic):
    link='https://ru.wikipedia.org/wiki/'+topic.capitalize()
    print(f'{link}')
    return link

def get_topic_page(topic):
    link = get_link(topic)
    html = requests.get(link).text
    return html

def get_topic_text(topic):
    html_content = get_topic_page(topic)
    words = re.findall("[а-яА-Я]{4,}",html_content)
    #text = ' '.join(words)
    return words

def get_links_text(topic):
    html_content = get_topic_page(topic)
    words = re.findall('(id="Ссылки".*)',html_content)
    #text = ' '.join(words)
    return words

# text = get_topic_text('Р”РµСЂРµРІРѕ')
# print(len(text))
# print(text[0:1000])

def get_common_words(topic):
    words_list = get_links_text(topic)
    rate={}
    for word in words_list:
        if word in rate:
            rate[word]+=1
        else:
            rate[word]=1
    rate_list = list(rate.items())
    rate_list.sort(key = lambda x: -x[1])
    return rate_list

if __name__ == '__main__':
    dict1 = get_common_words('Python')
    pprint(dict1[:10])