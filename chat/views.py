from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import *
from django.http import HttpResponse
# Create your views here.


def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login")
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "chat/index.html", context)


def room(request):
    return render(request, "chat/")


def chat(request, pk):
    mychats = Message.objects.filter(sender_id=request.user.id, room_id=pk)
    peoplechats = Message.objects.filter(
        room_id=pk).exclude(sender_id=request.user.id)
    rooms = Room.objects.all()
    room_detail = Room.objects.get(id=pk)
    context = {"mychats": mychats,
               "peoplechats": peoplechats, "rooms": rooms, "pk": pk, "room_detail": room_detail}
    return render(request, "chat/room.html", context)
# class RoonListView(ListView):


def send(request):
    message = request.POST['message']
    sender = request.user
    room = request.POST['room_id']
    new_message = Message.objects.create(
        message=message, sender=sender, room=room)
    new_message.save()
    for i in range(100):
        print(i)
    return HttpResponse("sent")
