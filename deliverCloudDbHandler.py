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






	def addVendorWeb(self,mobile,firstName,middleName,lastName,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd):
	# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO vendor_login (mobile,firstName,middleName,lastName,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,firstName,middleName,lastName,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd)
		print _sqlc_
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
	# except Exception,e:
	# 	print str(e)

	def addLiveLocationEmp(self, mobile, lastUpdate, lat, longitude, formatted_address):
		# try:
		dbname = "MOM_vendor"
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO `liveLocation` (`mobile`,`lastUpdate`,`lat`,`lang`,`address`) VALUES ('%s','%s',%s,%s,'%s')"%(mobile, lastUpdate, lat, longitude, formatted_address)
		print _sqlc_
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid

	def addPartnerToken(self, mobile,fcmToken):
		try:
			dbname = 'delivery'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO `partnerToken` (`mobile`,`fcmToken`) VALUES ( '%s', '%s')"%(mobile,fcmToken)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addDeliveryToken(self, mobile,fcmToken):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO `Momtoken` (`mobile`,`fcmToken`,`userType`) VALUES ( '%s', '%s', '%s') ON DUPLICATE KEY update fcmToken='%s'"%(mobile,fcmToken, 'Delivery', fcmToken)
		print _sqlc_
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)



	def addOnline(self,mobile,timeStamp,status):
		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO delivery_registration (mobile,timeStamp,status) VALUES ('%s', '%s','%s')"%(mobile,timeStamp,status)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addOnlineStatus(self,mobile,timeStamp,status):
		try:
			dbname = 'MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO onlineStatus (mobile,timeStamp,status) VALUES ('%s', '%s','%s')"%(mobile,timeStamp,status)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)




		#######################################################################################################

class GetData():

	def ComOrder_List(self,orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT food_item,quantity,itemId,pType,itemActualPrice,orderId,image FROM MOM_vendor.complete_order  where orderId='%s'"%(orderId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def MomProfile(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT image_name FROM vendor_login where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def ComOrderListDelivery(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM completeOrderInfo where delivery_number='%s' order by id desc"%(mobile)
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

	def getCheckLocation(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)

			cursor = conn.cursor()
			sqlcmd = "select * from liveLocation where mobile='%s' " %(str(mobile))
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



	def Momlatitude(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT latitude,longitude FROM MOM_vendor.vendor_login  where mobile='%s'"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def OrderList(self,mobile):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName,vendor_login.image_name, note, vendor_login.firstName, vendor_login.latitude, vendor_login.longitude, vendor_login.vendor_code, vendor_login.address FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mom_mobile= vendor_login.mobile where orderInfo.delivery_number='%s' order by orderInfo.id desc"%(mobile)

		print _sqlcmd_
		cursor.execute(_sqlcmd_)
		dbDetails=[]
		dbDetails = cursor.fetchall()
		conn.commit()
		conn.close()
		return dbDetails
		# except Exception,e:
		# 	print str(e)


	def getOnlineStatus(self,mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)

			cursor = conn.cursor()
			sqlcmd = "select status from delivery_registration where mobile='%s'" %(str(mobile))
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

















class UpdateData():

	##################################### END #################################################
	def updateLiveLocation(self,mobile,lastUpdate,lat,longitude,formatted_address):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE liveLocation SET lastUpdate='%s',lat='%s',lang='%s',address='%s',updateTime='%s' where mobile='%s'"%(str(lastUpdate),str(lat),str(longitude),str(formatted_address),str(lastUpdate),str(mobile))
			cursor.execute(sqlcmd)
			testid = cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
			print str(e)


	def updateOnlineStatus(self,mobile,timeStamp,status):
		# try:
		dbname='MOM'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE delivery_registration SET timeStamp='%s',status='%s' where mobile='%s'"%(str(timeStamp),str(status),str(mobile))
		print sqlcmd
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)








class DeleteData():



	def deletePartnerToken(self,mobile):
		try:
			dbname='delivery'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM partnerToken WHERE mobile="%s"'%(str(mobile))
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)
