from django.urls import path
from . import views

urlpatterns = [
    path("students/create/", views.create_student),
    path("students/", views.get_students),
    path("students/update/<int:id>/", views.update_student),
    path("students/delete/<int:id>/", views.delete_student),
]