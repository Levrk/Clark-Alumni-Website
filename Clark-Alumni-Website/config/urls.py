"""
URL configuration for alumniPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from meta import views
from meta.forms import AuthForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path(
        "viewrequests/",
        login_required(views.return_form_data, login_url="/login/"),
        name="viewrequests",
    ),
    path(
        "viewassignedrequests/",
        login_required(views.return_assigned_data, login_url="/login/"),
        name="viewassignedrequests",
    ),
    path(
        "change_status_assigned/<int:request_id>/",
        login_required(views.change_status_assigned, login_url="/login/"),
        name="status_change_assigned",
    ),
    path(
        "change_status_unassign/<int:request_id>/",
        login_required(views.change_status_unassigned, login_url="/login/"),
        name="status_change_unassigned",
    ),
    path(
        "change_status_closed/<int:request_id>/",
        login_required(views.change_status_closed, login_url="/login/"),
        name="status_change_closed",
    ),
    path(
        "add_comments/<int:request_id>/",
        login_required(views.add_comments, login_url="/login/"),
        name="add_comments",
    ),
    path(
        "studentrequestform/",
        login_required(views.StudentRequestFormSubmitView.as_view(), login_url="/login/"),
        name="base",
    ),
    path(
        "viewmyrequests/",
        login_required(views.return_my_requests, login_url="/login/"),
        name="viewmyrequests",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            form_class=AuthForm,
            template_name="users/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("noaccess/", views.no_access, name="noaccess"),
    path("noaccessalumni/", views.no_access_alumni, name="noaccessalumni"),
]
