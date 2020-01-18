from django.urls import path
from . import views

urlpatterns = [
    path('file_save', views.file_save, name='file_save'),
	path('get_file<file_id>', views.get_file, name='get_file'),
	path('get_mini<file_id>', views.get_mini, name='get_mini'),
	path('delete_file<file_id>', views.delete_file, name='delete_file'),
]
