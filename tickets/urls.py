from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.lista_tickets, name='lista_tickets'),
    path('<int:ticket_id>/', views.detalle_ticket, name='detalle_ticket'),
    path('nuevo/', views.crear_ticket_form, name='crear_ticket_form'),
    path('<int:ticket_id>/editar/', views.editar_ticket_form, name='editar_ticket_form'),
]
