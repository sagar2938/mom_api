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

class GetData():

	def getUnassignedOrder(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM orderInfo where deliver_number is NULL"%(vendor_no)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)



	def getVendorOnlineStatus(self, vendor_no):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT onlineStatus FROM vendor_login where mobile='%s'"%(vendor_no)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getUserSelection(self):
		try:
			dbname='youthmobi'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT name,email,mobile,company1,company2,company3,company4,response1,response2,response3,response4 FROM youthmobi.user_basic where response1!='';"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
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

	def OrderListWebDash(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName,vendor_login.image_name, note, orderStatus FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mom_mobile= vendor_login.mobile order by orderInfo.id desc"
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
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
			sqlcmd = "SELECT * From orderItemInfo where orderId='%s' "%str(orderId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getCompleteOrderInfo(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From completeOrderInfo "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def MomProfile(self,mobile):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd = "SELECT image_name, firstName, lastName FROM vendor_login where mobile='%s'"%(mobile)
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails
		# except Exception,e:
		# 	print str(e)


class UpdateData():

	##################################### END #################################################

	def updateDeliveryBoy(self, mobile, name, address, driveringLicense, aadharNo, vehicleNo, companyName, image):
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE delivery_registration SET name='%s', address='%s', driveringLicense='%s', aadharNo='%s', vehicleNo='%s', companyName='%s', image='%s'  where mobile='%s'"%( name, address, driveringLicense, aadharNo, vehicleNo, companyName, image, mobile)
		print sqlcmd

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def updateFoodOnlineStatus(self, item_id, food_status):
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE vendor_menu SET status=%s where id='%s'"%(food_status, item_id)
		print sqlcmd

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updatezoneoffer(self,Id):
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE offer_list SET status=1 where id='%s'"%(Id)
		print sqlcmd

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updatezoneoffernew(self,Id):
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE offer_list SET status=0 where id='%s'"%(Id)
		print sqlcmd

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid


	def updateOnlineStatus(self,mobile, status):
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE vendor_login SET onlineStatus=%s where mobile='%s'"%(status, mobile)
		print sqlcmd

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdatePassbook(self,mobile,account_holder,account_number,ifsc,bankName,pancard,check,passbook):
		# try:
		dbname='youthmobi'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE user_basic SET account_holder='%s',account_number='%s',ifsc='%s',bankName='%s',pancard='%s',checkdata='%s', passbook='%s' where mobile='%s'"%(account_holder,account_number,ifsc,bankName,pancard,check,passbook,mobile)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateActiveVendor(self,mobile):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE vendor_login SET status=1 where mobile='%s'"%(mobile)
		print sqlcmd

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateDeActiveVendor(self,mobile):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE vendor_login SET status=0 where mobile='%s'"%(mobile)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid


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

	def UpdateActiveoffer(self,Id):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE offer_list SET status=1 where id='%s'"%(Id)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateDeActiveoffer(self,Id):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE offer_list SET status=0 where id='%s'"%(Id)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateCustomerRate(self,orderId,rating,deliver_rating):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE completeOrderInfo SET customerRating='%s',deliveryRating='%s',ratingStatus=1 where orderId='%s'"%(rating,deliver_rating,orderId)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid


	def UpdateCustomer2Rate(self,orderId,rating,deliver_rating):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE completeOrderInfo SET ratingStatus=2 where orderId='%s'"%(orderId)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateSpecial(self,mobile,menuItem,date):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE vendor_login SET menuItem='%s',date='%s' where mobile='%s'"%(menuItem,date,mobile)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateVendorProfile(self,mobile,firstName,middleName,lastName,email,image_name,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,latitude,longitude,image,trackingStatus, about_mom):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE vendor_login SET firstName='%s',middleName='%s',lastName='%s',email='%s',image_name='%s',address='%s',country='%s',state='%s',profileStatus=1,zipCode='%s',foodLicenseNo='%s',dob='%s',specialization='%s',comment='%s',openTime='%s',endTime='%s',breakStart='%s',breakEnd='%s',latitude='%s',longitude='%s',image='%s',trackingStatus='%s', about_mom='%s' where mobile='%s'"%(firstName,middleName,lastName,email,image_name,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,latitude,longitude,image,trackingStatus,about_mom, mobile )
		print sqlcmd
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

	def UpdateDeliveryBoy(self,orderId):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE orderInfo SET orderstatus='1', status=1 where orderId='%s'"%(orderId)

		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateVendorMenu(self,Id,mobile,food_type,itemName,itemDescription,itemGroup,half,quarter,full,halfPrice,quarterPrice,fullPrice,item_image,itemPreparationTime):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE vendor_menu SET mobile='%s',food_type='%s',itemName='%s',itemDescription='%s',itemGroup='%s',half='%s',quarter='%s',full='%s',halfPrice='%s',quarterPrice='%s',fullPrice='%s',item_image='%s',itemPreparationTime='%s' where id='%s'"%(mobile,food_type,itemName,itemDescription,itemGroup,half,quarter,full,halfPrice,quarterPrice,fullPrice,item_image,itemPreparationTime,Id)
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateCancelOrder(self,orderId):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE completeOrderInfo SET orderstatus=4 where orderId='%s'"%(orderId)
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# try:
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE offer_zone set status=1 where id='%s'"%(Id)
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateDeliveryAssigned(self,orderId,delivery_mobile,delivery_latitute,delivery_longitude):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE orderInfo SET orderStatus=2,delivery_number='%s',delivery_latitute='%s',delivery_longitude='%s', status=1 where orderId='%s'"%(delivery_mobile,delivery_latitute,delivery_longitude,orderId)
		print sqlcmd
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateDelivery2(self,orderId,delivery_mobile,delivery_latitute,delivery_longitude):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE orderInfo SET orderStatus=6,delivery_number='%s',delivery_latitute='%s',delivery_longitude='%s' where orderId='%s'"%(delivery_mobile,delivery_latitute,delivery_longitude,orderId)
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateDelivery(self,orderId,delivery_mobile,delivery_latitute,delivery_longitude):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE orderInfo SET orderStatus=1,delivery_number='%s',delivery_latitute='%s',delivery_longitude='%s' where orderId='%s'"%(delivery_mobile,delivery_latitute,delivery_longitude,orderId)
		print sqlcmd
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
	def updateDeliveryBoyAssign(self, orderId, delivery_mobile):
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE orderInfo SET orderStatus=2, delivery_number='%s' where orderId='%s'"%(delivery_mobile, orderId)
		print sqlcmd
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid








class DeleteData():

	def DeleteVendor(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM vendor_login WHERE mobile="%s"'%(mobile)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def Deleteoffer(self,Id):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM offer_list WHERE id="%s"'%(Id)
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

	def DeleteUser(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM customer_login WHERE mobile="%s"'%(mobile)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteVendorMenu(self,Id):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM vendor_menu WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteRunorder(self,orderId):
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
