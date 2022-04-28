from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile_page, name="profile"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name="password_reset_done"),
    path("password_reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password_reset/finish/", auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name="password_reset_complete"),
]
