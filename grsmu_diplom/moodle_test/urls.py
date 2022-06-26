from django.urls import path
from . import views

urlpatterns = [
    path('', views.moodle_test_add, name="moodle_test_add"),
]