from django.urls import path
from . import views

urlpatterns = [
    path('', views.container_list, name='container_list'),
    path('container/<str:container_id>/<str:action>/', views.container_action, name='container_action'),
    path('container/<str:container_id>/logs/', views.container_logs, name='container_logs'),
]