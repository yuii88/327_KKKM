from django.db import models

# Create your models here.
# เกี่ยวกับ database การเก็บข้อมูล
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

