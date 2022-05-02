from django.shortcuts import render
from .models import Teacher, Department, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from .forms import CommentForm
from django.contrib import messages


# SCRAPING
import requests
from bs4 import BeautifulSoup
from .forms import DepartmentAddForm


# Create your views here.
def demo_site_index(request):
    departments = Department.objects.all()
    context = {
        "departments": departments,
    }
    return render(request, "demo_site/demo_site_index.html", context)

def demo_site_department(request, department):
    teachers = Teacher.objects.filter(departments__title__contains=department)
    context = {
        "department": department,
        "teachers": teachers
    }
    return render(request, "demo_site/demo_site_department.html", context)

def demo_site_detail(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author = request.user,
                body = form.cleaned_data['body'],
                teacher = teacher
            )
            comment.save()
    comments = Comment.objects.filter(teacher=teacher).order_by('-created_on')
    context = {
        "teacher": teacher,
        "comments": comments,
        "form": form,
    }
    return render(request, "demo_site/demo_site_detail.html", context)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'demo_site/comment_deletion.html'
    def get_success_url(self):
        return reverse_lazy('demo_site_index')

    def test_func(self):
        comment = self.get_object()
        return str(self.request.user) == str(comment.author)

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'demo_site/comment_edit.html'
    def get_success_url(self):
        return reverse_lazy("demo_site_index")

    def test_func(self):
        comment = self.get_object()
        return str(self.request.user) == str(comment.author)

# SCRAPING
def info_scraping(request):
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
    if request.method == "POST":
        form = DepartmentAddForm(request.POST)
        if form.is_valid():
            for dep in new_dep_list:
                department = Department(title = dep)
                department.save()
            messages.success(request, ('Изменения сохранены!'))
    return render(request, "scraping/scraping_page.html", {'new_dep_list': new_dep_list, 'exist_dep_list': exist_dep_list})