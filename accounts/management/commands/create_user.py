from uuid import uuid4

from django.core.management import BaseCommand

from api.methods import create_account, generate_api_key


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--username", type=str)
        parser.add_argument("--password", type=str, required=False)

    def execute(self, *args, **options):
        username = options["username"]
        password = options.get("password", str(uuid4()))

        user = create_account(
            username=username,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save()

        user.account.setup_complete = True
        user.account.is_verified = True
        user.account.save()

        print(f"Username: {username}\nPassword: {password}")
