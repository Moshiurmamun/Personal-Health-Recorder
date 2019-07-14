from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.contrib.auth.models import User

from django.utils import timezone

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=50, null=True, blank=True)
    disease_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = RichTextField()
    image = models.ImageField(upload_to='patient_story', null=True, blank=True)
    file = models.FileField(upload_to='file', null=True, blank=True)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["-publish", "updated"]


    def get_absolute_url(self):
        return reverse("accounts:story_detail", kwargs={"slug": self.slug})



def create_slug(instance, new_slug=None):
    slug = slugify(instance.user)
    if new_slug is not None:
        slug = new_slug
    qs = Patient.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Patient)
