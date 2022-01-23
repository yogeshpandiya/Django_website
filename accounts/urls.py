from django.urls import path
from . import views

urlpatterns = [

    path('Home', views.home, name='home'),
    path('', views.home, name='home'),
    path('Login', views.Login, name='Login'),
    path('ULogin', views.ULogin, name='Login'),
    path('SignUp', views.SignUp, name='SignUp'),
    path('Submit', views.Submit, name='Submit'), 
    #path('Manager', views.Manager, name='manager'),     
    
    path('dashboard', views.dashBoard, name="dashboard"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),

    #------------ (CREATE URLS) ------------
    path('create_order/', views.createOrder, name="create_order"),

    path('create_cst/', views.create_cst, name="create_cst"),

    path('Submit_cst', views.Submit_cst, name="Submit_cst"),

    #------------ (UPDATE URLS) ------------
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),


    #------------ (UPDATE URLS) ------------
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    #--------------------ADD PRODUCT----------

    path('Add_Product/', views.addproduct, name="addproduct"),

    path('Submit_Product', views.Submit_Product, name="Submit_Product"),
]
