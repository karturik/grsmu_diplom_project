from django.urls import path, include
from . import views
import notifications.urls

urlpatterns = [

    path('', views.staff, name='staff'),
    path('message/', views.message, name='message'),
    path('notification/', views.notification, name='notification'),
    path('comments/', views.comments_moderation, name='comments'),
    path('comment_delete/', views.comment_delete, name='comment_delete'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]