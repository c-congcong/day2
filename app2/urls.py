from django.contrib import admin
from django.urls import path, include

from app2 import views

urlpatterns = [
    path("employees/", views.EmployeeAPIView.as_view()),
    path("employees/<str:id>/", views.EmployeeAPIView.as_view()),

]
