from django.urls import path
from . import views


urlpatterns = [
    path('', views.rating_main_page, name="rating_main_page"),
    path('departments/', views.rating_departments_page, name="rating_departments_page"),
    path('departments/<pk>', views.rating_department_detail_page, name="rating_department_detail_page"),
]