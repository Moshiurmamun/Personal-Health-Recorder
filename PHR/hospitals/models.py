from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse


class Doctor(models.Model):
    doctor_name = models.ForeignKey(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100, null=True, blank = True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    phone = models.CharField(max_length=18, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='doctor_image', null=True, blank=True)

    def __str__(self):
        name = self.email
        return name


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    doctor = models.ManyToManyField(User, blank=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    image = models.ImageField(upload_to='hospital_image', null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hospitals:hospital_list", args=[self.id])







class District(models.Model):
    name = models.CharField(max_length=30)
    hospital = models.ManyToManyField(Hospital, blank=True)

    def __str__(self):
        return self.name





