from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.generic.edit import CreateView
# Add UdpateView & DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch
# ...
class FinchUpdate(UpdateView):
      model = Finch
  # Let's disallow the renaming of a cat by excluding the name field!
      fields = ['breed', 'description', 'age']
      success_url = '/finchs/'

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finchs/'

class FinchCreate(CreateView):
      model = Finch
      fields = '__all__'
      success_url='/finchs/'
# class CatCreate(CreateView):
#       model = Cat
#       fields = ['name', 'breed', 'description', 'age']
        
def finchs_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  return render(request, 'finchs/detail.html', { 'finch': finch})

def finchs_index(request):
  finchs = Finch.objects.all()
  return render(request, 'finchs/index.html', { 'finchs': finchs })


# class Cat:
#   def __init__(self, name, breed, description, age):
#     self.name = name
#     self.breed = breed
#     self.description = description
#     self.age = age

# cats = [
#   Cat('Lolo', 'tabby', 'foul little demon', 3),
#   Cat('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
#   Cat('Raven', 'black tripod', '3 legged cat', 4)
# ]

# View functions

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# def cats_index(request):
#   return render(request, 'cats/index.html', { 'cats': cats})