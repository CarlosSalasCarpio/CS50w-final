from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('register', views.register, name='register'),
    path('admin_main', views.admin_main, name='admin_main'),
    path('delete_desprendible/<int:pk>', views.delete_desprendible, name='delete_desprendible'),
    path('download_desprendible', views.download_desprendible, name='download_desprendible'),
    path('download_certificado_user', views.download_certificado_user, name='download_certificado_user'),

    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="pdf_manager/password_reset.html"),
    name="reset_password"),

    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="pdf_manager/password_reset_sent.html"), 
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="pdf_manager/password_reset_form.html"), 
    name="password_reset_confirm"),

    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="pdf_manager/password_reset_done.html"), 
    name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)