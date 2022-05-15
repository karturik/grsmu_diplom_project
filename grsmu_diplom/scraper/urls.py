from django.urls import path
from . import views

urlpatterns = [
path("", views.scraping, name="scraper"),
path("department/", views.department_scraping, name="dep-scraper"),
path("teacher/", views.teacher_scraping,name="teach-scraper"),
path("teacher/pic_update", views.teacher_pic_scraping, name="teach-pic-scraper"),
]