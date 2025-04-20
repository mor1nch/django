from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product
from users.models import User


class Command(BaseCommand):
    help = 'Populates the database with initial data from fixtures and deletes old data first.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Loading data from fixtures...')
        call_command('loaddata', 'categories.json')
        call_command('loaddata', 'products.json')

        self.stdout.write('Loading groups and permissions...')
        call_command('loaddata', 'groups.json')

        self.stdout.write('Database population complete.')