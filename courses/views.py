from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse


# Create your views here.


def permissions(request):
    context = {
        'course_permission': request.user.has_perm(perm="course.view_course")
    }


def dashboard(request):

    context = {}
    return render(request, 'admin-side/dashboard.html', {"open": "dashboard"})


def homePage(request):
    context = {"open": "home"}
    return render(request, 'main/homepage.html', context)


def about(request):
    context = {"open": "about"}
    return render(request, 'main/about.html', context)


def trainer(request):
    context = {"open": "trainer"}
    return render(request, 'main/trainers.html', context)


def events(request):
    context = {"open": "event"}
    return render(request, 'main/events.html', context)


def contact(request):
    context = {"open": "contact"}
    return render(request, 'main/contact.html', context)


class CourseCreateView(CreateView):
    model = Course
    form_class = RegisterCourseForm
    template_name = "admin-side/register-course.html"
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


@login_required
def CourseDetail(request, pk):
    course = Course.objects.get(id=pk)
    user = request.user
    lesson = Lesson.objects.get()
    context = {
        "title": "Course",
    }
    if request.method == "POST":
        for i in range(100):
            print("amin")
        attending = Attending(
            course=course, student=user.student, date=timezone.now())
        attending.full_clean()
        attending.save()
        messages.success(request, message="Renter Deleted Sucessfully")
        return redirect("home")
    return render(request, 'main/course-details.html', context)


class CourseDetailView(DetailView):
    model: Course
    template_name = "main/course-details.html"

    def get(self, *args, **kwargs):
        self.filter = kwargs.get("filter", None)
        return super().get(self.request, *args, **kwargs)

    def get_queryset(self):
        return Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Course"

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


class LessonCreateview(CreateView):
    form_class = RegisterLessonForm
    success_url = reverse_lazy("lessons")
    template_name = "admin-side/register-lesson.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Register"
        context["title"] = "Lesson"
        context["card_header"] = "Register lesson"
        context["open"] = "lesson"
        return {**context}

    def form_valid(self, form):
        print("done")
        messages.success(self.request, 'Lesson Registerd Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class LessonListView(ListView):
    model = Lesson
    template_name = "admin-side/lesson-list.html"

    def get(self, *args, **kwargs):
        self.filter = kwargs.get("filter", None)
        return super().get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Lessons"
        context["open"] = "lesson"

        return {**context}


class CategoryCreateView(CreateView):
    model = Category
    form_class = RegisterCategoryForm
    success_url = reverse_lazy('categorys')
    template_name = "admin-side/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category"
        context["open"] = "category"

        return {**context}


class CategoryListView(ListView):
    model = Category
    template_name = 'admin-side/category-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category"
        context["open"] = "category"

        return {**context}


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "admin-side/register.html"
    success_url = reverse_lazy('categorys')
    form_class = RegisterCategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category"
        context["open"] = "category"

        return {**context}


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy("categorys")

    template_name = "admin-side/delete_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category"
        context["open"] = "category"

        return {**context}

    def form_valid(self, form):
        if self.get_object().course_set.all().count() == 0:
            super().form_valid(self)
            messages.success(self.request, "Category Deleted successfully")

        else:
            messages.error(
                self.request, "Category Cant Be Deleted. Make sure there are no Courses under this Category ")

        return HttpResponseRedirect(self.success_url)


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy("courses")

    template_name = "admin-side/delete_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Course"
        context["open"] = "course"

        return {**context}

    def form_valid(self, form):
        if self.get_object().lesson_set.all().count() == 0:
            super().form_valid(self)
            messages.success(self.request, "Course Deleted successfully")

        else:
            messages.error(
                self.request, "Course Cant Be Deleted. Make sure there are no Lessons under this Course ")

        return HttpResponseRedirect(self.success_url)


class CourseUpdateView(UpdateView):
    model = Course
    form_class = RegisterCourseForm
    success_url = reverse_lazy('courses')
    template_name = "admin-side/register-course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Update"
        context["title"] = "Course"
        context["card_header"] = "Update Course"
        context["open"] = "course"
        return {**context}

    def form_valid(self, form):
        print("done")
        messages.success(self.request, 'Course Updated Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = RegisterLessonForm
    success_url = reverse_lazy('lessons')
    template_name = "admin-side/register-lesson.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Update"
        context["title"] = "Lesson"
        context["card_header"] = "Update Lessons"
        context["open"] = "lesson"
        return {**context}

    def form_valid(self, form):
        print("done")
        messages.success(self.request, 'Lesson Updated Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy("lessons")

    template_name = "admin-side/delete_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Lesson"
        context["open"] = "lesson"

        return {**context}

    def form_valid(self, form):
        super().form_valid(self)
        messages.success(self.request, "Lesson Deleted successfully")

        return HttpResponseRedirect(self.success_url)
