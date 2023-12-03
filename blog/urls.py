from django.urls import path
from .views import main_list

urlpatterns = [
    path('', main_list, name = 'main_list'),

]
