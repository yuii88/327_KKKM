#urls.py
from django.urls import path, include
from .views import *
# .views ดึงไฟล์เข้ามาใช้ 
urlpatterns = [
	path('', Home, name='home-page'),
	path('about/', About, name='about-page'),
	path('contact/',Contact, name='contact-page'),
	path('FILA/',Fila, name='fila_bts-page'),
	path('addproduct/',AddProduct, name='addproduct-page'),
	path('allproduct/',ProductTotal, name='allproduct-page'),
	path('register/',Register, name='register-page'), #locallhost:8000/register
	path('addtocart/<int:pid>/',AddtoCart,name='addtocart-page'), #<int:pid> is number of product
	path('mycart/',MyCart,name='mycart-page'),
	path('mycart/edit/',MyCartEdit,name='mycartedit-page'),
	path('checkout/',Checkout,name='checkout-page'),
	path('orderlist/',OrderListPage,name='orderlist-page'),
	path('allorderlist/',AllOrderListPage,name='allorderlist-page'),
	path('uploadslip/<str:orderid>/',UploadSlip,name='uploadslip-page'),
	path('updatestatus/<str:orderid>/<str:status>/',UpdatePaid,name='updatestatus'),
	path('updatetracking/<str:orderid>/',UpdateTracking,name='updatetracking'),

]