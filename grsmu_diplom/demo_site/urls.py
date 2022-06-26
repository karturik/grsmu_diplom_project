from django.urls import path
from django.urls import re_path as url
from . import views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy



urlpatterns = [
    path("", views.demo_site_index, name="demo_site_index"),
    path("teacher/<int:pk>/", views.demo_site_detail, name="demo_site_detail"),
    path("department/<pk>", views.demo_site_department, name="demo_site_department"),
    path("search/", views.searching, name="searching"),
    path('likes/', views.likes, name='likes'),
    path('dislikes/', views.dislikes, name='dislikes'),
    path('vote/', views.voting, name='voting'),
]