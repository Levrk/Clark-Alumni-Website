from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AuthUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from meta.utils import ALUM_GROUP_NAME, STUDENT_GROUP_NAME, check_form_fields, field_str_display

HELP_REQUESTED_FIELD = [
    "cover_letter",
    "career_planning",
    "resume",
    "mentor_shadowing",
    "mock_interview",
    "other",
]


class UserManager(AuthUserManager):
    """
    This overrides the default UserManager provided by Django.
    We do this to remove the usage of the field "username" which
    is not needed in this project.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Overrides Django's default User class to use the email field as the username
    """

    ACADEMIC_OPTIONS = (
        ("first_year", "First Year"),
        ("sophomore", "Sophomore"),
        ("junior", "Junior"),
        ("senior", "Senior"),
        ("grad", "Grad Student"),
        ("alumni", "Alum"),
    )

    username = None
    email = models.EmailField(_("email address"), unique=True)
    cell_phone = models.CharField(blank=True, null=True)
    academic_standing = models.CharField(choices=ACADEMIC_OPTIONS, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name", "cell_phone")

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    @property
    def is_alum(self):
        return self.groups.filter(name=ALUM_GROUP_NAME).exists()

    @property
    def is_student(self):
        return self.groups.filter(name=STUDENT_GROUP_NAME).exists()

    class Meta(AbstractUser.Meta):
        ordering = ("-date_joined",)


class StudentRequestFormQueryset(models.QuerySet):
    """
    Custom QuerySet manager for the StudentRequestForm. This is
    used to verify that the two User FK's match the student and
    alum groups respectively.
    """

    def create(self, **kwargs):
        check_form_fields(**kwargs)
        super().create(**kwargs)

    def update(self, *args, **kwargs):
        check_form_fields(**kwargs)
        super().update(*args, **kwargs)

    #  TODO: Evaluate if these methods will be used and update if so
    def get_or_create(self, defaults=None, **kwargs):
        raise NotImplementedError

    def update_or_create(self, *args, **kwargs):
        raise NotImplementedError

    def bulk_create(self, *args, **kwargs):
        raise NotImplementedError

    def bulk_update(self, *args, **kwargs):
        raise NotImplementedError


class StudentRequestFormManager(models.Manager.from_queryset(StudentRequestFormQueryset)):
    pass


class StudentRequestForm(models.Model):
    """
    StudentRequestForm: This model holds the student request forms to be handled by the alumni
    """

    STATUS_OPTIONS = (
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("assigned", "Assigned"),
        ("closed", "Closed"),
    )

    SUPPORT_URGENCY_OPTIONS = (
        ("within_1_week", "Within 1 Week"),
        ("within_2_weeks", "Within 2 Weeks"),
        ("within_1_month", "Within 1 Month"),
        ("within_2_months", "Within 2 Months"),
        ("no_urgent_need", "No Urgent Need"),
    )

    status = models.CharField(choices=STATUS_OPTIONS, default="draft")
    submission_date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(User, models.CASCADE, related_name="student_requests")
    cover_letter = models.BooleanField(default=False)
    career_planning = models.BooleanField(default=False)
    resume = models.BooleanField(default=False)
    mentor_shadowing = models.BooleanField(default=False)
    mock_interview = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True)
    document_link = models.CharField(blank=True, null=True)
    job_interest = models.CharField(max_length=50, blank=True, null=True)
    industry_interest = models.CharField(max_length=50, blank=True, null=True)
    support_urgency = models.CharField(
        max_length=50, choices=SUPPORT_URGENCY_OPTIONS, default="within_1_week"
    )
    my_comments = models.TextField(blank=True, null=True)
    assigned_alum = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="alumni_assignments",
        blank=True,
        null=True,
    )

    objects = StudentRequestFormManager()

    def save(self, *args, **kwargs):
        fields = {
            "student": self.student,
            "assigned_alum": self.assigned_alum,
            "status": self.status,
            "document_link": self.document_link,
            "comments": self.comments,
        }
        fields.update(self.help_requested)
        check_form_fields(**fields)
        super().save(*args, **kwargs)

    @property
    def help_requested(self):
        help_requested = {}
        for field in HELP_REQUESTED_FIELD:
            help_requested[field] = getattr(self, field, False)
        return help_requested

    @property
    def help_requested_list_display(self):
        help_requested = []
        for field in HELP_REQUESTED_FIELD:
            if getattr(self, field, None):
                help_requested.append(field_str_display(field))
        return help_requested
