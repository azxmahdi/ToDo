import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from random import choice
from todo.models import Task

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test users and tasks'
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('number_user', type=int, help='The number of users to create')
        parser.add_argument('number_task', type=int, help='The number of tasks per user')

    def handle(self, *args, **kwargs):
        number_user = kwargs['number_user']
        number_task = kwargs['number_task']

        if number_user < 1:
            self.stdout.write(self.style.ERROR(f'The number of users must be greater than 1 (arg1)'))
            sys.exit(1)

        if number_task < 1:
            self.stdout.write(self.style.ERROR(f'The number of tasks must be greater than 1 (arg2)'))
            sys.exit(1)

        email_user_list = []

        for _ in range(number_user):
            user = User.objects.create_user(
                email=self.fake.free_email(),
                password="a/123456",  
                is_verified=True
            )

            for _ in range(number_task):
                Task.objects.create(
                    user=user,
                    title=self.fake.sentence(nb_words=3),
                    is_done=choice([False, True])
                )

            email_user_list.append(user.email)


        self.stdout.write(self.style.SUCCESS(f'Created users with these emails:'))
        for email in email_user_list:
            self.stdout.write(self.style.SUCCESS(f'  {email}'))

