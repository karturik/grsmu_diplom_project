from django.urls import path
from . import views

urlpatterns = [
path("refrash/department/", views.department_scraping, name="dep-scraper"),
path("refrash/teacher/", views.teacher_scraping, name="teach-scraper"),
]