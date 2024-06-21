from django.db import models
from django.utils import timezone

import uuid

from users.models import UserTable
from vendordetails.models import InventoryDetail

class CategoryDetails(models.Model):
    category_id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    category_name = models.CharField(max_length=120, unique=True)

    class Meta:
        db_table = "category_details"
        managed = True


class StockDetails(models.Model):
    stock_id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    categoryid = models.ForeignKey(CategoryDetails, on_delete=models.CASCADE)
    inventory_id = models.ForeignKey(InventoryDetail, on_delete=models.CASCADE)
    stock_title = models.CharField(max_length=56)
    stock_description = models.CharField(max_length=255)
    stock_price = models.FloatField()
    quantity_available = models.IntegerField(default=0)

    class Meta:
        db_table = "stock_details"
        managed=True


class PurchasedHistory(models.Model):
    purchased_id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    purchased_userid = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(StockDetails, on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField()
    status = models.CharField(max_length=30, default="Order Placed")
    payment_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "purchased_history"
        managed=True
    
    def save(self, *args, **kwargs):
        if self.pk:  # if instance already exists in database
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)