from django.db import models
from django.urls import reverse
from datetime import date

CARE = (
    ('C', 'Coat brushing'),
    ('T', 'Toothbrushing'),
    ('B', 'Bath time')
)

# Create your models here.

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})


class Yorkie(models.Model):
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=25)
    fixed = models.BooleanField(default=False)
    sire = models.CharField(max_length=150)
    dame = models.CharField(max_length=150)
    description = models.TextField(max_length=300)
    age = models.IntegerField()
    registered = models.BooleanField(default=False)
    toys = models.ManyToManyField(Toy)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'yorkie_id': self.id})

    def care_for_today(self):
        return self.grooming_set.filter(date=date.today()).count() >= len(CARE)

class Grooming(models.Model):
    date = models.DateField('Grooming date')
    care = models.CharField(
        max_length=1,
        choices=CARE,
        default=CARE[0][0]
    )
    class Meta:
        ordering = ['-date']

    yorkie = models.ForeignKey(Yorkie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_care_display()} on {self.date}"
    
