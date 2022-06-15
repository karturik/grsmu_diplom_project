from django.shortcuts import render, redirect
from .models import Profile
from demo_site.models import Comment
from .forms import NewUserForm, UserForm, ProfileForm, StudentVerificationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
import requests
from django.contrib.auth.decorators import login_required

#password reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

#MOODLE check
from bs4 import BeautifulSoup

#PAGINATION
from django.core.paginator import Paginator

#SORTING
from django.db.models import Count


# Create your views here.
def register_request(request):
    if not Group.objects.filter(name='Student').exists():
        Group.objects.create(name='Student')
        Group.objects.create(name='Not_student')
    Student_group = Group.objects.get(name='Student')
    Not_student_group = Group.objects.get(name='Not_student')
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Not_student_group)
            login(request, user)
            messages.success(request, "Регистрация прошла успешно")
            return redirect("demo_site_index")
        messages.error(request, "Ошибка. Неверно введенная информация")
    form = NewUserForm()
    return render (request=request, template_name="users/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли в аккаунта {username}")
                return redirect("demo_site_index")
            else:
                messages.error(request, "Неверный логин или пароль")
        else:
            messages.error(request, "Неверный логин или пароль")
    form = AuthenticationForm()
    return render(request=request, template_name="users/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта")
    return redirect("demo_site_index")

def profile_page(request):
    comments = Comment.objects.filter(author=request.user).order_by('-created_on')
    comment_list = Comment.objects.filter(author=request.user).order_by('-created_on')

    sort_by = request.GET.get("sort")
    if sort_by == "likes":
        comment_list = Comment.objects.filter(author=request.user).annotate(cnt=Count('likes')).order_by('-cnt')
    elif sort_by == "date":
        comment_list = Comment.objects.filter(author=request.user).order_by('created_on')

    paginator = Paginator(comment_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    profile_pics_list = ['images/teacher.jpg', 'images/van.jpg', 'images/1.jpg', 'images/user.jpg']
    if request.method == "POST":
        #кнопка "изменить данные профиля"
        if "user_change" in request.POST:
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            #обновление картинки профиля
            if user_form.is_valid() and profile_form.is_valid():
                request.user.profile.profile_pic = request.POST.get('picture-name')
                profile_form.save()
                user_form.save()
                #обновляет логин в "автор комментариев"
                messages.success(request, ('Изменения сохранены!'))
            else:
                messages.error(request, ('Не удалось сохранить изменения'))
            return redirect ('/user/profile')
        #кнопка "удалить комментарий"
        elif "comment_delete" in request.POST:
            comment_pk = request.POST.get('comment_pk')
            comment = Comment.objects.filter(pk=comment_pk)
            comment.delete()
        # MOODLE CHECK
        if "acc_verification" in request.POST:
            Student_group = Group.objects.get(name='Student')
            moodle_form = StudentVerificationForm(request.POST)
            #вытягиваем логин и пароль из формы
            if moodle_form.is_valid():
                moodle_username = moodle_form.cleaned_data['username']
                moodle_password = moodle_form.cleaned_data['password']
                login_data = {
                        'username': moodle_username,
                        'password': moodle_password}
                #делаем гет и пост запросы, возвращаем результат
                with requests.Session() as s:
                      url = "http://edu.grsmu.by/login/index.php"
                      r = s.get(url)
                      soup = BeautifulSoup(r.content)
                      login_data['form-control'] = soup.find('input', attrs={'class':'form-control'})['value']
                      r = s.post(url, data=login_data)
                      #если запрос прошел - переводим в новую группу
                      if "http://edu.grsmu.by/user/profile.php?id" in str(r.content):
                          request.user.groups.clear()
                          request.user.groups.add(Student_group)
                          messages.info(request, "Аккаунт подтвержден!")
                          return redirect('users:profile')
                      else:
                          messages.error(request, "Логин или пароль неверный.")
            else:
                messages.error(request, "Логин или пароль неверный.")



    user_form = UserForm(instance = request.user)
    profile_form = ProfileForm(instance = request.user.profile)
    moodle_form = StudentVerificationForm(request.POST)
    group = str(request.user.groups.get())
    context = {
        "user": request.user,
        "user_form": user_form,
        "profile_form": profile_form,
        "comments": comments,
        "group": group,
        "moodle_form": moodle_form,
        "page_obj": page_obj,
        "profile_pics_list": profile_pics_list,
        "sort_by": sort_by,
    }

    return render(request=request, template_name='users/profile_page.html', context=context, )

# password reset functions
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Восстановление пароля"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'GRSMU-check',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'grsmu.check@mail.ru', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Произошла ошибка.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

@login_required(login_url='/user/login/')
def profile_delete(request):
    user = request.user
    if request.method == "POST":
        user = User.objects.get(id = user.id)
        user.delete()
        messages.error(request, "Аккаунт удален")
        return redirect ("/")
    return render(request=request, template_name="users/profile_delete.html")
