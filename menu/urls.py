from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path("monitor/<int:pk>/", views.monitor_page, name="monitor_page"),
    path("monitor/sse/<int:monitor_pk>/", views.sse_monitor, name="sse_monitor"),
]
