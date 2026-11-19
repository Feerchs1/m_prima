from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_cotizacion, name='home_cotizacion'),
    path('ticket/', views.ticket_view, name='ticket'),
]
