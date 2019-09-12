from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3

from .models import Yorkie, Toy, Photo
from .forms import GroomingForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-bs0623'

# Create your views here.

class YorkieCreate(LoginRequiredMixin, CreateView):
  model = Yorkie
  fields = ['name', 'gender', 'fixed', 'sire', 'dame', 'description', 'age', 'registered']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class YorkieUpdate(LoginRequiredMixin, UpdateView):
  model = Yorkie
  fields = ['fixed', 'description', 'age', 'registered']

class YorkieDelete(LoginRequiredMixin, DeleteView):
  model = Yorkie
  success_url = '/yorkies/'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def yorkies_index(request):
  yorkies = Yorkie.objects.filter(user=request.user)
  return render(request, 'yorkies/index.html', { 'yorkies': yorkies })

@login_required
def yorkies_detail(request, yorkie_id):
  yorkie = Yorkie.objects.get(id=yorkie_id)
  toys_yorkie_doesnt_have = Toy.objects.exclude(id__in = yorkie.toys.all().values_list('id'))
  grooming_form = GroomingForm()
  return render(request, 'yorkies/detail.html', 
    {'yorkie': yorkie, 'grooming_form': grooming_form, 'toys': toys_yorkie_doesnt_have })

@login_required
def add_grooming(request, yorkie_id):
  form = GroomingForm(request.POST)
  if form.is_valid():
    new_grooming = form.save(commit=False)
    new_grooming.yorkie_id = yorkie_id
    new_grooming.save()
  return redirect('detail', yorkie_id=yorkie_id)

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, yorkie_id, toy_id):
  Yorkie.objects.get(id=yorkie_id).toys.add(toy_id)
  return redirect ('detail', yorkie_id=yorkie_id)

@login_required
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)