from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('flights/<int:id>', views.flights, name="flights"),
    path('<int:id>/book', views.book, name="book"),
]
