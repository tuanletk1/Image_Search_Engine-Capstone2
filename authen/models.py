from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(null=True)

    class Meta:
        db_table = 'users'


class Permission(models.Model):
    permission = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

    class Meta:
        db_table = 'permission'

