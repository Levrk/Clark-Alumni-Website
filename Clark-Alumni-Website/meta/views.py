from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from meta.forms import StatusChangeForm, StudentSubmissionForm, UserRegistrationForm, selectStatusForm
from meta.models import StudentRequestForm, Comment
from meta.utils import ALUM_GROUP_NAME, STUDENT_GROUP_NAME, send_assignment_notification
import re

#Called when creating request comment
@never_cache
def add_comments(request, request_id):
  request_obj = StudentRequestForm.objects.get(pk=request_id) # Gets the request being commented on
  Comment.objects.create(request = request_obj, user = request.user, body = request.POST['comment']) # Creates a Comment from the posted comment
  return HttpResponseRedirect(reverse("viewassignedrequests"))

# Called when navigating to the request page
def request_page(request, request_id):
  request_obj = StudentRequestForm.objects.get(id = request_id) # Gets the request
  if request.method == 'POST':
    Comment.objects.create(request = request_obj, user = request.user, body = request.POST['comment'])
  comments = sorted(Comment.objects.filter(request = request_obj).all(), key = lambda comment : comment.date) # Gets the request's comments in a sorted list
  return render(request, 'request_page.html', {'request': request_obj, 'comments': comments})

#Directs the user to the home page, called when logo is clicked on website
def home(request):
    return render(request, "users/home.html")

#Directs the user to the draft page
def draft(request):
    return render(request, "draft.html")

# Function to delete a draft
def delete_draft(request, draft_id):
    if request.method == 'POST':
        draft_obj = StudentRequestForm.objects.get(pk=draft_id)
        # Check if the request belongs to the current user
        if draft_obj.student == request.user:
            # Delete the request
            draft_obj.delete()
            messages.success(request, "Draft deleted successfully.")
            return HttpResponseRedirect(reverse("draft"))
        else:
            # If the request doesn't belong to the user, show an error message
            messages.error(request, "You are not authorized to delete this draft.")
    # Redirect to a relevant page
    return HttpResponseRedirect(reverse("home"))

# Function to delete a request
def delete_request(request, request_id):
    if request.method == 'POST':
        request_obj = StudentRequestForm.objects.get(pk=request_id)
        # Check if the request belongs to the current user
        if request_obj.student == request.user:
            # Delete the request
            request_obj.delete()
            messages.success(request, "Request deleted successfully.")
            return HttpResponseRedirect(reverse("viewmyrequests"))
        else:
            # If the request doesn't belong to the user, show an error message
            messages.error(request, "You are not authorized to delete this request.")
    # Redirect to a relevant page
    return HttpResponseRedirect(reverse("home"))

#Returns True if the given user profile is an alum, otherwise, False
def is_alum(user):
    return user.groups.filter(name=ALUM_GROUP_NAME).exists()

#Returns True if the given user is a student, otherwise, false
def is_student(user):
    return user.groups.filter(name=STUDENT_GROUP_NAME).exists()

#Directs user to "/noaccess" if the user cannot make the given request
def no_access(request):
    return render(request, "no_access.html")

#Directs alum to "/noaccessalumni" if the alum cannot make the given request
def no_access_alumni(request):
    return render(request, "no_access_alumni.html")

#Directs student to "/viewmyrequests" and collects their requests
@user_passes_test(is_student, login_url="/noaccessalumni") #Checks user is not alum, and redirects them to "/noaccessalumni" if they are
@never_cache
def return_my_requests(request):
    all_requests = [post for post in StudentRequestForm.objects.filter(student=request.user) if post.status != 'draft'] #Collects user's requests
    return render(request, "view_my_requests.html", {"all_requests": all_requests})

#Directs student to "/draft" and collects their draft
@user_passes_test(is_student, login_url="/noaccessalumni") #Checks user is not alum, and redirects them to "/noaccessalumni" if they are
@never_cache
def draft(request):
    all_drafts = StudentRequestForm.objects.filter(status='draft', student=request.user)
    return render(request, "draft.html", {"all_drafts": all_drafts})

#Directs alum to "/viewrequests" and collects unanswered requests
@user_passes_test(is_alum, login_url="/noaccess") #Checks user is not student, and redirects them to "/noaccess" if they are
@never_cache
def return_form_data(request):
    submitted_requests = StudentRequestForm.objects.filter(status="submitted") #Collects unanswered requests
    return render(request, "view_requests.html", {"submitted_requests": submitted_requests})

#Called when alum closes assigned request, closes request and reloads assigned requests page
@user_passes_test(is_alum, login_url="/noaccess")
@never_cache
def change_status_closed(request, request_id):
    if request.method == "POST": #Tests if the type of request is "POST", seems to always be true
        request_obj = StudentRequestForm.objects.get(pk=request_id) 
        form = StatusChangeForm(request.POST, instance=request_obj)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse("viewassignedrequests"))

#Called when alum unassigns themself from an assigned request, unassigns request and reloads assigned request page
@user_passes_test(is_alum, login_url="/noaccess")
@never_cache
def change_status_unassigned(request, request_id):
    if request.method == "POST": #seems to always be the case?
        request_obj = StudentRequestForm.objects.get(pk=request_id)
        form = StatusChangeForm(request.POST, instance=request_obj)
        if form.is_valid():
            request_obj.status = "submitted"
            request_obj.assigned_alum = None
            form.save()
    return HttpResponseRedirect(reverse("viewassignedrequests"))

#Called when a user registers an account
@never_cache
def register(request):
    if request.user.is_authenticated: #Prevents logged in user from accessing registration page, could use "user_passes_test" decorator?
        return redirect("home")
    if request.method == "POST": #Seems like this would always be the case?
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if form.instance.academic_standing == "alumni":
                group = Group.objects.get(name=ALUM_GROUP_NAME)
            else:
                group = Group.objects.get(name=STUDENT_GROUP_NAME)
            form.instance.groups.add(group)
            messages.success(request, "Your account has been created. You can log in now!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "users/register.html", context)

#Directs alum to their assigned requests page
@user_passes_test(is_alum, login_url="/noaccess")
@never_cache
def return_assigned_data(request):
    form = selectStatusForm(request.GET or None)
    if request.method == "GET" and form.is_valid():
        statuses = []
        if request.GET.get("show_open", False):
            statuses.append("assigned")
        if request.GET.get("show_closed", False):
            statuses.append("closed")
    else:
        statuses = ["assigned"]

    assigned_requests = StudentRequestForm.objects.filter(
        assigned_alum=request.user, status__in=statuses
    )
    return render(
        request,
        "view_assigned_requests.html",
        {"assigned_requests": assigned_requests, "form": form},
    )

#Called when alum claims a request
@user_passes_test(is_alum, login_url="/noaccess")
@never_cache
def change_status_assigned(request, request_id):
    if request.method == "POST": #Seems to always be the cas?
        request_obj = StudentRequestForm.objects.get(pk=request_id)
        form = StatusChangeForm(request.POST, instance=request_obj)
        email = request.POST.get("email")
        request_obj.assigned_alum = request.user
        request_host_path = request.META["HTTP_HOST"]
        alum_name = request.user.first_name + " " + request.user.last_name
        kwargs = {
            "alum_name": alum_name,
            "assigned_alum": request_obj.assigned_alum,
            "request_host_path": request_host_path,
        }
        if form.is_valid():
            send_assignment_notification(email, **kwargs)
            form.save()
    submitted_requests = StudentRequestForm.objects.filter(status="submitted")
    return render(request, "view_requests.html", {"submitted_requests": submitted_requests}) #Returns alum to unassigned

#Doesn't seem to be called
#Would return the contained HttpResponse object
def index(request):
    return HttpResponse("Index page")

#Seems deprecated
#Redundant, would do same as home()
def home_screen(request):
    return render(request, "base.html", {})

# Trying to restrict alumni from viewing this page results in an issue.
class StudentRequestFormSubmitView(LoginRequiredMixin, View):

    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        form = StudentSubmissionForm()
        context = {"form": form}
        return render(request, "base.html", context)

    def post(self, request):
      form = StudentSubmissionForm(request.POST)
      inst = form.instance
      inst.student = request.user
      if form.is_valid():
        form.save()
        if inst.status == 'submitted':
          messages.success(request, "Your request has been received")
          return render(request, "base.html", {'form_submitted': True})
        else:
          messages.success(request, "Your request has been saved as a draft")
          return render(request, "base.html", {'form_drafted': True})
      return render(request, "base.html", {'form': form})
