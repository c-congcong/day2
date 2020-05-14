from django.urls import path, include

from app_work import views

urlpatterns = [
    path("students1/", views.StudentsAPIVIew.as_view()),
    path("students1/<str:pk>/", views.StudentsAPIVIew.as_view()),
]