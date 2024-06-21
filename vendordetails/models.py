import uuid

from django.db import models

# Create your models here.

class VendorDetails(models.Model):

    vendorid = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pincode = models.IntegerField()
    address = models.CharField(max_length=255)

    class Meta:
        db_table = "vendor_details"
        managed=True

class VendorLogin(models.Model):

    id = models.ForeignKey(VendorDetails, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = "vendor_login"
        managed=True


class InventoryDetail(models.Model):
    inventory_id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    inventory_title = models.CharField(max_length=50)
    belongs_to = models.ForeignKey(VendorDetails, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    pincode = models.IntegerField()

    class Meta: 
        db_table = "inventory_details"
        managed=True