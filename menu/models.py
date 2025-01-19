# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class ProductToppings(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    topping = models.ForeignKey('Toppings', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'product_toppings'


class Products(models.Model):
    PRODUCT_TYPE = [('Veg', 'Veg'), ('Non-Veg','Non-Veg')]

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    product_price = models.DecimalField(decimal_places=2, max_digits=5)
    product_category = models.CharField(max_length=100)
    product_type = models.CharField(max_length=7, choices=PRODUCT_TYPE)

    class Meta:
        managed = True
        db_table = 'products'


class Ratings(models.Model):
    rating_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    rating_value = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        managed = True
        db_table = 'ratings'


class Toppings(models.Model):
    topping_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(ProductToppings, models.DO_NOTHING)
    topping_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'toppings'


class ToppingsGroups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'toppings_groups'
