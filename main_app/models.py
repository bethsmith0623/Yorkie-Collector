from django.db import models

# Create your models here.
class Yorkie(models.Model):
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=25, default='male')
    fixed = models.BooleanField(default=False)
    sire = models.CharField(max_length=150)
    dame = models.CharField(max_length=150)
    description = models.TextField(max_length=300)
    age = models.IntegerField()
    registered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.id})'