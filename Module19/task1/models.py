from django.db import models

# Create your models here.
class Buyer(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(decimal_places=2, max_digits=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200)
    cost = models.DecimalField(decimal_places=2, max_digits=100)
    size = models.DecimalField(decimal_places=2, max_digits=100)
    description = models.TextField()
    age_limited = models.BooleanField(default=False)
    buyer = models.ManyToManyField(Buyer, related_name="games")
    DecimaField = models.DecimalField(decimal_places=10, max_digits=100)
    BooleanField = models.BooleanField()

    def __str__(self):
        return self.title