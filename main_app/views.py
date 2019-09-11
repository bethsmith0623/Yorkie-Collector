from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

import uuid
import boto3

from .models import Yorkie, Toy, Photo
from .forms import GroomingForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-bs0623'

# Create your views here.

class YorkieCreate(CreateView):
  model = Yorkie
  fields = '__all__'

class YorkieUpdate(UpdateView):
  model = Yorkie
  fields = ['fixed', 'description', 'age', 'registered']

class YorkieDelete(DeleteView):
  model = Yorkie
  success_url = '/yorkies/'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def yorkies_index(request):
  yorkies = Yorkie.objects.all()
  return render(request, 'yorkies/index.html', { 'yorkies': yorkies })

def yorkies_detail(request, yorkie_id):
  yorkie = Yorkie.objects.get(id=yorkie_id)
  toys_yorkie_doesnt_have = Toy.objects.exclude(id__in = yorkie.toys.all().values_list('id'))
  grooming_form = GroomingForm()
  return render(request, 'yorkies/detail.html', 
    {'yorkie': yorkie, 'grooming_form': grooming_form, 'toys': toys_yorkie_doesnt_have })

def add_grooming(request, yorkie_id):
  form = GroomingForm(request.POST)
  if form.is_valid():
    new_grooming = form.save(commit=False)
    new_grooming.yorkie_id = yorkie_id
    new_grooming.save()
  return redirect('detail', yorkie_id=yorkie_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def assoc_toy(request, yorkie_id, toy_id):
  Yorkie.objects.get(id=yorkie_id).toys.add(toy_id)
  return redirect ('detail', yorkie_id=yorkie_id)

def add_photo(request, yorkie_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, yorkie_id=yorkie_id)
      photo.save()
    except:
      print('An error occurred uploading file to s3')
  return redirect('detail', yorkie_id=yorkie_id)