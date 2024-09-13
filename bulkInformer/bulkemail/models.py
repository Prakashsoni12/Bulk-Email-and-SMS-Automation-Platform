from django.db import models

# Create your models here.

class User(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=120,unique=True)
    gender = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name