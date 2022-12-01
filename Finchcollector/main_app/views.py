from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Feather
from .forms import SightingForm
from django.views.generic import ListView, DetailView
# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-east-1.amazonaws.com/'
BUCKET = 'finchcollector'


class FinchCreate(LoginRequiredMixin, CreateView):
  model = Finch
  fields = ['name', 'species', 'description', 'age']
  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class FinchUpdate(UpdateView):
  model = Finch
  fields = ['name', 'species', 'description', 'age']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def finches_index(request):
  finches = Finch.objects.all()
  return render(request, 'finches/index.html', { 'finches': finches })

@login_required
def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
# Get the toys the cat doesn't have
  feathers_finch_doesnt_have = Feather.objects.exclude(id__in = finch.feathers.all().values_list('id'))
  # instantiate FeedingForm to be rendered in the template
  sighting_form = SightingForm()
  return render(request, 'finches/detail.html', {
    # pass the cat and feeding_form as context
    'finch': finch, 'sighting_form': sighting_form,
   # Add the toys to be displayed
    'feathers': feathers_finch_doesnt_have
  })

@login_required
def add_sighting(request, finch_id):
	# create the ModelForm using the data in request.POST
  form = SightingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_sighting = form.save(commit=False)
    new_sighting.finch_id = finch_id
    new_sighting.save()
  return redirect('detail', finch_id=finch_id)

@login_required
def add_photo(request, finch_id):
	# photo-file was the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      photo = Photo(url=url, finch_id=finch_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', finch_id=finch_id)

@login_required
def assoc_feather(request, finch_id, feather_id):
  Finch.objects.get(id=finch_id).feathers.add(feather_id)
  return redirect('detail', finch_id=finch_id)

@login_required
def unassoc_feather(request, finch_id, feather_id):
  Finch.objects.get(id=finch_id).feathers.remove(feather_id)
  return redirect('detail', finch_id=finch_id)

class FeatherList(LoginRequiredMixin, ListView):
  model = Feather

class FeatherDetail(LoginRequiredMixin, DetailView):
  model = Feather

class FeatherCreate(LoginRequiredMixin, CreateView):
  model = Feather
  fields = '__all__'

class FeatherUpdate(LoginRequiredMixin, UpdateView):
  model = Feather
  fields = ['name', 'color']

class FeatherDelete(LoginRequiredMixin, DeleteView):
  model = Feather
  success_url = '/feathers/'

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
  # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)