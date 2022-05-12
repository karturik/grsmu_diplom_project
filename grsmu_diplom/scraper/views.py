from django.shortcuts import render
from django.contrib import messages
from demo_site.models import Department, Teacher
from django import forms
from .forms import DepartmentAddForm, TeacherAddForm


# SCRAPING
import requests
from bs4 import BeautifulSoup
# from .forms import DepartmentAddForm

# IMAGE SCRAPING
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import os
from django.template.defaultfilters import slugify
from django.core.files import File

# Create your views here.
def scraping(request):
    return render (request, "scraping/scraping.html")

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
    dep_list = []
    new_dep_list = []
    old_dep_list = []
    link_list = []
    a = -3
    all_info = []
    name_list = []
    new_names = []
    teacher_count = Teacher.objects.all().count()
    base_department_count = Department.objects.all().count()
    if request.method == "POST":
        url = "http://www.grsmu.by/ru/university/structure/chairs/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        departments = soup.find_all("div", class_="category-item")
        for dep in departments:
            title = dep.find('span').text
            if title == 'Оториноларингологии и глазных болезней':
                dep_list.append('Кафедра оториноларингологии')
                dep_list.append('Кафедра глазных болезней')
            if title != 'Инфекционных болезней' and title != 'Оториноларингологии и глазных болезней':
                dep_list.append(title)
            if not Department.objects.filter(title=title).exists() and title != 'Инфекционных болезней' and title != 'Оториноларингологии и глазных болезней':
                new_dep_list.append(title)
            else:
                old_dep_list.append(title)
            links = dep.find('a')['href']
            if '/chairs/cafedry_4' in links:
                link_list.append('http://www.grsmu.by' + links + 'prof/')
            if 'chairs/cafedry_8' in links:
                link_list.append('http://www.grsmu.by' + links + '8_sostav/')
            if 'chairs/cafedry_10' in links:
                link_list.append('http://www.grsmu.by' + links + 'pps/')
            if 'chairs/cafedry_19' in links:
                link_list.append('http://www.grsmu.by' + links + 'cafedry_19_sostav/')
            if '/chairs/cafedry_25' in links:
                link_list.append('http://www.grsmu.by' + links + 'prof/')
            if '/chairs/kafedry_28/' in links:
                link_list.append('http://www.grsmu.by' + links + 'prof/')
            if '/chairs/cafedry_26/' in links:
                link_list.append('http://www.grsmu.by' + links + 'prof/')
            if '/chairs/cafedry_21/' in links:
                link_list.append('http://www.grsmu.by' + links + 'cafedry_21_sostav/')
            if '/chairs/kafedry_34/' in links:
                link_list.append('http://www.grsmu.by' + links + 'otorinolaringology/sostav_ent/')
                link_list.append('http://www.grsmu.by' + links + 'ophtalmology/sostav_eyes/')
            if 'ru/university/' in links:
                link_list.append('http://www.grsmu.by' + links + 'sostav/')

        for link in link_list:
            department_info = {}
            url = link
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            teachers_info = soup.find_all("div", class_="inf")
            for teacher in teachers_info:
                a += 1
                name = teacher.find('a').text
                if not Teacher.objects.filter(name=name).exists():
                    new_names.append(name)
                else:
                    name_list.append(name)
                position = teacher.find('p').text
                department_info[name] = position
                if not department_info in all_info:
                    all_info.append(department_info)

# ДОБАВЛЕНИЕ В БАЗУ ПО КНОПКЕ
        form = TeacherAddForm(request.POST)
        if "data-save" in request.POST:
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
    grsmu_dep_count = len(dep_list)
    context = {
        'a': a,
        'dep_list': dep_list,
        'link_list': link_list,
        'all_info': all_info,
        'name_list': name_list,
        'new_names': new_names,
        'teacher_count':teacher_count,
        'base_department_count':base_department_count,
        'new_dep_list':new_dep_list,
        'old_dep_list':old_dep_list,
        'grsmu_dep_count':grsmu_dep_count,
    }

    return render(request, "scraping/teacher_scraping_page.html", context)

def teacher_pic_scraping(request):
    dep_list = []
    link_list = []
    teach_link_list = []
    a = 0
    all_info = []
    pictures = {}
    if request.method == "POST":
        # ПОЛУЧАЕМ ССЫЛКИ НА СТРАНИЦУ КАФЕДРЫ
        url = "http://www.grsmu.by/ru/university/structure/chairs/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        departments = soup.find_all("div", class_="category-item")
        # ФОРМИРУЕМ ССЫЛКИ НА ПРОФ.СОСТАВ
        for dep in departments:
            links = dep.find('a')['href']
            if '/chairs/cafedry_4' or 'chairs/cafedry_8' or 'chairs/cafedry_10' or 'chairs/cafedry_19' or '/chairs/cafedry_25' or '/chairs/kafedry_28/' or '/chairs/cafedry_26/' or '/chairs/cafedry_21/' or '/chairs/kafedry_34/' or 'infekcii-grodno.wixsite' in links:
                if '/chairs/cafedry_4' in links:
                    link_list.append('http://www.grsmu.by'+links+'prof/')
                    break
                elif 'chairs/cafedry_8' in links:
                    link_list.append('http://www.grsmu.by'+links+'8_sostav/')
                    break
                elif 'chairs/cafedry_10' in links:
                    link_list.append('http://www.grsmu.by'+links+'pps/')
                    break
                elif 'chairs/cafedry_19' in links:
                    link_list.append('http://www.grsmu.by'+links+'cafedry_19_sostav/')
                    break
                elif '/chairs/cafedry_25' in links:
                    link_list.append('http://www.grsmu.by'+links+'prof/')
                    break
                elif '/chairs/kafedry_28/' in links:
                    link_list.append('http://www.grsmu.by'+links+'prof/')
                    break
                elif '/chairs/cafedry_26/' in links:
                    link_list.append('http://www.grsmu.by'+links+'prof/')
                    break
                elif '/chairs/cafedry_21/' in links:
                    link_list.append('http://www.grsmu.by'+links+'cafedry_21_sostav/')
                    break
                elif '/chairs/kafedry_34/' in links:
                    link_list.append('http://www.grsmu.by'+links+'otorinolaringology/sostav_ent/')
                    link_list.append('http://www.grsmu.by'+links+'ophtalmology/sostav_eyes/')
                    break
                elif 'infekcii-grodno.wixsite' in links:
                    pass
                break
            else:
                    link_list.append('http://www.grsmu.by' + links + 'sostav/')
        for link in link_list:
            url = link
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            teachers_info = soup.find_all("div", class_="inf")
            for teacher in teachers_info:
                teach_link = teacher.find('a')['href']
                a += 1
                teach_link_list.append("http://www.grsmu.by"+teach_link)
        pictures = {}
        for item in teach_link_list:
            url = item
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            name = soup.h1.string
            img_link = "http://www.grsmu.by" + soup.find(class_="img")['href']
            pictures[name] = img_link
        for key, value in pictures.items():
            teacher = Teacher(name=key)
            image_url = value
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            teacher.teacher_img.save("image_%s" % teacher.pk, File(img_temp))
            teacher.save()



        #     teacher(image_src=value).save()
            # if self.url and not self.photo:
            #     result = urllib.urlretrieve(self.url)
            #     self.photo.save(
            #         os.path.basename(self.url),
            #         File(open(result[0], 'rb'))
            #     )
            #     self.save()


            # string = "{}".format(name)
            # slug = slugify(string)
            # img_temp = NamedTemporaryFile(delete=True)
            # img_temp.write(urlopen(img_link).read())
            # img_temp.flush()
            # filename, file_extension = os.path.splitext(img_link)
            # teacher.image_src.save(img_link)
            # teacher.teacher_img.save(f"{slug}{file_extension}", File(img_temp))

# ДОЕНИЕ В БАЗУ ПО КНОПКЕ
#         form = TeacherAddForm(request.POST)
#         if "data-save" in request.POST:
#             for i in range(len(dep_list)):
#                 department = dep_list[i]
#                 if not Department.objects.filter(title=department).exists():
#                     Department(title=department).save()
#                 for key, value in all_info[i].items():
#                     name = key
#                     position = value
#                     teacher = Teacher(department=Department.objects.get(title=department), name=name, position=position)
#                     if not Teacher.objects.filter(name=name, position=position).exists():
#                         teacher.save()
#             messages.success(request, ('Изменения сохранены!'))


    return render(request, "scraping/teacher_pic_scraping_page.html", {"a":a,"teach_link_list":teach_link_list, "pictures":pictures})