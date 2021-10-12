from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

#HttpResponse คือ function สำหรับทำให้แสดงข้อความหน้าเว็บไซต์ได้

#เกี่ยวกับหน้า homepage 
# Create your views here.
def Home(request):
	product = Allproduct.objects.all().order_by('id').reverse()[:3]
	preorder = Allproduct.objects.filter(quantity__lte=0) 
	# quanlity__lte=0 (หาค่าที่ quantity <= 0 - lte is <= ) (underscore 2 ตัว)
	#quantity__gt=0 (หาค่าที่ quantity > 0 - gt is >)
	#quantity__gte=0 (หาค่าที่ quantity >= 5 - gte is >=)
	context = {'product':product,'preorder':preorder}
	return render(request, 'myapp/home.html',context)
	
def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Fila(request):
	return render(request, 'myapp/FILA.html')	

#from django.contrib.auth.models import User
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

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()

		#from django.contrib.auth import authenticate,login
		user = authenticate(username=email,password=password) 
		login(request,user) #ให้คนที่มีการ login ในระบบทำการloginเข้าไปเลย (Auto login)

	return render(request,'myapp/register.html')


def AddtoCart(request,pid):
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)

	newcart = Cart()
	newuser.user = user
	newcart.productid = pid 
	newcart.productname = check.name
	newcart.price = int(check.price)
	newcart.quantity = 1
	calculate = int(check.price)*1
	newcart.total = calculate
	newcart.save()
	return redirect('allproduct-page')





