from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

import csv
from django.http import HttpResponse
from .forms import GenerateUsersForm, UserForm, LoginForm
from .models import User

from faker import Faker
import os
from django.conf import settings


def index(request):
    users = User.objects.all()
    context = {
        'title': 'Главная страница',
        'users': users
    }
    return render(request, 'main/index.html', context)


def create(request):
    error = ''
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Произошла ошибка'

    form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'main/create.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def generate_users(request):
    if request.method == "POST":
        form = GenerateUsersForm(request.POST)
        if form.is_valid():
            num_users = form.cleaned_data.get('num_users')

            # генерируем данные пользователей
            fake = Faker()
            users_data = []
            for _ in range(num_users):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                job = fake.job()
                text = fake.paragraph()
                date = fake.date_of_birth()

                users_data.append({
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'job': job,
                    'text': text,
                    'date': date
                })

            # создаем объект HttpResponse с csv-данными
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="users.csv"'

            # имена столбцов и порядок
            fieldnames = ['first_name', 'last_name', 'email', 'job', 'text', 'date']

            # записываем данные в csv
            writer = csv.DictWriter(response, fieldnames=fieldnames)
            writer.writeheader()
            for user in users_data:
                writer.writerow(user)

            return response
    else:
        form = GenerateUsersForm()
    return render(request, 'main/generate_users.html', {'form': form})


def download_csv(request):
    media_path = os.path.join(settings.MEDIA_ROOT, 'csv')
    file_path = os.path.join(media_path, 'users.csv')

    # Проверяем, есть ли файл на сервере
    if not os.path.exists(file_path):
        # Если файла нет, то создаем его и записываем данные
        with open(file_path, mode='w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['First Name', 'Last Name', 'Job', 'Email', 'Text', 'Date'])

            users = User.objects.all()
            for user in users:
                writer.writerow(
                    [user.first_name, user.last_name, user.get_job_display(),user.email, user.text, user.date])

    # Открываем файл на чтение и считываем его содержимое
    with open(file_path, mode='r') as csv_file:
        file_content = csv_file.read()


    # Устанавливаем заголовок ответа и возвращаем ссылку на файл
    response = HttpResponse(file_content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'


    return response