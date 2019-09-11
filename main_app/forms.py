from django.forms import ModelForm
from .models import Grooming


class GroomingForm(ModelForm):
    class Meta: 
        model = Grooming
        fields = ['date', 'care']
