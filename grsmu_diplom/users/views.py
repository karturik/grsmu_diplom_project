from django.shortcuts import render, redirect
from .models import Profile
from demo_site.models import Comment
from .forms import NewUserForm, UserForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

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


# Create your views here.
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            request.user.profile_pic = profile_form.cleaned_data.get('profile_pic')
            profile_form.save()
            user_form.save()
            #обновляет логин в "автор комментариев"
            for comment in comments:
                comment.author = str(request.user)
                comment.save()
            messages.success(request, ('Изменения сохранены!'))
        else:
            messages.error(request, ('Не удалось сохранить изменения'))
        return redirect ('/user/profile')
    user_form = UserForm(instance = request.user)
    profile_form = ProfileForm(instance = request.user.profile)
    context = {
        "user": request.user,
        "user_form": user_form,
        "profile_form": profile_form,
        "comments": comments,
    }
    return render(request=request, template_name='users/profile_page.html', context=context)

# password reset functions
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
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
                        send_mail(subject, email, 'grsmu.check@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})