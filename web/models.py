from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=5000)
    file = models.FileField(upload_to='documents/', blank=True, validators=[FileExtensionValidator(['pdf'])])
    answer = models.CharField(max_length=5000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)