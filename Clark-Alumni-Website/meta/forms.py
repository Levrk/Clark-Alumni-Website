import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from meta.models import StudentRequestForm, User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField(required=True)
    cell_phone = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "cell_phone",
            "academic_standing",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean_cell_phone(self):
        phone_number = self.cleaned_data.get("cell_phone")
        phone_number_regex = r"^\d{10}$"

        if phone_number and not re.match(phone_number_regex, phone_number):
            raise forms.ValidationError("Please enter a valid phone number.")

        return phone_number


class StudentSubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentRequestForm
        exclude = ["status", "student", "assigned_alum"]


class StatusChangeForm(forms.ModelForm):
    class Meta:
        model = StudentRequestForm
        fields = ["status"]


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = StudentRequestForm
        fields = ["my_comments"]


class AuthForm(AuthenticationForm):
    def clean_username(self):
        return self.cleaned_data["username"].lower()


class selectStatusForm(forms.Form):
    show_open = forms.BooleanField(
        initial={"checked": True},
        widget=forms.CheckboxInput(attrs={"onclick": "this.form.submit();"}),
        required=False,
    )
    show_closed = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"onclick": "this.form.submit();"}),
        required=False,
    )
