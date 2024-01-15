from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandParser
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Creates a superuser, bypassing password complexity requirements"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("username", type=str, help="user's email")
        parser.add_argument("password", type=str, nargs="?", help="user's password")

    def handle(self, *args, **kwargs):
        try:
            username = kwargs.get("username")
            password = kwargs.get("password")
            get_user_model().objects.create_superuser(email=username, password=password)
            print(f"Created superuser {username}")
        except IntegrityError as e:
            raise IntegrityError(
                f"IntegrityError: User {username} already exists and is left untouched."
            ) from e
