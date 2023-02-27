from django.urls import path

from . import views

urlpatterns = [
    path('files_storage_api', views.files_storage, name='files_storage'),
]
