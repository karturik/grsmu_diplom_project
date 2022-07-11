from django.shortcuts import render
from .models import Proxie

import random
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import threading

count = 0

headers = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"},
    {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"},
    {"User-Agent": "Microsoft Internet Explorer 6 / IE 6: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"},
    {"User-Agent": "Microsoft Internet Explorer 7 / IE 7: Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)"},
    {"User-Agent": "Microsoft Internet Explorer 8 / IE 8: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"},
    {"User-Agent": "Microsoft Internet Explorer 9 / IE 9: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)"},
    {"User-Agent": "Microsoft Internet Explorer 10 / IE 10: Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)"},
    {"User-Agent": "Apple iPhone: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"},
    {"User-Agent": "Googlebot (Google Search Engine Bot): Mozilla/5.0 (compatible; Googlebot/2.1; +What Is Googlebot | Google Search Central | Documentation | Google Developers)"},
]

header = random.choice(headers)

def site_proxies_scrap(url):
    r = requests.get(url, headers=header)
    print('подключаемся к странице с ip', url)
    soup = BeautifulSoup(r.content, features="html.parser")
    text_field = soup.find('textarea', class_="form-control").text
    ls = text_field.split("\n")
    ls_1 = ls[3:-1]
    with open("proxie/template/unchecked_proxies.txt", 'a', encoding="utf-8") as file:
        for i in ls_1:
            file.write(i+"\n")
        file.close()

def site1_proxies_scrap(url):
    r = requests.get(url, headers=header)
    print('подключаемся к странице с ip', url)
    soup = BeautifulSoup(r.content, features="html.parser")
    ls = str(soup.text).replace("\r", '').split("\n")
    ls_1 = ls[:-1]
    with open("proxie/template/unchecked_proxies.txt", 'a', encoding="utf-8") as file:
        for i in ls_1:
            file.write(i+"\n")
        file.close()


def doubler(proxy, ):
    with open('proxie/template/checked_proxies.txt', 'a', encoding='utf-8') as file:
        try:
            page = requests.get('https://ipecho.net/plain', timeout=5, proxies={"http": proxy, "https": proxy}, headers=header)
            file.write(proxy + '\n')
            print('Status OK: ', proxy)
            try:
                Proxie(ip=proxy).save()
            except:
                pass
        except OSError as e:
            pass
            print(e, proxy)

def db_proxies_checker(proxy, ):
    try:
        page = requests.get('https://ipecho.net/plain', timeout=5, proxies={"http": proxy, "https": proxy}, headers=header)
        print('Status OK: ', proxy)
    except OSError as e:
        try:
            page = requests.get('https://ipecho.net/plain', timeout=5, proxies={"http": proxy, "https": proxy},
                                headers=header)
            print('Status OK: ', proxy)
        except:
            print(proxy, 'не работает')
            Proxie.objects.get(ip=proxy).delete()


def proxie_update(request):
    with open('proxie/template/checked_proxies.txt', 'w', encoding='utf-8') as file:
        file.close()
    with open('proxie/template/unchecked_proxies.txt', 'w', encoding='utf-8') as file:
        file.close()
    site_proxies_scrap("https://www.sslproxies.org/")
    site_proxies_scrap("https://free-proxy-list.net/#list")
    site_proxies_scrap("https://free-proxy-list.net/anonymous-proxy.html")
    site1_proxies_scrap("https://api.proxyscrape.com/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    with open('proxie/template/unchecked_proxies.txt', 'r', encoding='utf-8') as file:
        proxies = file.read().split("\n")
        file.close()
    for proxy in proxies:
        my_thread = threading.Thread(target=doubler, args=(proxy, ))
        my_thread.start()
    return HttpResponse('Парсинг прокси завершен!')

def proxies_check(request):
    proxies = Proxie.objects.all()
    for proxy in proxies:
        my_thread = threading.Thread(target=db_proxies_checker, args=(proxy.ip, ))
        my_thread.start()
    return HttpResponse('Проверка прокси в бд завершена!')