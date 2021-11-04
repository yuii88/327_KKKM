#readdb.py
import csv 
import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

with conn:
	c.execute("""SELECT * FROM myapp_orderpending WHERE user_id=3 """)
	data = c.fetchall() # ดึงข้อมูลออกมาทั้งหมด
	#print(data) # แสดงเป็น list
	#data = [(1,'shirt',30),(2,'shirt small',40)]
	for d in data:
		print(d)
		print('----')

	with open('cart_user3.csv','w',newline='',encoding='utf-8') as f:
		fw = csv.writer(f) # File Write
		fw.writerows(data)
	