from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.homePage, name='home'),
    path("course/", views.CourseListView.as_view(), name='courses'),
    path("about/", views.about, name="about"),
    path('trainer/', views.trainer, name="trainer"),
    path('event/', views.events, name="event"),
    path('contact/', views.contact, name="contact"),

    path("dashbaord/", views.dashboard, name='dashboard'),
    path("register", views.CourseCreateView.as_view(), name='register-course'),
    path("admin-courses", views.CourseListViewAdmin.as_view(), name='admin-course'),
]
