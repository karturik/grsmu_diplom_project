from django.urls import path
from django.urls import re_path as url
from . import views
from .views import CommentEditView\
    # , CommentDeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy



urlpatterns = [
    path("", views.demo_site_index, name="demo_site_index"),
    path("teacher/<int:pk>/", views.demo_site_detail, name="demo_site_detail"),
    path("department/<pk>", views.demo_site_department, name="demo_site_department"),
    # path("comment/<int:pk>/deletion/", view=login_required(CommentDeleteView.as_view(), login_url=reverse_lazy('users:login')), name="comment_deletion"),
    path("comment/<int:pk>/edit/", CommentEditView.as_view(), name="comment_edit"),
    path("search/", views.searching, name="searching"),
    path('likes/', views.likes, name='likes'),
    path('dislikes/', views.dislikes, name='dislikes'),
    path('comments/', views.comments, name='comments'),
]