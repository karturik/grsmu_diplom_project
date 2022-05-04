from django.shortcuts import render
from django.contrib import messages
from demo_site.models import Department, Teacher
from django import forms
from .forms import DepartmentAddForm, TeacherAddForm


# SCRAPING
import requests
from bs4 import BeautifulSoup
# from .forms import DepartmentAddForm

# Create your views here.
def department_scraping(request):
    url = "http://www.grsmu.by/ru/university/structure/chairs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    departments = soup.find_all("div", class_="category-item")
    exist_dep_list=[]
    new_dep_list=[]
    for dep in departments:
        title = dep.find('span').text
        if not Department.objects.filter(title=title).exists():
            new_dep_list.append(title)
        elif Department.objects.filter(title=title).exists():
            exist_dep_list.append(title)
# СОХРАНЕНИЕ НОВЫХ ОТДЕЛЕНИЙ ПО КНОПКЕ
    form = DepartmentAddForm(request.POST)
    if request.method == "POST":
        for dep in new_dep_list:
            title = dep
            department = Department(title=title)
            department.save()
        messages.success(request, ('Изменения сохранены!'))
    return render(request, "scraping/department_scraping_page.html", {'new_dep_list': new_dep_list, 'exist_dep_list': exist_dep_list, 'form':form})

def teacher_scraping(request):
    url = "http://www.grsmu.by/ru/university/structure/chairs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    departments = soup.find_all("div", class_="category-item")
    dep_list=[]
    link_list=[]
    for dep in departments:
        title = dep.find('span').text
        if title == 'Оториноларингологии и глазных болезней':
            dep_list.append('Кафедра оториноларингологии')
            dep_list.append('Кафедра глазных болезней')
        if title != 'Инфекционных болезней' and title !='Оториноларингологии и глазных болезней':
            dep_list.append(title)
        links = dep.find('a')['href']

        if '/chairs/cafedry_4' in links:
            link_list.append('http://www.grsmu.by'+links+'prof/')
        if 'chairs/cafedry_8' in links:
            link_list.append('http://www.grsmu.by'+links+'8_sostav/')
        if 'chairs/cafedry_10' in links:
            link_list.append('http://www.grsmu.by'+links+'pps/')
        if 'chairs/cafedry_19' in links:
            link_list.append('http://www.grsmu.by'+links+'cafedry_19_sostav/')
        if '/chairs/cafedry_25' in links:
            link_list.append('http://www.grsmu.by'+links+'prof/')
        if '/chairs/kafedry_28/' in links:
            link_list.append('http://www.grsmu.by'+links+'prof/')
        if '/chairs/cafedry_26/' in links:
            link_list.append('http://www.grsmu.by'+links+'prof/')
        if '/chairs/cafedry_21/' in links:
            link_list.append('http://www.grsmu.by'+links+'cafedry_21_sostav/')
        if '/chairs/kafedry_34/' in links:
            link_list.append('http://www.grsmu.by'+links+'otorinolaringology/sostav_ent/')
            link_list.append('http://www.grsmu.by'+links+'ophtalmology/sostav_eyes/')
        if 'ru/university/' in links:
            link_list.append('http://www.grsmu.by' + links + 'sostav/')
    a = 0
    all_info = []
    for link in link_list:
        department_info = {}
        url = link
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        teachers_info = soup.find_all("div", class_="inf")
        for teacher in teachers_info:
            name = teacher.find('a').text
            a += 1
            position = teacher.find('p').text
            department_info[name] = position
            if not department_info in all_info:
                all_info.append(department_info)

# ДОБАВЛЕНИЕ В БАЗУ ПО КНОПКЕ
    form = TeacherAddForm(request.POST)
    if request.method == "POST":
        # for dep in dep_list:
        #     department = dep
        #     if not Department.objects.filter(title=department).exists():
        #         Department(title=department).save()
        #     for i in all_info:
        #         for key, value in i.items():
        #             name = key
        #             position = value
        #             teacher = Teacher(department=Department.objects.get(title=department), name=name, position=position)
        #             if not Teacher.objects.filter(name=name, position=position).exists():
        #                 teacher.save()
        for i in range(len(dep_list)):
            department = dep_list[i]
            if not Department.objects.filter(title=department).exists():
                Department(title=department).save()
            for key, value in all_info[i].items():
                name = key
                position = value
                teacher = Teacher(department=Department.objects.get(title=department), name=name, position=position)
                if not Teacher.objects.filter(name=name, position=position).exists():
                    teacher.save()
        messages.success(request, ('Изменения сохранены!'))


    return render(request, "scraping/teacher_scraping_page.html", {'a':a ,'dep_list':dep_list,'link_list':link_list ,'all_info':all_info})