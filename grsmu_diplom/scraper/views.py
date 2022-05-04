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
        dep_list.append(title)
        links = dep.find('a')['href']
        if 'ru/university/' in links:
            link_list.append('http://www.grsmu.by'+links+'sostav/')
    a = int(len(link_list))
    all_info = []
    full_info = []
    for link in link_list:
        department_info_list = {}
        url = link
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        teachers_info = soup.find_all("div", class_="inf")
        for teacher in teachers_info:
            name = teacher.find('a').text
            position = teacher.find('p').text
            department_info_list[name] = position
            all_info.append(department_info_list)
    # for i in range(a):
    #     full_info[dep_list[i]] = all_info[i]
# ДОБАВЛЕНИЕ В БАЗУ ПО КНОПКЕ
#     form = TeacherAddForm(request.POST)
#     if request.method == "POST":
#         for i in range(a):
#             teacher = Teacher(department=dep_list[i], name=)
#             department = dep_list[i]
#             for teach in all_info[i]:
#                 name =

    return render(request, "scraping/teacher_scraping_page.html", {'full_info':full_info,'dep_list':dep_list ,'link_list':link_list, 'all_info':all_info})