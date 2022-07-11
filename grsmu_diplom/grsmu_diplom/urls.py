from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
import notifications.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name="main_page"),
    path('staff/', include("staff_only.urls")),
    path('moodle_test/', include("moodle_test.urls")),
    path('demo_site/', include("demo_site.urls")),
    path('user/', include("users.urls")),
    path('scraper/', include("scraper.urls")),
    path('rating/', include("rating.urls")),
    path('proxie/', include("proxie.urls")),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name="password_reset_done"),
    path("password_reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password_reset/finish/", auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name="password_reset_complete"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)