import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
import re


def get_html(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    r = requests.get(url, headers=headers)
    if r.ok:
        return r.text

def refine_ang(ang1):
    ang = str.upper(ang1)
    intab = 'А, В, С, Е, Н, К, М, О, Р, Т, Х'
    outtab = 'A, B, C, E, H, K, M, O, P, T, X'
    trantab = ang.maketrans(intab,outtab)
    return ang.translate(trantab)

def refine_p(p):
    return p.replace(' ','')

def write_csv(data):
    with open('ufa_железная-мебель.csv', 'a',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['price']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    lis = soup.find_all('div', class_='item_info')

    for li in lis:
        try:
            ang = li.find('div', class_='item-title').find('a').text.strip()
            name = refine_ang(ang)
        except:
            name = ''

        try:
            p = li.find('div', class_='price_value_block').find('span', class_='price_value').text.strip()
            price = refine_p(p)
        except:
            price = ''
        data = {'name': name,
                'price': price}

        write_csv(data)

def konec(url):

    soup = BeautifulSoup(get_html(url), 'lxml')
    url1 = soup.find('div', class_='nums').find_all('a', class_="dark_link")
    for elem in url1:
        e = []
        e.append(elem)

    k = str(e[-1])
    c = re.compile('\d+')

    return int(c.findall(k)[-1])+1


def main():



    pattern = 'https://xn--80a1bd.xn----7sbenacbbl2bhik1tlb.xn--p1ai/catalog/metallicheskie-shkafy/?PAGEN_1={}'

    for i in range(1, konec(pattern)):
        url = pattern.format(str(i))
        get_page_data(get_html(url))

    pattern = 'https://xn--80a1bd.xn----7sbenacbbl2bhik1tlb.xn--p1ai/catalog/seyfy/?PAGEN_1={}'

    for i in range(0, konec(pattern)):
        url = pattern.format(str(i))
        get_page_data(get_html(url))


if __name__ == '__main__':
    main()





def save_function(article_list):
    print('starting')
    new_count = 0

    for article in article_list:
        try:
            News.objects.create(
                title = article['title'],
                link = article['link'],
                published = article['published'],
                source = article['source']
            )
            new_count += 1
        except Exception as e:
            print('failed at latest_article is none')
            print(e)
            break
    return print('finished')


import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import lxml


# функция скрапинга
@shared_task
def hackernews_rss():
    article_list = []
    try:
        print('Starting the scraping tool')
        # выполняем запрос, разбираем данные с помощью XML
        # разбираем данные в BS4
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')
        # выбираем из данных только "items", которые нам нужны
        articles = soup.findAll('item')

        # для каждого "item" разбираем его в список
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published_wrong = a.find('pubDate').text
            published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
            # выводим(published, published_wrong) # проверяем корректность формата даты
            # создаем объект "article" с данными
            # из каждого "item"
            article = {
                'title': title,
                'link': link,
                'published': published,
                'source': 'HackerNews RSS'
            }
            # добавляем "article_list" с каждым объектом "article"
            article_list.append(article)
            print('Finished scraping the articles')

            # после цикла передаем сохраненный объект в файл .txt
            return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)




# models.py
from django.db import models
# Здесь создаем модель.
class News(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2083, default="", unique=True)
    published = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=30, default="", blank=True, null=True)