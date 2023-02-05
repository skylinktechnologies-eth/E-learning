from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib import messages as mes
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
    mychats = Message.objects.filter(
        sender_id=request.user.id, room_id=pk).order_by('date')
    roomChats = Message.objects.filter(
        room_id=pk).exclude(sender_id=request.user.id).order_by('date')
    messages = mychats | roomChats
    print(messages)
    rooms = Room.objects.all()
    room_detail = Room.objects.get(id=pk)
    if request.method == "POST":
        sender = request.user
        room = room_detail
        thismessage = request.POST.get('message')
        new_message = Message(sender=sender, room=room, message=thismessage)
        new_message.save()

    context = {"mychats": mychats,
               "roomchats": roomChats, "rooms": rooms, "pk": pk, "room_detail": room_detail, "messages": messages}

    return render(request, "chat/room.html", context)
# class RoonListView(ListView):


def send(request):
    message = request.POST['message']
    sender = request.user
    room = request.POST['room_id']
    new_message = Message(
        message=message, sender=sender, room=room)
    new_message.save()
    for i in range(100):
        print(i)
    return HttpResponse("sent")


def getMessages(request, pk):
    room_details = Room.objects.get(id=pk)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
