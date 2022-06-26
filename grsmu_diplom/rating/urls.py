from django.urls import path
from . import views


urlpatterns = [
    path('', views.rating_main_page, name="rating_main_page"),
]