from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tickets, name='lista_tickets'),
    path('tickets/todos/', views.TicketListView.as_view(), name='tickets_todos'),
    path('<int:ticket_id>/', views.detalle_ticket, name='detalle_ticket'),
    path('nuevo/', views.crear_ticket_form, name='crear_ticket_form'),
    path('<int:ticket_id>/editar/', views.editar_ticket_form, name='editar_ticket_form'),
    path("tablero/", views.tablero, name="tablero"),
    path("areas/red/", views.red_areas, name="red_areas"),
]
