from django.urls import path
from . import views

app_name = 'wms'
urlpatterns = [
    path('item', views.item_list, name='item_list'),
    path('item/add-item/', views.add_item, name='add_item'),
    path('item/update/<int:pk>', views.update_item, name='update_item'),
    path('item/delete/<int:pk>', views.delete_item, name='delete_item'),
    path('item/export', views.export_itemToExcel, name='export_item'),
    path('item/print', views.print_itemToPdf, name='print_item'),

    path('location', views.location_list, name='location_list'),
    path('location/add-location/', views.add_location, name='add_location'),
    path('location/update/<int:pk>', views.update_location, name='update_location'),
    path('location/delete/<int:pk>', views.delete_location, name='delete_location'),
    path('location/export', views.export_locationToExcel, name='export_location'),
    path('location/print', views.print_locationToPdf, name='print_location'),

    path('subdept', views.subdepartement_list, name='subdept_list'),
    path('subdept/add-subdept/', views.add_subdepartement, name='add_subdept'),
    path('subdept/update/<int:pk>', views.update_subdepartement, name='update_subdept'),
    path('subdept/delete/<int:pk>', views.delete_subdepartement, name='delete_subdept'),
    path('subdept/export', views.export_subdeptToExcel, name='export_subdept'),
    path('subdept/print', views.print_subdeptToPdf, name='print_subdept'),
    
    path('transaction', views.transaction_list, name='transaction_list'),
    path('transaction/add-transaction/', views.add_transaction, name='add_transaction'),
    path('transaction/export', views.export_transaksiToExcel, name='export_transaction'),
    path('transaction/print', views.print_transactionToPdf, name='print_transaction'),
    path('transaction/filter', views.filter_transaction, name='filter_transaction')
]
