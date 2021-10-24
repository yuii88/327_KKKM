from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# เกี่ยวกับ database การเก็บข้อมูล

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	photo = models.ImageField(upload_to="gallery_photo_profile",null=True,blank=True,default='dafaultprofile.png')
	usertype = models.CharField(max_length=100,default='member')
	cartquan = models.IntegerField(default=0) #เก็บจำนวนสินค้าในตะกร้า

	def __str__(self):
		return self.user.first_name


class Allproduct(models.Model):
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	detail = models.TextField(null=True,blank=True) #null=True,blank=True ใช้คู่กัน
	imageurl = models.CharField(max_length=200,null=True,blank=True)
	instock = models.BooleanField(default=True)
	quantity = models.IntegerField(default=1)
	unit = models.CharField(max_length=200,default='-')
	image = models.ImageField(upload_to="gallery_products",null=True,blank=True)

	def __str__(self): # def ทำให้ชื่อสินค้าแสดงบนหน้า แอดสินค้า admin
		return self.name

class Cart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE) #อ้างอิงถึง User
	productid = models.CharField(max_length=100) # id from database
	productname = models.CharField(max_length=100)
	price = models.IntegerField()
	quantity = models.IntegerField()
	total = models.IntegerField()
	stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class OrderList(models.Model):
	orderid = models.CharField(max_length=100)
	productname = models.CharField(max_length=100)
	price = models.IntegerField()
	quantity = models.IntegerField()
	total = models.IntegerField()

class OrderPending(models.Model):
	orderid = models.CharField(max_length=100)
	user = models.ForeignKey(User,on_delete=models.CASCADE) #บังคับให้ login
	address = models.TextField()
	shipping = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	tel = models.CharField(max_length=100)
	address = models.TextField()
	shipping = models.CharField(max_length=100)
	payment = models.CharField(max_length=100)
	other = models.TextField(max_length=200,null=True,blank=True) #ต้องเพิ่ม blank=True ด้วย
	stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	paid = models.BooleanField(default=False)
	slip = models.ImageField(upload_to="gallery_slip",null=True,blank=True)
	sliptime = models.CharField(max_length=200,null=True,blank=True)
	paymentid = models.CharField(max_length=200,null=True,blank=True)
	trackingnumber = models.CharField(max_length=200,null=True,blank=True)

	def __str__(self): 
		return self.orderid
