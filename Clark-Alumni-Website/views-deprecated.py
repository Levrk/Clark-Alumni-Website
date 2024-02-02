'''
This file appears to be deprecated.
Another views file exists and is more feature complete.
meta/views.py appears to be the one referenced throughout the project.
'''
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from meta.forms import StudentSubmissionForm, UserRegistrationForm
from meta.utils import STUDENT_GROUP_NAME


class StudentRequestFormSubmitView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = StudentSubmissionForm()
        context = {"form": form}
        return render(request, "base.html", context)

    def post(self, request):
        form = StudentSubmissionForm(request.POST)
        form.instance.student = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Your request has been received")
            return render(request, "users/home.html")


def home(request):
    return render(request, "users/home.html")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            group = Group.objects.get(name=STUDENT_GROUP_NAME)
            form.instance.groups.add(group)
            messages.success(request, "Your account has been created. You can log in now!")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "users/register.html", context)


def index(request):
    return HttpResponse("Index page")


def home_screen(request):
    print(request.headers)
    return render(request, "base.html", {})
