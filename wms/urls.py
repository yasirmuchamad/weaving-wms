from django.urls import path
from . import views

app_name = 'wms'
urlpatterns = [
    path('item', views.item_list, name='item_list'),
    path('item/add-item/', views.add_item, name='add_item'),
    path('location', views.location_list, name='location_list'),
    path('location/add-location/', views.add_location, name='add_location'),
    path('subdept', views.subdepartement_list, name='subdept_list'),
    path('subdept/add-subdept/', views.add_subdepartement, name='add_subdept'),
    path('transaction', views.transaction_list, name='transaction_list'),
    path('transaction/add-transaction/', views.add_transaction, name='add_transaction'),
]
