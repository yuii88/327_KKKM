from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Allproduct
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
#HttpResponse คือ function สำหรับทำให้แสดงข้อความหน้าเว็บไซต์ได้

#เกี่ยวกับหน้า homepage 
# Create your views here.
def Home(request):
	# request คือ สิ่งที่ร้องขอจากเว็บไซต์
	#return HttpResponse('<h2>hello world</h2>')
	
	product1 = 'เสื้อสีม่วงFILA'
	product2 = 'เสื้อสีดำ'
	product3 = 'เสื้อ Love YourSelf'

	context = {'product1':product1,'product2':product2,'product3':product3}
	return render(request, 'myapp/home.html',context)
	
def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Fila(request):
	return render(request, 'myapp/FILA.html')	


#เป็นการดึงมาจากหน้า addproduct.html หากมีการกด ส่งหรือsubmit (POST=submit) data 
def AddProduct(request):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')


	if request.method == 'POST' and request.FILES['imageupload']:
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')
#สร้าง database ต้องมี model
		new = Allproduct() #models ชื่อ Allproduct
		new.name = name
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit
		###########Save Image#############
		file_image = request.FILES['imageupload'] #file ที่เรา upload มา (ที่กด submit)
		file_image_name = request.FILES['imageupload'].name.replace(' ','') # ทำช่องว่างให้ติดกัน
		print('FILE_IMAGE:',file_image)
		print('IMAGE_NAME:',file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		new.image = upload_file_url[6:]
		##################################
		new.save()

	return render(request, 'myapp/addproduct.html')		

def ProductTotal(request):
	product = Allproduct.objects.all().order_by('id').reverse() #ดึงข้อมูลมาทั้งหมดจากmodel (Allproduct) 

	context = {'product':product} #เอาข้อมูลที่เอามาจาก Alproduct โยนไปใน 'product'
	return render(request, 'myapp/allproduct.html',context)	



def Register(request):
	if request.method == 'POST' :
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')


		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save() 

	return render(request,'myapp/register.html')





