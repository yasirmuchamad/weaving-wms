from django.urls import path
from . import views

app_name = 'wms'
urlpatterns = [
    path('item', views.item_list, name='item_list'),
    path('item/add-item/', views.add_item, name='add_item'),
    path('transaction', views.transaction_list, name='transaction_list'),
    path('transaction/add-transaction/', views.add_transaction, name='add_transaction'),
]
