from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from authentication.models import Student
from .filters import courseFilter


# Create your views here.


def permissions(request):
    context = {
        'course_permission': request.user.has_perm(perm="course.view_course")
    }


def dashboard(request):
    course = Course.objects.all().count()
    student = Student.objects.all().count()

    payment = Payment.objects.all()

    total = 0
    unconfirmed = 0
    for i in payment:
        if i.status:
            amount = i.course_order_id.amount
            total = total + amount
        else:
            amount = i.course_order_id.amount
            unconfirmed = unconfirmed + amount
    context = {"course": course, "student": student,
               "open": "dashboard", "total": total, "unpaid": unconfirmed}
    return render(request, 'admin-side/dashboard.html', context)


def homePage(request):
    category = Category.objects.all()
    courses = Course.objects.all()
    students = Student.objects.all()
    trainerCount = User.objects.filter(groups__name="trainer").count()
    courseCount = courses.count()
    studentCount = students.count()
    event = Event.objects.all()
    eventCount = event.count()
    context = {"open": "home", "courses": courses,
               "studentCount": studentCount, "courseCount": courseCount, "category": category, "trainerCount": trainerCount, "eventCount": eventCount}
    return render(request, 'main/homepage.html', context)


def about(request):
    context = {"open": "about"}
    return render(request, 'main/about.html', context)


def trainer(request):
    context = {"open": "trainer"}
    return render(request, 'main/trainers.html', context)


def events(request):
    event = Event.objects.all()
    context = {"open": "event", 'datas': event}
    return render(request, 'main/events.html', context)


def contact(request):
    context = {"open": "contact"}
    return render(request, 'main/contact.html', context)


def PaymentCreateView(request):
    if request.method == "POST":
        form = RegisterPaymentForm(request.POST)
        user = request.user
        course_id = request.POST.get("course_order_id")
        if form.is_valid():
            course = Course.objects.get(id=course_id)
            payment = form.save(commit=False)
            payment.student = user.student
            payment.save()

            attending = Attending(
                payment=payment)
            attending.full_clean()
            attending.save()
            messages.success(request, message="payment registerd Sucessfully")
            return redirect("home")
    else:
        form = RegisterPaymentForm()
    context = {"title": "payment", "form": form}
    return render(request, 'main/register.html', context)


def PaymentConfirmView(request, pk):
    attending = Attending.objects.get(payment_id=pk)
    payment = Payment.objects.get(id=pk)
    payment.status = True
    attending.status = True
    attending.save()
    payment.save()
    messages.success(request, 'Payment Conrimed Succesfully')
    return HttpResponseRedirect(reverse_lazy('payments'))


# class paymentUpdateView(UpdateView):
#     model = Payment
#     template_name = "admin-side/register.html"
#     success_url = reverse_lazy('payments')
#     form_class = RegisterPaymentForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Payment"
#         context["open"] = "payment"

#         return {**context}


def paymentRejectView(request, pk):
    attending = Attending.objects.get(payment_id=pk)
    payment = Payment.objects.get(id=pk)
    payment.status = False
    attending.status = False
    attending.save()
    payment.save()
    messages.success(request, 'Payment Conrimed Succesfully')
    return HttpResponseRedirect(reverse_lazy('payments'))


class PaymentListView(ListView):
    model = Payment
    template_name = "admin-side/payment-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Payment"
        context["open"] = "payment"

        return {**context}


# def PaymentConfirmView(request, pk):
#     if request.method == 'POST':
#         payment = Payment.objects.get(id=pk)

#         payment.status = True


class CourseCreateView(CreateView):
    model = Course
    form_class = RegisterCourseForm
    template_name = "admin-side/register-course.html"
    context_object_name = 'form'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Register"
        context["title"] = "Course"
        context["card_header"] = "Register Course"
        context["open"] = "course"
        return {**context}

    def form_valid(self, form):
        form.instance.trainer = self.request.user
        messages.success(self.request, 'Course Registerd Successfully')
        course = form.save()
        trainer = TrainerCourse(course=course,
                                trainer=self.request.user)
        trainer.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


# def CourseListView(request):
#     object_list = Course.objects.all()
#     category = Category.objects.all()

#     context = {}
#     context['category'] = category
#     context['object_list'] = object_list
#     context['open'] = "course"
#     context['title'] = "Courses"

#     return render(request, 'main/courses.html', context)


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
        context["filter"] = courseFilter(
            self.request.GET, queryset=self.get_queryset())
        context['category'] = Category.objects.all()
        return {**context}


def CourseDetail(request, pk):
    course = Course.objects.get(id=pk)
    user = request.user
    lessons = Lesson.objects.filter(course_id=pk)
    context = {
        "title": "Course",
        "course": course,
        "lessons": lessons
    }

    return render(request, 'main/course-details.html', context)


# class CourseDetailView(DetailView):
#     model: Course
#     template_name = "main/course-details.html"

#     def get(self, *args, **kwargs):
#         self.filter = kwargs.get("filter", None)
#         return super().get(self.request, *args, **kwargs)

#     def get_queryset(self):
#         return Course.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Course"

#         return {**context}


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


class AttendingListView(ListView):
    model = Attending
    template_name = "admin-side/attending-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Attending"
        context["open"] = "attending"

        return {**context}


class TrainerListView(ListView):
    model = User
    template_name = "admin-side/trainer-list.html"

    def get_queryset(self):
        users = User.objects.filter(groups__name='trainer')

        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Trainer"
        context["open"] = "trainer"

        return {**context}


class trainerCreateView(CreateView):
    model = User
    template_name = "admin-side/register.html"
    form_class = TrainerRegistrationForm

    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User"
        context["open"] = "user"
        context["card_header"] = "Register User"
        context['obj_model'] = "user"

        return {**context}


class eventCreateView(CreateView):
    form_class = eventRegistrationForm
    model = Event
    success_url = reverse_lazy('event-list')
    template_name = "admin-side/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Event"
        context["open"] = "event"
        context["card_header"] = "Register Event"
        context['obj_model'] = "event"

        return {**context}


class eventListView(ListView):
    model = Event
    template_name = "admin-side/event-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Event"
        context["open"] = "event"
        context["card_header"] = " Events"
        context['obj_model'] = "event"

        return {**context}
