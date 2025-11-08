from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_page, name='menu_page'),
    path('events/menu/', views.sse_menu, name='sse_menu'),
]
