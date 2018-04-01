# from django.core.management.base import BaseCommand, CommandError

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         sprint('it works')

from django.core.management import BaseCommand

class Command(BaseCommand):
    help = "My test command"

    # A command must define handle()
    def handle(self, *args, **options):
        self.stdout.write("Doing All The Things!")
