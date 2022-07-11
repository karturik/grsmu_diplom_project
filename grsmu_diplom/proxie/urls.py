from django.urls import path
from . import views



urlpatterns = [
    path("update/", views.proxie_update, name="proxie_update"),
    path("proxies_check/", views.proxies_check, name="proxies_check"),
]