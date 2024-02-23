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
from meta.models import StudentRequestForm
from meta.utils import ALUM_GROUP_NAME, STUDENT_GROUP_NAME, send_assignment_notification

def request_page(request, request_id):
  request_obj = StudentRequestForm.objects.get(id = request_id)
  return render(request, 'request_page.html', {'request': request_obj})

#Directs the user to the home page, called when logo is clicked on website
def home(request):
    return render(request, "users/home.html")

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
    all_requests = StudentRequestForm.objects.filter(student=request.user) #Collects user's requests
    return render(request, "view_my_requests.html", {"all_requests": all_requests})

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

#Called when creating request comment
@never_cache
def add_comments(request, request_id):
    if request.method == "POST":
        request_obj = StudentRequestForm.objects.get(pk=request_id)
        new_comment = request.POST.get("my_comments").strip()  # Remove leading/trailing whitespaces
        if new_comment:  # Check if the new comment contains data
            timestamp = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone())
            formatted_timestamp = timestamp.strftime("%m/%d/%y")
            comment_with_timestamp = f"{formatted_timestamp}: {new_comment}"
            existing_comments = request_obj.my_comments
            if existing_comments:
                updated_comments = f"{existing_comments}\n{comment_with_timestamp}" #new comments appended to end of old comments as plain string
            else:
                updated_comments = comment_with_timestamp
            request_obj.my_comments = updated_comments
            request_obj.save()
    return HttpResponseRedirect(reverse("viewassignedrequests"))

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
        form.instance.student = request.user
        form.instance.status = "submitted"
        if form.is_valid():
            form.save()
            messages.success(request, "Your request has been received")
            return render(request, "base.html", {'form_submitted': True})
        return render(request, "base.html", {'form': form})
