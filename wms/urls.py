from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('add-item/', views.add_item, name='add_item'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
]
