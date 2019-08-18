from pprint import pprint
import requests
import re
import os

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
    return words

def get_paragraph_text(html_content, pattern_paragraph):
    paragraph = re.findall(f'{pattern_paragraph}',html_content)
    print(paragraph[0])
    return paragraph[0]

def get_links_text(html_content, pattern_links):
    words = re.findall(f'{pattern_links}',html_content)
    return words

def get_html_content(topic):
    html_content = get_topic_page(topic)
    return html_content

def get_common_words(topic):
    html_content = get_html_content(topic)
    html_content = get_paragraph_text(html_content, pattern_paragraph)
    words_list = get_links_text(html_content, pattern_links)
    rate={}
    for word in words_list:
        if word in rate:
            rate[word]+=1
        else:
            rate[word]=1
    rate_list = list(rate.items())
    rate_list.sort(key = lambda x: -x[1])
    return rate_list

def write_result_to_file(text: str, file_name: str, param = {}):
    with open(file_name, 'w', encoding="utf-8") as file:
        file_text = file.write(text)
    return file_text

pattern_paragraph = r'id=\"Ссылки\"[\s\S]*?class=\"navbox|printfooter\"'
pattern_links = r'<a.*nofollow.*?external.*?href=\"(.*?)\">(.*?)</a>'
topic = 'Python'
file_name = 'parser/data/links_from_wiki.txt'

if __name__ == '__main__':
    list_result = get_common_words(topic)
    pprint(list_result [:10])
    separator = str('\n')
    text = separator.join([f'link : {items[0][0]} - text : {items[0][1]}' for items in list_result])
    print(text)
    write_result_to_file(text, file_name)
    