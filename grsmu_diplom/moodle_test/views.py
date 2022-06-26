from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import random
import re
import time
from .models import Question, Answer

proxies = [
'173.212.245.135:3128'

]

headers = [
    {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"},
    {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"},
    {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"},
    {"User-Agent":"Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"},
]

proxy=random.choice(proxies)
header=random.choice(headers)

# Create your views here.
time_intervals = [4, 5, 6 ,7, 8 , 9, 10]
time_interval = random.choice(time_intervals)

def moodle_test_add(request):
    questions = Question.objects.get(id=3)
    answers = questions.answers.all()
    ls =[]
    if request.method == "POST":
        q1 = Question(body="Test q", topic='Farma')
        q2 = Question(body="Test q2", topic='Nervy')
        print(questions.body)
        print(questions.subject)
        print(questions.topic)
        for answer in answers:
            print(answer.body)
        print(q1.body)
        print(q1.topic)
        q1.save()
        ls.append(q1)
        ls.append(q2)
        print(ls)
        for l in ls:
            if Question.objects.filter(body = l.body).exists():
                print('yes')
            else:
                print('no')
        # moodle_username = request.POST.get('moodle_username')
        # moodle_password = request.POST.get('moodle_password')
        # urls = request.POST.getlist('test_url')
        # login_data = {
        #     'username': moodle_username,
        #     'password': moodle_password}
        #
        # with requests.Session() as s:
        #     url = "http://edu.grsmu.by/login/index.php"
        #     r = s.get(url, proxies={"http": proxy, "https": proxy}, headers=header)
        #     print('подключаемся к логин пейдж')
        #     soup = BeautifulSoup(r.content, features="html.parser")
        #     login_data['form-control'] = soup.find('input', attrs={'class':'form-control'})['value']
        #     r = s.post(url, data=login_data)
        #     print('авторизация')
        #     if "http://edu.grsmu.by/user/profile.php?id" in str(r.content):
        #         print('Авторизация прошла')
        #         for link in urls:
        #             try:
        #                 print(url)
        #                 r = s.get(link, proxies={"http": proxy, "https": proxy}, headers=header)
        #                 print(r.text)
        #                 time.sleep(time_interval)
        #                 soup = BeautifulSoup(r.content, features="html.parser")
        #                 print(url, "тест получил")
        #                 questions = soup.find_all('div', class_="que multichoice deferredfeedback correct")
        #                 question_subject = soup.find('div', class_="page-header-headings").text
        #                 question_topic = soup.find_all('li', class_="breadcrumb-item")[-1].text
        #                 print(question_subject, question_topic)
        #                 for question in questions:
        #                     question_text = question.find('div', class_="qtext").text
        #                     question_text = question_text.replace('\n', '#').replace('##', ' ').replace(' ', '')
        #                     question_right_answer = question.find_all('div', {"class": re.compile(r'correct$')})
        #                     right_answer = ''
        #                     for answer in question_right_answer:
        #                         right_answer += "111" + answer.text
        #                     ls = right_answer.split('111')
        #                     ls.pop(0)
        #                     print(question_text,': ', ls)
        #             except Exception as e:
        #                 print(url, ' Ошибка', e)


    return render(request, 'moodle_test/moodle_test_add.html')

