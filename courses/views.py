from django.shortcuts import render
from .models import *
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.


def permissions(request):
    context = {
        'course_permission': request.user.has_perm(perm="course.view_course")
    }


def dashboard(request):

    context = {}
    return render(request, 'admin-side/dashboard.html', {"open": "dashboard"})


def homePage(request):
    context = {}
    return render(request, 'main/homepage.html', context)


def about(request):
    context = {}
    return render(request, 'main/about.html', context)


def trainer(request):
    context = {}
    return render(request, 'main/trainers.html', context)


def events(request):
    context = {}
    return render(request, 'main/events.html', context)


def contact(request):
    context = {}
    return render(request, 'main/contact.html', context)


class CourseCreateView(CreateView):
    model = Course
    form_class = RegisterCourseForm
    template_name = "admin-side/register.html"
    context_object_name = 'form'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Register"
        context["title"] = "Room"
        context["card_header"] = "Register Course"
        context["open"] = "room"
        return {**context}

    def form_valid(self, form):
        print("done")
        messages.success(self.request, 'Course Registerd Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class CourseListView(ListView):
    model = Course
    template_name = "main/courses.html"

    def get(self, *args, **kwargs):
        self.filter = kwargs.get("filter", None)
        return super().get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Courses"
        context["open"] = "course"

        return {**context}


class CourseListViewAdmin(ListView):
    model = Course
    template_name = "admin-side/course-list.html"

    def get(self, *args, **kwargs):
        self.filter = kwargs.get("filter", None)
        return super().get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Courses"
        context["open"] = "course"

        return {**context}
