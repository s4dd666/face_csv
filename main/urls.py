from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.index, name='home'),
    path('create/', views.create, name='create'),
    path('logout/', views.logout_view, name='logout'),
    path('generate-users/', views.generate_users, name='generate_users'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('login/', views.login_view, name='login'),
]

# urlpatterns = [
#     path('login/', views.login, name='login'),
#     path('logout', views.logout_view, name='logout'),
#     path('data_schemas/', views.data_schemas, name='data_schemas'),
#     path('new_schema/', views.new_schema, name='new_schema'),
#     path('data_sets/', views.data_sets, name='data_sets'),
# ]