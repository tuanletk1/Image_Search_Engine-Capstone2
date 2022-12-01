from django.db import models
import json


# Create your models here.
class User(models.Model):
  username = models.CharField(max_length=150)
  first_name = models.CharField(max_length=255, null=True)
  last_name = models.CharField(max_length=255, null=True)
  email = models.EmailField(max_length=255)
  password = models.CharField(max_length=255)
  is_active = models.BooleanField(null=True)
  avatar = models.TextField(null=True)

  def toJson(self):
    data = '{"id": "' + str(self.id) + '", "username": "' + str(self.username) + '", "role": "' \
           + str(self.permission_set.all().values().get().get('permission')) + '", ' + \
           '"email":"' + self.email + '", "avatar":"' + self.avatar + '", "perid": "'+str(self.permission_set.all().values().get().get('id'))+'"}'
    return json.loads(data)


  class Meta:
    db_table = 'users'


class Permission(models.Model):
  permission = models.CharField(max_length=255)
  users = models.ManyToManyField(User)

  class Meta:
    db_table = 'permission'
