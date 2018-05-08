from django.db import models
from django.utils import timezone


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    # created_date = models.DateTimeField( #  Removed created date
    #         default=timezone.now)
    expiration_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    # created_date = models.DateTimeField( #Not Needed
    #         default=timezone.now)
    # standard = models.BooleanField(default=False) # Not needed
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
