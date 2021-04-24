from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customers/<str:pk_test>/', views.customers, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name="createOrder"),
    path('update_order/<str:pk>', views.updateOrder, name="updateOrder"),
    path('delete/<str:pk>', views.deleteOrder, name="deleteOrder"),
    path('create_customer/', views.createCustomer, name="createCustomer"),
    path('create_product/', views.createProduct, name="createProduct"),
    path('report/', views.ReportPage, name="report"),
]