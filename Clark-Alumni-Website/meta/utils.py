from django.core.mail import send_mail

STUDENT_GROUP_NAME = "Student"
ALUM_GROUP_NAME = "Alum"


def check_form_fields(**kwargs) -> None:
    status = kwargs.get("status")

    student = kwargs.get("student")
    if student and not student.groups.filter(name=STUDENT_GROUP_NAME).exists():
        raise Exception(f"student value must be a User within the {STUDENT_GROUP_NAME} group")
    if student and not student.academic_standing:
        raise Exception(
            "Student account must have selected an academic standing before drafting or submitting any requests"
        )

    cover_letter = kwargs.get("cover_letter")
    resume = kwargs.get("resume")
    other = kwargs.get("other")
    is_help_requested = (
        cover_letter
        or kwargs.get("career_planning")
        or resume
        or kwargs.get("mentor_shadowing")
        or kwargs.get("mock_interview")
        or other
    )
    if not is_help_requested and status != "draft":
        raise Exception(
            'One of the "help requested" categories is required when submitting a request.'
        )

    description = kwargs.get("description")
    if status != "draft" and other and not description:
        raise Exception(
            '"Other" was selected for Help Requested, but no description was given. Please use the description field to specify the help requested.'
        )

    document_link = kwargs.get("document_link")
    if status != "draft" and (cover_letter or resume) and not document_link:
        raise Exception(
            f"Request form was submitted for a cover letter or resume request, but no document link was provided."
        )

    alum = kwargs.get("assigned_alum")
    if alum and not alum.groups.filter(name=ALUM_GROUP_NAME).exists():
        raise Exception(f"assigned_alum value must be a User within the {ALUM_GROUP_NAME} group")

    if status == "assigned" and not alum:
        raise Exception(
            "The assigned alum field cannot be blank when the form status is set as Assigned"
        )


def send_assignment_notification(email_to, **kwargs):
    assigned_alum = kwargs.get("assigned_alum")
    alum_name = kwargs.get("alum_name")
    request_host_path = kwargs.get("request_host_path")
    website_URL = request_host_path + "/viewmyrequests/"
    website_name = "Clark CS Alumni-Student Connection Website"

    subject = f"{website_name} - Request Assigned Notification"

    message = (
        f"Your request submitted to the {website_name} has been picked up by an alum. "
        "You should hear from them in the near future.\n\n"
        f"Your career advancement support request has been assigned to {alum_name} ({assigned_alum}).\n"
        f"To view this request, go to http://{website_URL}"
    )

    from_email = "noreply@clarkalumnics.com"
    recipient_list = [email_to]

    send_mail(subject, message, from_email, recipient_list)


def field_str_display(value):
    return value.replace("_", " ").title()
