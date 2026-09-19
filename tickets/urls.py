from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_tickets, name="lista_tickets"),
    path("demo-fifo/", views.demo_fifo, name="demo_fifo"),
]
