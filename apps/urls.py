from django.contrib import admin
from django.urls import path, include
from apps import views

urlpatterns = [

    path("users/", views.UserView.as_view()),
    path("users/<str:pk>/", views.UserView.as_view()),

    path("students/", views.StudentView.as_view()),
    path("students/<str:pk>/", views.StudentView.as_view()),

]
