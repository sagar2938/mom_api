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

	def addContactUs(self, name,phone_no,email, pincode, note):
		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO contact_us (name,phone_no,email, pincode, note) VALUES ('%s','%s','%s', '%s', '%s')"%(name,phone_no,email, pincode, note)
			cursor.execute(_sqlc_)

			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)




	def addUser(self,name,email,mobile):
		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO customer_login (name,email,mobile) VALUES ('%s','%s','%s')"%(name,email,mobile)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addFoodOnlineStatus(self,offer_name,offer_type,discount,maxdiscount,valid_to,pvalues,image,promocode,mobile,Status,chefPart,momPart,minVal,maxVal, minCartVal):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO offer_list (offer_name,offer_type,discount,maxdiscount,usage_limit,pvalues,image,promocode,mobile,Status,chefPart,momPart,minVal,maxVal, minCartVal) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s')"%(offer_name,offer_type,discount,maxdiscount,valid_to,pvalues,image,promocode,mobile,Status,chefPart,momPart,minVal,maxVal, minCartVal)
		print _sqlc_
		cursor.execute(_sqlc_)
		# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
		# cursor.execute(_sqlc)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)






	def addQuery(self,name,email,phone,pincode,message):
		try:
			dbname = 'MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO lead (name,email,phone,pincode,message) VALUES ('%s','%s','%s','%s','%s')"%(name,email,phone,pincode,message)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addVendorMenu(self,mobile,food_type,itemName,itemDescription,itemGroup,half,quarter,full,halfPrice,quarterPrice,fullPrice,item_image,itemPreparationTime):
		try:
			dbname = 'MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO vendor_menu (mobile,food_type,itemName,itemDescription,itemGroup,half,quarter,full,halfPrice,quarterPrice,fullPrice,item_image,itemPreparationTime) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,food_type,itemName,itemDescription,itemGroup,half,quarter,full,halfPrice,quarterPrice,fullPrice,item_image,itemPreparationTime)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addUser2(self,firstName,middleName,lastName,email,mobile,image_name,vendor_code,about_mom):
		try:
			dbname = 'MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO vendor_login (firstName,middleName,lastName,email,mobile,image_name,vendor_code,about_mom) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(firstName,middleName,lastName,email,mobile,image_name,vendor_code,about_mom)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addVendorOffer(self,mobile,offerName,offerType,discount,maxdiscount,valid_to,image,promocode,description):
		try:
			dbname = 'MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO offer_list (mobile,offer_name,offer_type,discount,maxdiscount,usage_limit,image,promocode,pvalues) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,offerName,offerType,discount,maxdiscount,valid_to,image,promocode,description)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def AddReferralMaster(self, referal_code):
		try:
			dbname = 'MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO master_referral (referralCode) VALUES ('%s')"%(referal_code)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)


	def addToken(self,mobile,fcmToken,userType):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO `Momtoken` (`mobile`,`fcmToken`,`userType`) VALUES ( '%s', '%s', '%s') ON DUPLICATE KEY update fcmToken='%s'"%(mobile,fcmToken, userType, fcmToken)
		print _sqlc_
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)
	def updateToken(self, mobile, fcmToken, userType):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "UPDATE Momtoken SET fcmToken=%s (`mobile`,`fcmToken`,`userType`) VALUES ( '%s', '%s', '%s') ON DUPLICATE KEY update fcmToken='%s'" % (
		mobile, fcmToken, userType, fcmToken)
		print _sqlc_
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid

	# except Exception,e:
	# 	print str(e)



	def addRunningBooking(self, orderId):
		try:
			dbname = 'MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO runningOrderInfo  (SELECT * FROM orderInfo where orderId='%s')"%(str(orderId))
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addCompleteBooking(self, orderId):
		# try:
		dbname = 'MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO completeOrderInfo  (SELECT * FROM orderInfo where orderId='%s')"%(str(orderId))
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid
		# except Exception,e:
		# 	print str(e)

	def addCancelBooking(self, orderId):
		try:
			dbname = 'MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO completeOrderInfo  (SELECT * FROM orderInfo where orderId='%s')"%(str(orderId))
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)




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




		#######################################################################################################

class GetData():
	def getProfilePics(self, mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT profile_image FROM customer_login where mobile='%s'"%(mobile)
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
	def getOrderInfoData(self,orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM orderInfo where orderId='%s'"%(orderId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				data_dict={}
				data_dict['orderId']=row[1]
				data_dict['name']=row[2]
				data_dict['mobile']=row[3]
				data_dict['totalPrice']=row[8]
				data_dict['location']=row[4]
				data_dict['note']=row[17]
				data_dict['promocode']=row[18]
				# data_dict['mobile']=row[3]
				dbDetails.append(data_dict)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getContacUsT(self):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM contact_us"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


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

	def getLead(self):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM leads"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getToken(self,senderType,to):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT fcmToken FROM Momtoken where userType='%s' and mobile='%s'"%(senderType,to)
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

	def getLastID(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM vendor_login;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
	def getCompleteOrderInfoMom(self, mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From completeOrderInfo  where mom_mobile='%s' order by id desc"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getVendorProfile(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM vendor_login where mobile='%s'"%(mobile)
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

	def GetOffer(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM offer_list where status=1"
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

	def getUserLoginStatus(self,mobile):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT name,mobile From customer_login where mobile='%s'"%str(mobile)
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
			sqlcmd = "SELECT firstName,middleName,lastName,mobile,profileStatus,email,image_name,status From vendor_login where mobile='%s'"%str(mobile)
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

	def PostAdmintLoginData(self, username):
		try:
			dbname='MOM'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT id, password, username, name, status FROM admin_login where (username = '%s')"%(username)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getVendorData(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM vendor_login"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
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

	def getVendorLogin(self, mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM vendor_login where mobile = '%s'"%(str(mobile))
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
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
			_sqlcmd_ ="SELECT * FROM vendor_menu where mobile = '%s'"%(str(mobile))
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def VendorMenuListCustomer(self, mobile):
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

	def VendorMenuList2(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM vendor_menu"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
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
			_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName,vendor_login.image_name, note, orderStatus,  delivery_number FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mom_mobile= vendor_login.mobile where orderInfo.mom_mobile='%s' and orderInfo.status=0 order by orderInfo.id desc"%(mobile)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def OrderListWeb(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName,vendor_login.image_name, note,  orderStatus, delivery_number FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mom_mobile= vendor_login.mobile where orderStatus<2  order by orderInfo.id desc"
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
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
			_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName,vendor_login.image_name, note, orderStatus, delivery_number FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mom_mobile= vendor_login.mobile where orderInfo.mom_mobile='%s' and orderInfo.status=1 order by orderInfo.id desc"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def AssignOderList(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT orderInfo.id, orderInfo.orderId, name,  orderInfo.mobile, location,  orderInfo.latitude, orderInfo.longitude, mom_mobile,totalPrice, createdAt,firstName,middleName,lastName,vendor_login.image_name, note,  orderStatus, delivery_number FROM MOM_vendor.orderInfo LEFT JOIN vendor_login ON orderInfo.mobile= vendor_login.mobile where orderInfo.status=1 order by orderInfo.id desc"
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
			_sqlcmd_ ="SELECT * FROM completeOrderInfo where mom_mobile='%s'"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def ComOrderweb(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM completeOrderInfo"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)







	def getdeliverNumber(self,orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT distinct(delivery_number),orderStatus FROM MOM_vendor.orderInfo  where orderId='%s'"%(orderId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)

			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getdeliverLocation(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT lat,lang FROM MOM_vendor.liveLocation  where mobile='%s'"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getFoodLicenseStatus(self, vendor_no):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlcmd_ ="SELECT foodLicenseNo FROM MOM_vendor.vendor_login  where mobile = '%s'"%(vendor_no)
		cursor.execute(_sqlcmd_)
		dbDetails=[]
		dbDetails = cursor.fetchall()
		conn.commit()
		conn.close()
		return dbDetails
		# except Exception,e:
		# 	print str(e)
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

	def ComOrder_List(self,orderId):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT food_item,quantity,itemId,pType,itemActualPrice,orderId FROM MOM_vendor.orderItemInfo  where orderId='%s'"%(orderId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getCustomerLastID(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM master_referral;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def MomLocation(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT latitude,longitude FROM vendor_login where mobile='%s'"%(mobile)
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


	def PartnerLocation(self,Lat,Lan):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd = "SELECT mobile,lat,lang,(((acos(sin((%s*pi()/180)) * sin((lat*pi()/180))+cos((%s*pi()/180)) * cos((lat*pi()/180)) * cos(((%s- lang)*pi()/180))))*180/pi())*60*1.1515) as distance FROM liveLocation where liveLocation.mobile in (SELECT mobile FROM MOM.delivery_registration where status='True') HAVING distance < 5"%(str(Lat),str(Lat),str(Lan))
		print sqlcmd
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails
		# except Exception,e:
		# 	print str(e)

	def DeliveryLocation(self,mobile):
		# try:
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd = "SELECT mobile,lat,lang FROM liveLocation where mobile='%s'"%(mobile)
		print sqlcmd
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails
		# except Exception,e:
		# 	print str(e)

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

	def getUserStatus2(self,mobile):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from vendor_login where mobile=%s" %(mobile)
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

	def getoffernew(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * from offer_list where status=1"
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getoffernewDashboard(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * from offer_list"
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getorderprice(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * from order_price_info"
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getOrderListData(self):
		try:
			dbname='MOM_vendor'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT distinct(orderId), latitude, longitude  FROM MOM_vendor.orderInfo where delivery_number is Null and orderStatus!=-1 and status=1;"
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)






















class UpdateData():

	##################################### END #################################################
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
		sqlcmd="UPDATE orderInfo SET orderStatus='1', status=1 where orderId='%s'"%(orderId)

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
		sqlcmd="UPDATE completeOrderInfo SET orderStatus=4, ratingStatus=2 where orderId='%s'"%(orderId)


		cursor.execute(sqlcmd)

		sql_cm = "UPDATE order_price_info SET status='Cancelled' where orderId='%s'"%(orderId)
		cursor.execute(sql_cm)
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
		sqlcmd="UPDATE orderInfo SET orderStatus=2, delivery_number='%s',delivery_latitute='%s',delivery_longitude='%s', status=1 where orderId='%s'"%(delivery_mobile,delivery_latitute,delivery_longitude,orderId)
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
		sqlcmd="UPDATE orderInfo SET orderStatus=6, delivery_number='%s',delivery_latitute='%s',delivery_longitude='%s' where orderId='%s'"%(delivery_mobile,delivery_latitute,delivery_longitude,orderId)
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
		sqlcmd="UPDATE orderInfo SET orderStatus=2,delivery_number='%s',delivery_latitute='%s',delivery_longitude='%s' where orderId='%s'"%(delivery_mobile,delivery_latitute,delivery_longitude,orderId)
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

	def updateOrderStatusInfo(self, orderId):
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE orderInfo SET orderStatus=0, status=0 where orderId='%s'"%(orderId)
		print sqlcmd
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def updateOrderStatusInfoNeg(self, orderId):
		dbname='MOM_vendor'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE orderInfo SET orderStatus=-2, status=-2 where orderId='%s'"%(orderId)
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
