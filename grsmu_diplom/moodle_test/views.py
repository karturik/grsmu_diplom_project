from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import random
import re
import time
from .models import Question, Answer
from proxie.models import Proxie
import threading
from django.http import HttpResponse

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

# proxy=random.choice(proxies)
header=random.choice(headers)

# Create your views here.
time_intervals = [4, 5, 6 ,7, 8 , 9, 10]
time_interval = random.choice(time_intervals)

def moodle_test_scrap(request):
    if request.method == 'POST':
        db_questions_list = Question.objects.all()
        db_answers_list = Answer.objects.all()
        proxies_list = Proxie.objects.values_list('ip', flat=True)
        proxy = random.choice(proxies_list)
        header = random.choice(headers)

        moodle_username = request.POST.get('moodle_username')
        moodle_password = request.POST.get('moodle_password')
        urls = request.POST.getlist('test_url')
        login_data = {
            'username': moodle_username,
            'password': moodle_password}

        with requests.Session() as s:
            url = "http://edu.grsmu.by/login/index.php"
            try:
                r = s.get(url, proxies={"http": proxy, "https": proxy}, headers=header)
                print('подключаемся к логин пейдж')
            except OSError as e:
                return HttpResponse('Ошибка ip, попробуйте обновить страницу','\n',e)

            soup = BeautifulSoup(r.content, features="html.parser")
            login_data['form-control'] = soup.find('input', attrs={'class':'form-control'})['value']
            r = s.post(url, data=login_data)
            print('авторизация')
            if "http://edu.grsmu.by/user/profile.php?id" in str(r.content):
                print('Авторизация прошла')
                for link in urls:
                    try:
                        proxy = random.choice(proxies_list)
                        header = random.choice(headers)
                        print(link)
                        r = s.get(link, proxies={"http": proxy, "https": proxy}, headers=header)
                        # print(r.text)
                        soup = BeautifulSoup(r.content, features="html.parser")
                        print(url, "тест получил")
                        questions = soup.find_all('div', class_="que multichoice deferredfeedback correct")
                        question_subject = soup.find('div', class_="page-header-headings").text
                        question_topic = soup.find_all('li', class_="breadcrumb-item")[-1].text
                        print(question_subject, question_topic)
                        for question in questions:
                            question_text = question.find('div', class_="qtext").text
                            question_text = question_text.replace('\n', '#').replace('##', ' ').replace(' ', '')
                            try:
                                new_question = Question.objects.get(body=question_text, subject=question_subject, topic=question_topic)
                            except:
                                new_question = Question(body=question_text, subject=question_subject, topic=question_topic)
                                new_question.save()
                            question_right_answer = question.find_all('div', {"class": re.compile(r'correct$')})
                            # right_answer = ''
                            for answer in question_right_answer:
                                answer_text = answer.text
                                try:
                                    answer = Answer.objects.get(body=answer_text)
                                except:
                                    answer = Answer(body=answer_text)
                                    answer.save()
                                new_question.answers.add(answer)

                    except Exception as e:
                        print(url, ' Ошибка', e)
            else:
                print("Авторизация не прошла")
    return render(request, 'moodle_test/moodle_test_add.html')


