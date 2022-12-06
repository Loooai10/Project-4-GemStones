from django.urls import path, include
from . import views
from .views import image_request 

# app_name = 'sampleapp'  
urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('products/<int:product_id>/image_request/', views.image_request, name = "image-request"), 
  path('products/', views.products_index, name='index'),
  path('products/<int:product_id>/', views.products_detail, name='detail'),
  path('products/create/', views.ProductCreate.as_view(), name='products_create'),
  path('products/<int:pk>/update/', views.ProductUpdate.as_view(), name='product_update'),
  path('products/<int:pk>/delete/', views.ProductDelete.as_view(), name='product_delete'),
  # path('products/<int:product_id>/add_offering/', views.add_offering, name='add_offering'),
  # associate a toy with a cat (M:M)
  path('products/<int:product_id>/assoc_offer/<int:offer_id>/', views.assoc_offer, name='assoc_offer'),
  # unassociate a toy and cat
  path('products/<int:product_id>/unassoc_offer/<int:offer_id>/', views.unassoc_offer, name='unassoc_offer'),
  # path('cats/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),
  path('offers/', views.OfferList.as_view(), name='offers_index'),
  path('offers/<int:pk>/', views.OfferDetail.as_view(), name='offers_detail'),
  path('offers/create/', views.OfferCreate.as_view(), name='offers_create'),
  path('offers/<int:pk>/update/', views.OfferUpdate.as_view(), name='offers_update'),
  path('offers/<int:pk>/delete/', views.OfferDelete.as_view(), name='offers_delete'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup', views.signup, name='signup'),
  ]