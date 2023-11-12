from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            action="store",
            required=True,
            help="Email Address",
        )
        parser.add_argument(
            "--password",
            action="store",
            required=True,
            help="Password",
        )

    def handle(self, *args, **kwargs):
        user_model = get_user_model()
        try:
            user_model.objects.db_manager().create_superuser(
                email=kwargs["email"],
                password=kwargs["password"],
            )
        except Exception as e:
            self.stdout.write(self.style.WARNING("could not create user: {}".format(e)))
