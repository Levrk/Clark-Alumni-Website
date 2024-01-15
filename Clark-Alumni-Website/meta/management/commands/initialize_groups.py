from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from meta.utils import ALUM_GROUP_NAME, STUDENT_GROUP_NAME

GROUP_NAMES = (STUDENT_GROUP_NAME, ALUM_GROUP_NAME)


class Command(BaseCommand):
    help = "Loads the initial set of Groups for students and alumni"

    def handle(self, *args, **kwargs):
        try:
            for group_name in GROUP_NAMES:
                Group.objects.create(name=group_name)

            self.stdout.write("Successfully initialized Auth Groups")
        except Exception as e:
            self.stderr.write(f"Could not initialize groups. Error: {e}")
