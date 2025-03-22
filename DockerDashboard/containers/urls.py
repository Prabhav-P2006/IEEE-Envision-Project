from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logged-out/', views.logout_view, name='logout'),
    path('', views.container_list, name='container_list'),
    path('container/<str:container_id>/logs/', views.container_logs, name='container_logs'),
    path('container/<str:container_id>/<str:action>/', views.container_action, name='container_action'),
]