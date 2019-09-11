from django.contrib import admin
from .models import Yorkie, Grooming, Toy, Photo

# Register your models here.
admin.site.register(Yorkie)
admin.site.register(Grooming)
admin.site.register(Toy)
admin.site.register(Photo)