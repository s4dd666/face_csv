import csv

from django.core.files.base import ContentFile
from django.db import models

from django.core.exceptions import ValidationError
import re

from django.db import models
from django.http import HttpResponse
from faker import Faker


class UserManager(models.Manager):
    def create_random_user(self):
        fake = Faker()

        first_name = fake.first_name()
        last_name = fake.last_name()
        job = fake.job()
        email = fake.email()
        text = fake.paragraph(min_nb_sentences=1, max_nb_sentences=4)
        date = fake.date()

        manage = self.model(first_name=first_name, last_name=last_name, job=job, email=email, text=text, date=date)
        manage.save()

        return manage


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    objects = UserManager()
    csv_file = models.FileField(upload_to='csv_files/', null=True, blank=True)
    csv_file_number = models.IntegerField(null=True, blank=True)
    csv_file_status = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.csv_file:
            self.csv_file_number = self.id
            self.csv_file_status = 'generating'
            self.generate_csv()

    def generate_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="users_{self.csv_file_number}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Full Name', 'Job', 'Email', 'Text', 'Date'])

        users = User.objects.all()
        for user in users:
            writer.writerow([user.fullname(), user.get_job_display(), user.email, user.text, user.date])

        file_name = f'users_{self.csv_file_number}.csv'
        self.csv_file.save(file_name, ContentFile(response.getvalue()))
        self.csv_file_status = 'ready'
        self.save()

    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'CSV'




