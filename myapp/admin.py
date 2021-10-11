from django.contrib import admin
from .models import Allproduct ,Profile # ดึง ไฟล์ 
# Register your models here.

admin.site.register(Allproduct) #แสดง Allproduct ที่ Site administration
admin.site.register(Profile)