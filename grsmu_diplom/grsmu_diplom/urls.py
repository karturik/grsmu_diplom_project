from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo_site/', include("demo_site.urls")),
    path('user/', include("users.urls")),
    path("password_reset", views.password_reset_request, name="password_reset")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)