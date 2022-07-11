from django.urls import path
from . import views

urlpatterns = [
    path('', views.moodle_test_scrap, name="moodle_test_scrap"),

]