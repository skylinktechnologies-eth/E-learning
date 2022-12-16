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
    path("detail-course/<int:pk>/",
         views.CourseDetail, name="detail-course"),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("register-Course", views.CourseCreateView.as_view(), name='register-course'),
    path("admin-courses", views.CourseListViewAdmin.as_view(), name='admin-courses'),
    path("register-lesson", views.LessonCreateview.as_view(), name="register-lesson"),
    path("admin-lesson", views.LessonListView.as_view(), name="lessons"),
    path("admin-category", views.CategoryListView.as_view(), name='categorys'),
    path("register-category", views.CategoryCreateView.as_view(),
         name='register-category'),
    path("update-category/<int:pk>/",
         views.CategoryUpdateView.as_view(), name='update-category'),
    path("delete-category/<int:pk>/",
         views.CategoryDeleteView.as_view(), name="delete-category"),
    path("delete-course/<int:pk>/",
         views.CourseDeleteView.as_view(), name="delete-course"),
    path("update-course/<int:pk>/",
         views.CourseUpdateView.as_view(), name='update-course'),
    path("update-lesson/<int:pk>/",
         views.LessonUpdateView.as_view(), name='update-lesson'),
    path("delete-lesson/<int:pk>/",
         views.LessonDeleteView.as_view(), name="delete-lesson"),
    path("register-payment",
         views.PaymentCreateView, name="register-payment"),
]
