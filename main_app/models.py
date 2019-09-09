from django.db import models

# Create your models here.
class Yorkie(models.Model):
    name = 
    sire = 
    dame = 
    description = 
    age = 

    def __str__(self):
        return f'{self.name} ({self.id})'