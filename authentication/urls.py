from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot/', views.forgot, name='forgot'),
    path('forgot/security-question/',
         views.forgot_password, name='forgot-password'),
    path('change-password/', views.PasswordChangeView.as_view(),
         name='change-password'),
    path("register-user/", views.StudentCreateView.as_view(), name="register-user"),

]
