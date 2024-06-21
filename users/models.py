import uuid

from django.db import models
from django.utils import timezone

# Create your models here.
class UserTable(models.Model):

    userid = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, unique=True)
    phno = models.IntegerField(null=True)
    pincode = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user_table"
        managed=True


class UserLoginTable(models.Model):

    id = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, primary_key=True, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = "user_login_table"
        managed=True