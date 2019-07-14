from django.urls import path, re_path
from . import views

app_name = "hospitals"

urlpatterns = [
    path('details/<id>', views.hospital_list, name="hospital_list"),
    path('doctor', views.doctor, name="doctor_page"),
]
