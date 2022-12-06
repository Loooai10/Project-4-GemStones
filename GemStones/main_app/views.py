from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserImage 
from .models import UploadImage 
import uuid
import boto3
from .models import *

def image_request(request):  
    if request.method == 'POST':  
        form = UserImageForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
              
            return render(request, 'image_form.html', {'form': form, 'img_obj': img_object})  
    else:  
        form = UserImageForm()  
  
    return render(request, 'image_form.html', {'form': form}) 

class ProductCreate(LoginRequiredMixin, CreateView):
      model = Product
      fields = ['name', 'price', 'description']
  # This inherited method is called when a
  # valid cat form is being submitted
      def form_valid(self, form):
    # Assign the logged in user (self.request.user)
       form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
       return super().form_valid(form)

class ProductUpdate(UpdateView):
    model = Product
    fields = ['name', 'price', 'description']

class ProductDelete(DeleteView):
    model = Product
    success_url = '/products/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

# @login_required
def products_index(request):
  products = Product.objects.all()
  return render(request, 'products/index.html', { 'products': products })

# @login_required
def products_detail(request, product_id):
  product = Product.objects.get(id=product_id)
# Get the toys the cat doesn't have
  offers_product_doesnt_have = Offer.objects.exclude(id__in = product.offers.all().values_list('id'))
  # instantiate FeedingForm to be rendered in the template
  return render(request, 'products/detail.html', {
    # Pass the cat and feeding_form as context
    # Add the toys to be displayed
    'product': product,
    'offers': offers_product_doesnt_have
  })
@login_required
def assoc_offer(request, product_id, offer_id):
  Product.objects.get(id=product_id).offers.add(offer_id)
  return redirect('detail', product_id=product_id)

@login_required
def unassoc_offer(request, product_id, offer_id):
  Product.objects.get(id=product_id).offers.remove(offer_id)
  return redirect('detail', product_id=product_id)

class OfferList(LoginRequiredMixin, ListView):
  model = Offer

class OfferDetail(LoginRequiredMixin, DetailView):
  model = Offer

class OfferCreate(LoginRequiredMixin, CreateView):
  model = Offer
  fields = '__all__'

class OfferUpdate(LoginRequiredMixin, UpdateView):
  model = Offer
  fields = ['buyer', 'status', 'price']

class OfferDelete(LoginRequiredMixin, DeleteView):
  model = Offer
  success_url = '/offers/'


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
      error_message = 'Invalid credentials - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
