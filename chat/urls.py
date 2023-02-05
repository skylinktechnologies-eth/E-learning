from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chat import views as chat_views

urlpatterns = [
    path("", chat_views.chatPage, name="chat-page"),
    path("<int:pk>/", chat_views.chat, name="chat"),
    path("send", chat_views.send, name="send"),
    path('getMessages/<int:pk>/', chat_views.getMessages, name='getMessages'),
]
