from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tickets, name='lista_tickets'),
    path('<int:ticket_id>/', views.detalle_ticket, name='detalle_ticket'),
    path('nuevo/', views.crear_ticket_form, name='crear_ticket_form'),
    path('<int:ticket_id>/editar/', views.editar_ticket_form, name='editar_ticket_form'),
]
