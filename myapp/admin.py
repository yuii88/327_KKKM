from django.contrib import admin
from .models import * # ดึง ไฟล์ 


admin.site.site_header = 'KKKM SHOP ADMIN'
admin.site.index_title = 'Main Admin'
admin.site.site_title = 'KKKM BACKEND'

class AllproductAdmin(admin.ModelAdmin):
	list_display = ['name','id','instock','price','quantity']
	list_editable = ['instock','price','quantity']

admin.site.register(Allproduct,AllproductAdmin) #แสดง Allproduct ที่ Site administration
admin.site.register(Profile)
admin.site.register(Cart)



class OrderListAdimin(admin.ModelAdmin):
	list_display = ['orderid','productname','total']

admin.site.register(OrderList,OrderListAdimin)
admin.site.register(OrderPending)