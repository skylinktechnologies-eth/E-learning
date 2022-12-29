from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth import logout as logout_
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Student
from .forms import *

from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView


def permissions(request):
    context = {}


# redirectng the user to login page after logout
def logout(request):
    logout_(request)
    return redirect('login')


def forgot_password(request):
    try:
        value = request.session['username']
    except:
        return render(request, 'admin-side/forgot-password.html', {'errors': [f"No User found"]})
    try:
        user = User.objects.get(username=value)
    except:
        user = None

    if request.method == "POST" and user:
        if Student.objects.filter(user=user):
            security_question = Student.objects.get(user=user)
            security_answer = request.POST['security_answer']
            if security_answer == security_question.security_answer:
                request.session['security_answer'] = security_answer
                return redirect('change-password')
            else:
                return render(request, 'admin-side/forgot-password2.html', {"security_question": security_question.security_question, 'errors': ["Incorrect Answer"], "title": "Forgot Password"})
        else:
            messages.error(
                request, "The user doesn't have a security question.")

            return redirect('login')

    if user:
        if Student.objects.filter(user=user):
            security_question = Student.objects.get(user=user)

            return render(request, 'admin-side/forgot-password2.html', {"security_question": security_question.security_question, "title": "Forgot Password"})

        messages.error(request, "The user doesn't have a security quesion.")

        return redirect('login')

    del (request.session['username'])
    request.session['errors'] = [f"No User found with the username {value}"]
    return redirect('forgot')


def forgot(request):
    context = {"title": "Forgot Password"}
    if 'errors' in request.session.keys():
        context['errors'] = request.session['errors']

        del (request.session['errors'])

    if request.POST:
        username = request.POST.get("username")
        request.session['username'] = username

        return redirect('forgot-password')

    return render(request, 'admin-side/forgot-password.html', context)


class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')
    template_name = 'admin-side/forgot-password3.html'
    title = _('Password change')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        security_answer = self.request.session['security_answer']

        user = User.objects.get(username=self.request.session['username'])

        security_question = Student.objects.get(user=user)

        if security_answer != security_question.security_answer:
            self.request.session['error'] = ["No username specified"]
            return reverse_lazy("login")

        kwargs['user'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Forgot Password"
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def page_not_found_view(request, exception):
    context = {
        **permissions(request)
    }
    return render(request, '404.html', context)


def error_view(request):
    context = {
        **permissions(request)
    }
    return render(request, "500.html", context)


def permission_denied_view(request, exception):
    context = {
        **permissions(request)
    }
    return render(request, "403.html", context)


def bad_request_view(request, exception):
    context = {
        **permissions(request)
    }
    return render(request, "400.html")


class StudentupdateView(UpdateView):
    model = Student
    template_name = "admin-side/register.html"
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.get_object(self).user
        return {**context, **permissions(self.request)}

    def get_object(self, queryset=None):

        queryset = User.objects.all()

        pk = self.kwargs.get(self.pk_url_kwarg)

        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        obj = queryset.get().Student
        return obj


class StudentCreateView(CreateView):
    model = User
    template_name = "main/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User"
        context["open"] = "user"
        context["card_header"] = "Register User"
        context['obj_model'] = "user"

        return {**context}
