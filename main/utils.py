import random
import csv
from django.http import HttpResponse
from .models import User

def create_csv_response(filename, rows):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Job', 'Email', 'Text'])
    for row in rows:
        writer.writerow(row)

    return response

def generate_users(num_users):
    users = []
    for i in range(num_users):
        user = User.objects.create_random_user()
        users.append([user.id, user.first_name, user.last_name, user.job, user.email, user.text])
    return users
