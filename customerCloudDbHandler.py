import os

from google.appengine.api import memcache
from google.appengine.api import rdbms
from datetime import datetime
import time
import MySQLdb
from datetime import date, timedelta


_INSTANCE_NAME_GEN = 'momdata:us-central1:momdata'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'admin'



def connect_to_cloudsql(dbname):

	# When deployed to App Engine, the `SERVER_SOFTWARE` environment variable will be set to 'Google App Engine/version'.
	if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
		# Connect using the unix socket located at /cloudsql/cloudsql-connection-name.
		cloudsql_unix_socket = os.path.join('/cloudsql', _INSTANCE_NAME_GEN)

		db = MySQLdb.connect( unix_socket=cloudsql_unix_socket, user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname)

	# If the unix socket is unavailable, then try to connect using TCP. This will work if you're running a local MySQL server or using the Cloud SQL proxy, for example: cloud_sql_proxy -instances=your-connection-name=tcp:3306
	else:
		db = MySQLdb.connect(
			host='34.67.150.233',  user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname)

	return db


def connect_to_cloudsql_hindi(dbname):

	# When deployed to App Engine, the `SERVER_SOFTWARE` environment variable will be set to 'Google App Engine/version'.
	if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
		# Connect using the unix socket located at /cloudsql/cloudsql-connection-name.
		cloudsql_unix_socket = os.path.join('/cloudsql', _INSTANCE_NAME_GEN)

		db = MySQLdb.connect( unix_socket=cloudsql_unix_socket, user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname, charset='utf8', use_unicode=True)

	# If the unix socket is unavailable, then try to connect using TCP. This will work if you're running a local MySQL server or using the Cloud SQL proxy, for example: cloud_sql_proxy -instances=your-connection-name=tcp:3306
	else:
		db = MySQLdb.connect(
			host='34.67.150.233',  user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname, charset='utf8', use_unicode=True)

	return db


class AddData():
	def addUserPromoUsage(self, mobile, promocode):
		dbname = 'MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO promo_usage (mobile, promocode, usageCount) VALUES ('%s','%s',%s) on duplicate key update usageCount= usageCount + 1 "%(mobile, promocode, 1)
		print _sqlc_
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid


	def addPricingInfo(self, orderId, totalPrice, chefPrice, momPrice, packagingPrice, tax_amount, discount_amount, subTotal,  delivery_charge, promoCode, chefDiscountVal, momDiscountVal, status):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO order_price_info (orderId, totalPrice, chefPrice, momPrice, packagingCharge, taxAmount, discountAmount, subTotal,  deliveryCharge, couponApplied, chefCouponAmount, momCouponAmount, status) VALUES ('%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s')"%(orderId, totalPrice, chefPrice, momPrice, packagingPrice, tax_amount, discount_amount, subTotal,  delivery_charge, promoCode, chefDiscountVal, momDiscountVal, status)
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)



	def addUser(self,name,email,mobile,address,latitude,longitude):

		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO customer_login (name,email,mobile,address,latitude,longitude) VALUES ('%s','%s','%s','%s','%s','%s')"%(name,email,mobile,address,latitude,longitude)

			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addToken(self,mobile,fcmToken):
		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO `customer_token` (`mobile`,`fcmToken`) VALUES ( '%s', '%s')"%(mobile,fcmToken)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addAddress(self,mobile,address,latitude,longitude,phone_number,name):
		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO `customer_address` (mobile,address,latitude,longitude,phone_number,name) VALUES ( '%s', '%s','%s','%s', '%s','%s')"%(mobile,address,latitude,longitude,phone_number,name)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)


	def addImages(self,offer,image_name):
		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO `offer_zone` (`offer`,`image_name`) VALUES ( '%s', '%s')"%(offer,image_name)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addorderlist(self,name,location,price,mobile,total_price,latitude,longitude,food_item,quantity,item_id,ptype,itemActualPrice,mom_mobile,orderId,itemDescription,image,note, promoCode):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO orderInfo (name,location,price,mobile,total_price,latitude,longitude,food_item,quantity,itemId,ptype,itemActualPrice,mom_mobile,orderId,orderStatus,itemDescription,image,note, promoCode) VALUES ( '%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s','%s','%s','%s','%s','%s', '%s')"%(name,location,price,mobile,total_price,latitude,longitude,food_item,quantity,item_id,ptype,itemActualPrice,mom_mobile,orderId,'Waiting for Acceptance', itemDescription, image, note, promoCode)
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)

	def addDelivery(self,name,mobile,address,driveringLicense,aadharNo,vehicleNo,companyName,companyId):
		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO delivery_registration (name,mobile,address,driveringLicense,aadharNo,vehicleNo,companyName,companyId) VALUES ( '%s', '%s','%s', '%s','%s', '%s','%s', '%s')"%(name,mobile,address,driveringLicense,aadharNo,vehicleNo,companyName,companyId)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addCancelBooking(self, orderId):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO completeOrderInfo (SELECT * FROM orderInfo where orderId='%s')"%(str(orderId))
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)

	def addOrderInfo(self, orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO orderInfo (orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode) VALUES ('%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s','%s','%s')"%(orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode)
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid

	def addOrderInfoStatus(self, orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO orderInfo (orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode, status) VALUES ('%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s','%s','%s', '%s')"%(orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode, -1)
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)
	def addOrderItemInfo(self, itemInfoListSet):
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		for line in itemInfoListSet:
			_sqlc_ = "INSERT INTO orderItemInfo (orderId, food_item, quantity, itemId, pType, itemActualPrice, price, itemDescription, images) VALUES ('%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s')"%(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8])
			cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid

	def addOrderIdIncrease(self):
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO orderId (orderDone) VALUES ('%s')"%('2')
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid






		#######################################################################################################

class GetData():

	def getCustomerVersion(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select id,appName,version,versionCode,flag, updateOn, momCheffVersion from userVersion order by id desc limit 1"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getOrderDataBy(self, orderId):
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlcmd_ ="SELECT * from orderInfo where orderId='%s'"%(orderId)
		print _sqlcmd_
		cursor.execute(_sqlcmd_)
		dbDetails=[]
		dbDetails = cursor.fetchall()
		conn.commit()
		conn.close()
		return dbDetails



	def getUsageLimit(self, mobile, promoCode):
		# try:
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd = "SELECT * FROM promo_usage where mobile='%s' and promocode='%s'"%(mobile, promoCode.upper())

		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails
		# except Exception,e:
		# 	print str(e)

	def getUserreport(self):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id,name,email,mobile,status FROM customer_login"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def GetMomId(self,mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT momId FROM customer_login where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getVendorLoginStatus(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT firstName,middleName,lastName From vendor_login where mobile='%s'"%str(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetMomFavouriteUserLst(self,mobile):
	# try:s
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcm ="Select momId from MOM.customer_login where mobile='%s'"%(mobile)
		cursor.execute(sqlcm)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)

		conn.commit()
		conn.close()
		if len(dbDetails)!=0:
			return dbDetails[0][0]
		else:
			return ""


	def GetMomFavouriteUser(self,mobile, Lat, Lang):
	# try:s
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcm ="Select momId from MOM.customer_login where mobile='%s'"%(mobile)
		print sqlcm
		cursor.execute(sqlcm)
		dbDetails = cursor.fetchall()
		if dbDetails[0][0] is not None:

			newid_ = "("+dbDetails[0][0]+")"

			# sqlcmd = "SELECT * FROM vendor_login where vendor_login.id in %s"%(newid_)

			sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,vendor_login.image_name,latitude,longitude,vendor_login.image,about_mom, onlineStatus, (6371 * acos(cos( radians(latitude) )    * cos( radians( '%s' ) )    * cos( radians( '%s' ) - radians(longitude) )    + sin( radians(latitude) )   * sin( radians( '%s' ) )) ) as distance FROM vendor_login where vendor_login.status=1  HAVING distance < 5 and vendor_login.id in %s"%(str(Lat),str(Lang),str(Lat),newid_)
			#sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,vendor_login.image_name,latitude,longitude,vendor_login.image,about_mom, onlineStatus, (((acos(sin((%s*pi()/180)) * sin((latitude*pi()/180))+cos((%s*pi()/180)) * cos((latitude*pi()/180)) * cos(((%s- longitude)*pi()/180))))*180/pi())*60*1.1515) as distance FROM vendor_login  HAVING distance < 5 and vendor_login.id in %s"%(str(Lat),str(Lat),str(Lang),newid_)

    # SELECT (6371 * acos(
    #    cos( radians(vendor_login.latitude) )
    #    * cos( radians( lat1 ) )
    #    * cos( radians( lng1 ) - radians(vendor_login.longitude) )
    #    + sin( radians(vendor_login.latitude) )
    #    * sin( radians( lat1 ) )
    #) ) as distance from your_table

			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetail=[]
			for row in cursor.fetchall():
				dbDetail.append(row)
			conn.commit()
			conn.close()
			print dbDetail
			return dbDetail
		else:
			dbData =[]
			return dbData
	# except Exception,e:
	# 	print str(e)


	def GetMomnameId(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id FROM vendor_login where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetDeliveryName(self,mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT name FROM delivery_registration where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetPartnerName(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT firstName,middleName,lastName,status, id FROM vendor_login where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTokenCustomer(self,to):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT fcmToken FROM Momtoken where userType='Vendor' and mobile='%s'"%(to)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def applyoffer(self,promocode):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM offer_list where promocode='%s'"%(str(promocode))
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)



	def OrderList(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName, vendor_login.image_name, note FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mom_mobile= vendor_login.mobile where orderInfo.mobile='%s' and orderInfo.status=0 order by orderInfo.id desc"%(mobile)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def OrderListDateWise(self,mobile, state_date, end_date):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName,vendor_login.image_name, note FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mom_mobile= vendor_login.mobile where orderInfo.mobile='%s' and orderInfo.status=0 and createdAt between '%s' and '%s' order by orderInfo.id desc"%(mobile, state_date, end_date)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)



	def VendorList(self,Lat,Lang):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id,firstName,lastName,middleName,email,mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,image_name,latitude,longitude,image,(((acos(sin((%s*pi()/180)) * sin((latitude*pi()/180))+cos((%s*pi()/180)) * cos((latitude*pi()/180)) * cos(((%s- longitude)*pi()/180))))*180/pi())*60*1.1515) as distance FROM vendor_login  HAVING distance < 5"%(str(Lat),str(Lat),str(Lang))
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def VendorMenuList(self, mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM vendor_menu where mobile = '%s' and status=1"%(str(mobile))
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getUserreport(self):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id,name,email,mobile,status FROM customer_login"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getPromocode(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT promocode FROM MOM_vendor.offer_list where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def VendorDataList(self,Lat,Lang):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			# sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,image_name,latitude,longitude,itemName(((acos(sin((%s*pi()/180)) * sin((latitude*pi()/180))+cos((%s*pi()/180)) * cos((latitude*pi()/180)) * cos(((%s- longitude)*pi()/180))))*180/pi())*60*1.1515) as distance FROM vendor_login  LEFT JOIN vendor_menu ON vendor_login.mobile=vendor_menu.mobile  HAVING distance < 5"%(str(Lat),str(Lat),str(Lang))
			# print sqlcmd
			# cursor.execute(sqlcmd)
			sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,vendor_login.image_name,latitude,longitude,vendor_login.image,about_mom, onlineStatus, (((acos(sin((%s*pi()/180)) * sin((latitude*pi()/180))+cos((%s*pi()/180)) * cos((latitude*pi()/180)) * cos(((%s- longitude)*pi()/180))))*180/pi())*60*1.1515) as distance FROM vendor_login where vendor_login.status=1 HAVING distance < 5"%(str(Lat),str(Lat),str(Lang))
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def VendorDataListWithMenu(self,Lat,Lang, id):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			offsets=int(id)*4
			#sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,vendor_login.image_name,latitude,longitude,vendor_login.image,about_mom, onlineStatus, (6371 * acos(cos( radians(latitude) )    * cos( radians( '%s' ) )    * cos( radians( '%s' ) - radians(longitude) )    + sin( radians(latitude) )   * sin( radians( '%s' ) )) ) as distance FROM vendor_login where vendor_login.status=1  HAVING distance < 5 and vendor_login.id in %s"%(str(Lat),str(Lang),str(Lat),newid_)

			sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,vendor_login.image_name,latitude,longitude,vendor_login.image,about_mom, onlineStatus, (6371 * acos(cos( radians(latitude) )    * cos( radians( '%s' ) )    * cos( radians( '%s' ) - radians(longitude) )    + sin( radians(latitude) )   * sin( radians( '%s' ) )) ) as distance FROM vendor_login where vendor_login.status=1 HAVING distance < 5 limit 4 OFFSET %s"%(str(Lat),str(Lang),str(Lat), offsets)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			print dbDetails
			return dbDetails
		except Exception,e:
			print str(e)

	def VendorDataListWithMenuUpdated(self,Lat,Lang, id):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			offsets=int(id)*4
			sqlcm = "Select distinct(mobile), (((acos(sin((%s*pi()/180)) * sin((latitude*pi()/180))+cos((%s*pi()/180)) * cos((latitude*pi()/180)) * cos(((%s- longitude)*pi()/180))))*180/pi())*60*1.1515) as distance from MOM_vendor.vendor_login where  status=1 having distance< 5 limit 4 offset %s"%(str(Lat),str(Lat),str(Lang), offsets)
			print sqlcm
			cursor.execute(sqlcm)
			mobile=""
			print cursor.fetchall(), len(cursor.fetchall())
			if len(cursor.fetchall())!=0 :
				for row in cursor.fetchall():
					mobile=mobile+ ", "+ row[0]
				mobile_lst = "("+ mobile.strip().strip(',').strip() + ")"
				sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,vendor_login.image_name,latitude,longitude,vendor_login.image,about_mom, onlineStatus,  food_type, itemName FROM vendor_login inner join vendor_menu on vendor_menu.mobile = vendor_login.mobile where vendor_menu.status=1 and vendor_login.mobile in %s"%(mobile_lst)
				print sqlcmd
				cursor.execute(sqlcmd)
				dbDetails=[]
				for row in cursor.fetchall():
					dbDetails.append(row)
				conn.commit()
				conn.close()
				return dbDetails
			else:
				dbDetails=[]
				conn.commit()
				conn.close()
				return dbDetails

		except Exception,e:
			print str(e)

	def getUserLoginStatus(self,mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT name,mobile,email,address,latitude,longitude,addressStatus,profile_image From customer_login where mobile='%s'"%str(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def VendorDataListSearchLst(self,Lat,Lang):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,vendor_login.image_name,latitude,longitude,vendor_login.image,about_mom, onlineStatus, (((acos(sin((%s*pi()/180)) * sin((latitude*pi()/180))+cos((%s*pi()/180)) * cos((latitude*pi()/180)) * cos(((%s- longitude)*pi()/180))))*180/pi())*60*1.1515) as distance, food_type, itemName, itemDescription, itemGroup, fullPrice, item_image, itemPreparationTime FROM vendor_login left join vendor_menu on vendor_login.mobile= vendor_menu.mobile where vendor_login.status=1 HAVING distance < 5 limit 15"%(str(Lat),str(Lat),str(Lang))
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def VendorDataListSearchLstSearch(self,Lat,Lang, keyword):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT vendor_login.id,firstName,lastName,middleName,email,vendor_login.mobile,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,profileStatus,vendor_login.image_name,latitude,longitude,vendor_login.image,about_mom, onlineStatus, (((acos(sin((%s*pi()/180)) * sin((latitude*pi()/180))+cos((%s*pi()/180)) * cos((latitude*pi()/180)) * cos(((%s- longitude)*pi()/180))))*180/pi())*60*1.1515) as distance, food_type, itemName, itemDescription, itemGroup, fullPrice, item_image, itemPreparationTime FROM vendor_login left join vendor_menu on vendor_login.mobile= vendor_menu.mobile where (firstName like '%%%s%%' or lastName like '%%%s%%' or itemName like '%%%s%%') and vendor_login.status=1 HAVING distance < 5 limit 5"%(str(Lat),str(Lat),str(Lang), str(keyword), str(keyword), str(keyword))
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	# def OrderList(self,mobile):
	# 	try:
	# 		dbname='MOM_vendor'
	# 		conn = connect_to_cloudsql(dbname)
	# 		cursor = conn.cursor()
	# 		sqlcmd = "SELECT * From orderInfo where mobile='%s' and status=0"%str(mobile)
	# 		cursor.execute(sqlcmd)
	# 		dbDetails=[]
	# 		for row in cursor.fetchall():
	# 			dbDetails.append(row)
	# 		conn.commit()
	# 		conn.close()
	# 		return dbDetails
	# 	except Exception,e:
	# 		print str(e)

	# def OrderList(self,mobile):
	# 	try:
	# 		dbname='MOM_vendor'
	# 		conn = connect_to_cloudsql(dbname)
	# 		cursor = conn.cursor()
	# 		sqlcmd = "SELECT * From orderInfo where mobile='%s' and status=0"%str(mobile)
	# 		cursor.execute(sqlcmd)
	# 		dbDetails=[]
	# 		for row in cursor.fetchall():
	# 			dbDetails.append(row)
	# 		conn.commit()
	# 		conn.close()
	# 		return dbDetails
	# 	except Exception,e:
	# 		print str(e)


	def getDeliveryLogin(self,mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT name,mobile,address,driveringLicense,aadharNo,vehicleNo,companyName,companyId From delivery_registration where mobile='%s'"%str(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def orderItemInfo(self, orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From orderItemInfo where orderId='%s'"%str(orderId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def OrderList2(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From orderInfo where mobile='%s' and status=1 order by id desc"%str(mobile)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def ComOrderList(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM completeOrderInfo where mobile='%s' order by id desc"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def ComOrderListDateWsie(self,mobile, start_date, end_date):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			_sqlcmd_ ="SELECT completeOrderInfo.id, orderId, completeOrderInfo.name, completeOrderInfo.mobile, location, completeOrderInfo.latitude, completeOrderInfo.longitude, mom_mobile, totalPrice, orderStatus,delivery_number, createdAt, customerRating,  ratingStatus,  note,  firstName,middleName,lastName, vendor_login.status, image_name,  delivery_registration.name FROM completeOrderInfo left join vendor_login on completeOrderInfo.mom_mobile = vendor_login.mobile left join MOM.delivery_registration on completeOrderInfo.delivery_number= delivery_registration.mobile where completeOrderInfo.mobile='%s' and createdAt >= '%s' and createdAt <= '%s' order by id desc"%(mobile, start_date, end_date)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def ComCancelOrderList(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM completeOrderInfo where mobile='%s' and status=4 order by id desc"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getOrderStatus(self,orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT orderStatus FROM MOM_vendor.orderInfo where orderId='%s'"%(orderId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def ComOrderList(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM completeOrderInfo where mobile='%s' order by id"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)



	def DeliveryList(self):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From delivery_registration"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def RunOrderList(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName,vendor_login.image_name, note, orderStatus, delivery_number FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mom_mobile= vendor_login.mobile where orderInfo.mobile='%s' and orderInfo.status=1 order by orderInfo.id desc"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def RunorderInfo(self,orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT food_item,quantity,itemId,pType,itemActualPrice,orderId,image FROM MOM_vendor.orderItemInfo  where orderId='%s'"%(orderId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)




	def CompOrderList(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From completeOrderInfo where mobile='%s' order by id desc"%str(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getCheckReferal(self,referal_code):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from master_referral where referralCode='%s' " %(str(referal_code))
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			if len(dbDetails)>0:
				return True
			else:
				return False
		except Exception,e:
			print str(e)

	def GetCustomerAdd(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM orderInfo where mobile='%s' order by desc" %(mobile)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			if len(dbDetails)>0:
				return True
			else:
				return False
		except Exception,e:
			print str(e)

	def getCustomerLogin(self, mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM customer_login where mobile = '%s'"%(str(mobile))
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetCustomerAddress(self, mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM orderInfo where mobile = '%s' ORDER BY id DESC LIMIT 1;"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def orderInfo2(self,orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT food_item,quantity,itemId,pType,itemActualPrice,orderId,image FROM MOM_vendor.orderItemInfo  where orderId='%s'"%(orderId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getLastIDNew(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM orderInfo;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
	def getLastIDNewOrderInfo(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM orderId;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetCustomerAddress2(self, mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM customer_address where mobile = '%s' ORDER BY id DESC LIMIT 1;"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def GetCustomerAddress3(self, mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM customer_address where mobile = '%s'"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def offerList(self):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM offer_zone where status=1"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)





	def getUserStatus(self,mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from customer_login where mobile=%s" %(mobile)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return True
			else:
				return False
		except Exception,e:
			print str(e)






class UpdateData():

	##################################### END #################################################




	def UpdateDeActiveUser(self,mobile):
		# try:
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE customer_login SET status=0 where mobile='%s'"%(mobile)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateActiveUser(self,mobile):
		# try:
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE customer_login SET status=1 where mobile='%s'"%(mobile)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def updateUserProfile(self,mobile,name,email,profileImage):
		# try:
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE customer_login SET name='%s',email='%s',profile_image='%s' where mobile='%s'"%(name,email,profileImage,mobile)

		print sqlcmd

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def updateAddress(self,Id,mobile,address,latitude,longitude,phone_number,name):
		# try:
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE customer_address SET mobile='%s',address='%s',latitude='%s',longitude='%s',phone_number='%s',name='%s' where id='%s'"%(mobile,address,latitude,longitude,phone_number,name,Id)
		cursor.execute(sqlcmd)
		_sqlcmd="UPDATE customer_login SET addressStatus=1 where mobile='%s'"%(mobile)
		cursor.execute(_sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def updateFavMom(self,mobile,newMomId):
		# try:
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlcmd="UPDATE customer_login SET momId='%s' where mobile='%s'"%(newMomId, mobile)
		cursor.execute(_sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateCancelOrder(self,orderId):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE completeOrderInfo SET orderstatus=4, status=5 where orderId='%s' "%(orderId)
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid







class DeleteData():



	def deleteToken(self,mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM customer_token WHERE mobile="%s"'%(mobile)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteAddress(self,Id):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM customer_address WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def deleteorder(self,orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM orderInfo WHERE orderId="%s"'%(orderId)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)
