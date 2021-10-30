from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from datetime import datetime

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


def AddtoCart(request,pid): #pid is product id which get from url (<int:pid>)
	# localhost:8000/addtocard/4 (<int:pid>) เท่ากับ {% url 'addtocard-page' pd.id %}
	#print('CURRENT USER :',request.user) #test
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid) # check รายละเอียด ใน model 
	
	try:
		# กรณีที่ตัวสินค้ามีซ้ำ
		newcart = Cart.objects.get(user=user,productid=str(pid)) 
		#print('EXISTS: ',pcheck.exists())
		newquan = newcart.quantity + 1
		newcart.quantity= newquan
		calculate = newcart.price* newquan
		newcart.total = calculate
		newcart.save()

		# update จำนวนที่มีจำนวนของตะกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')
	except:

		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1
		calculate = int(check.price)*1
		newcart.total = calculate
		newcart.save()

		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('allproduct-page')

def MyCart(request):
	username = request.user.username #ออกมาเป็น string
	user = User.objects.get(username=username) #ออกมาเป็น objects
	context = {}
	if request.method == 'POST' :
		# ใช้สำหรับการลบเท่านั้น
		data = request.POST.copy()
		productid = data.get('productid')
		print('PID', productid)
		item = Cart.objects.get(user=user,productid=productid) 
		item.delete()
		context['status'] = 'delete'

		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

	mycart = Cart.objects.filter(user=user) #ใช้ .get ไม่ได้ เพราะ multiple (มีหลายอัน) ต้องใช้ filter เพราะ มีหลาย record 
	count = sum([ c.quantity for c in mycart])
	total = sum([ c.total for c in mycart])

	context['mycart'] = mycart
	context['count'] = count
	context['total'] = total
	return render(request,'myapp/mycart.html',context)

def MyCartEdit(request):
	username = request.user.username #get ค่าว่าใครกำลังloginอยู่ตอนนี้ #ออกมาเป็น string
	user = User.objects.get(username=username) #search ว่า usernameนี้เป็นใคร #ออกมาเป็น objects
	context = {}

	if request.method == 'POST' : 
		data = request.POST.copy()
		#print(data)
		if data.get('clear') == 'clear':
			print(data.get('clear'))
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')

		editlist = []

		for k,v in data.items():
			#print(k,v)
			# pv_7
			if k[:2] == 'pd':
				pid = int(k.split('_')[1]) 
				dt = [pid,int(v)]
				editlist.append(dt)
		#print('EDITLIST: ', editlist) #[[5, 5], [10, 6]] 10=productid,6=quan

		for ed in editlist:
			edit = Cart.objects.get(productid=ed[0],user=user) #productid
			edit.quantity = ed[1] #quan
			calculate = edit.price * ed[1]
			edit.total = calculate
			edit.save()



		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('mycart-page')
		#if data.get('checksave') =='checksave':
		#return redirect('mycart-page')

	mycart = Cart.objects.filter(user=user) #ใช้ .get ไม่ได้ เพราะ multiple (มีหลายอัน) ต้องใช้ filter เพราะ มีหลาย record 
	context['mycart'] = mycart
	return render(request,'myapp/mycartedit.html',context)


def Checkout(request):
	username = request.user.username #ออกมาเป็น string
	user = User.objects.get(username=username)
	if request.method == 'POST' :
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')
		if page == 'information':
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['address'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other

			mycart = Cart.objects.filter(user=user) 
			count = sum([ c.quantity for c in mycart])
			total = sum([ c.total for c in mycart])

			context['mycart'] = mycart
			context['count'] = count
			context['total'] = total
			
			return render(request, 'myapp/checkout2.html',context)
		if page == 'confirm':
			print('Confirm')
			print(data)
			mycart = Cart.objects.filter(user=user) # [['a','10']]

			# id = OD0007 2020 09 03 22 00 30
			# id = OD 0007 20200903220030
			mid = str(user.id).zfill(4)
			dt = datetime.now().strftime('%Y%m%d%H%M%S') # can search on google : what is strftime ?
			orderid = 'OD' + mid + dt

			for pd in mycart:
				order = OrderList()
				order.orderid = orderid
				order.productid = pd.productid
				order.productname = pd.productname
				order.price = pd.price
				order.quantity = pd.quantity
				order.total= pd.total
				order.save()

			# create order pending

			odp = OrderPending()
			odp.orderid = orderid
			odp.user = user
			odp.name = name
			odp.tel = tel
			odp.address = address
			odp.shipping = shipping
			odp.payment = payment
			odp.other = other
			odp.save()

			# clear cart
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')


			# generate order no. and save to Order Models
			# save product in cart to OrderProduct models
			# clear cart
			# redirect to order list page

	return render(request, 'myapp/checkout1.html')

def OrderListPage(request):
	username = request.user.username #ออกมาเป็น string
	user = User.objects.get(username=username) #ออกมาเป็น objects
	context = {}

	order = OrderPending.objects.filter(user=user)
	'''
	-order
		-orderid: OD2105012
		-user:
		-name: ผู้รับ

	'''
	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid) 
		'''
		-orlist
			-object (1)
			-orderid: OD102150
			-product: เสื้อม่วง
			-total: 280
			-object (2)
			-orderid: OD20235
			-product: เสื้อฟ้า
			-total: 260

		'''
		total = sum([ c.total for c in odlist])
		# total = sum([280,260])
		od.total = total
		#สั่งนับว่า order นี่มีจำนวนกี่ชิ้น
		count = sum([ c.quantity for c in odlist])

		if od.shipping == 'ems':
			shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		else:
			shipcost = sum([30 if i == 0 else 10 for i in range(count)])
		
		if od.payment == 'cod':
			shipcost += 30 
		od.shipcost = shipcost


	context['allorder'] = order


	return render(request, 'myapp/orderlist.html',context)

def AllOrderListPage(request):

	context = {}
	order = OrderPending.objects.all()

	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid) 
		total = sum([ c.total for c in odlist])
		od.total = total

		count = sum([ c.quantity for c in odlist])

		if od.shipping == 'ems':
			shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		else:
			shipcost = sum([30 if i == 0 else 10 for i in range(count)])
		
		if od.payment == 'cod':
			shipcost += 30 
		od.shipcost = shipcost



	context['allorder'] = order


	return render(request, 'myapp/allorderlist.html',context)


def UploadSlip(request,orderid):
	print('ODER ID: ',orderid)

	if request.method == 'POST' and request.FILES['slip']:
		data = request.POST.copy()
		sliptime = data.get('sliptime')
	
		update = OrderPending.objects.get(orderid=orderid)
		update.sliptime = sliptime
		file_image = request.FILES['slip'] #file ที่เรา upload มา (ที่กด submit)
		file_image_name = request.FILES['slip'].name.replace(' ','') # ทำช่องว่างให้ติดกัน
		print('FILE_IMAGE:',file_image)
		print('IMAGE_NAME:',file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		update.slip = upload_file_url[6:]
		update.save()


	odlist = OrderList.objects.filter(orderid=orderid) #odlist คือ allorderlist
	total = sum([ c.total for c in odlist])
	oddetail = OrderPending.objects.get(orderid=orderid) 
	# คำนวณค่าส่งตามประเภท
	count = sum([ c.quantity for c in odlist])
	if oddetail.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
	else:
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	
	if oddetail.payment == 'cod':
		shipcost += 30 

	context = {'orderid':orderid,
			   'total':total,
			   'shipcost':shipcost,
			   'grandtotal':total+shipcost,
			   'oddetail':oddetail,
			   'count':count}

	


# shipcost = รวมค่าทั้งหมด (หากเป็นชิ้นแรกค่าส่งจะคิด 50บาท ชิ้นถัดไปชิ้นละ10บาท)
	return render(request,'myapp/uploadslip.html',context)



def UpdatePaid(request,orderid,status):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	order = OrderPending.objects.get(orderid=orderid)
	if status == 'confirm':
		order.paid = True
	elif status == 'cancel':
		order.paid = False
	order.save()
	return redirect('allorderlist-page')

def UpdateTracking(request,orderid):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')


	if request.method == 'POST' : # มีการกด submit ค่าจาก html ก็จะ get ค่า
		order = OrderPending.objects.get(orderid=orderid)
		data = request.POST.copy()
		trackingnumber = data.get('trackingnumber')
		order.trackingnumber = trackingnumber
		order.save()
		return redirect('allorderlist-page')


	order = OrderPending.objects.get(orderid=orderid)
	odlist = OrderList.objects.filter(orderid=orderid) 

	total = sum([ c.total for c in odlist])
	order.total = total
	# คำนวณค่าส่งตามประเภท
	count = sum([ c.quantity for c in odlist])
	
	if order.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
	else:
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	
	if order.payment == 'cod':
		shipcost += 30 
	order.shipcost = shipcost

	context = {'order':order,'odlist':odlist,'total':total,'count':count}
		

	return render(request,'myapp/updatetracking.html',context)
	
def MyOrder(request,orderid):
	username = request.user.username # check user that has login
	user = User.objects.get(username=username) #ออกมาเป็น objects

	order = OrderPending.objects.get(orderid=orderid)
	odlist = OrderList.objects.filter(orderid=orderid) 

	total = sum([ c.total for c in odlist])
	order.total = total
	# คำนวณค่าส่งตามประเภท
	count = sum([ c.quantity for c in odlist])

	if order.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
	else:
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	
	if order.payment == 'cod':
		shipcost += 30 
	order.shipcost = shipcost

	context = {'order':order,'odlist':odlist,'total':total,'count':count}
	
	return render(request,'myapp/myorder.html',context)
