# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json, urllib2, logging
import cloudDbHandler as dbhelper
import datetime
import json
import StringIO
import mailhandler
import random
from math import radians, cos, sin, asin, sqrt
import math
import ast
from time import gmtime, strftime
import customerCloudDbHandler as dbhelper
from sets import  Set
import unicodedata
import urllib
import urllib2
from datetime import date, timedelta
import googleapiclient.discovery
import googleapiclient.http
from google.appengine.api import urlfetch
from datetime import timedelta, date, datetime
from time import gmtime, strftime,time,localtime
import random

app = Flask(__name__)

############################   Normal Function To calculate the Details   ###################################################

API_KEY = ['NkHb13BxRBiZ0JSyxLbAU','Hx1XU63ZThyFGsqfLeGu7']

def daterange(date1, date2):
	for n in range(int ((date2 - date1).days)+1):
		yield date1 + timedelta(n)

def haversine(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	km = 6367 * c


	return km


@app.after_request
def after_request(response):
	response.headers['Access-Control-Allow-Origin']='*'
	response.headers['Access-Control-Allow-Headers']='Content-Type, Authorization'
	response.headers['Access-Control-Allow-Methods']= 'GET, PUT, POST, DELETE'
	return response


@app.route('/customer/user/login/', methods=['GET','POST'])
def ApiUserLogin():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = user_data['otp']

		User= dbhelper.GetData().getUserLoginStatus(mobile)

		if len(User)>0:

			name = User[0][0]
			mobile=User[0][1]
			email=User[0][2]
			address=User[0][3]
			latitude=User[0][4]
			longitude=User[0][5]
			addressStatus=User[0][6]
			profile_image=User[0][7]
			api_key ='NkHb13BxRBiZ0JSyxLbAU'
			try:
				text ="Your + verification + code + is+ %s "%(str(otp))
				#text = "<#> +MOM: +Your +verification +code +is +%s+ /BPH4AP1pTx"%(str(otp))
				url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
				urlfetch.set_default_fetch_deadline(45)
				resp = urlfetch.fetch(url=url,
					method=urlfetch.GET,
					headers={'Content-Type': 'application/json'})
			except:
				print 'inside'



			db={'message':'User Exist',"confirmation":1,"otp":otp,'api_key':api_key,'mobile':mobile,'email':email,'name':name,'address':address,'latitude':latitude,'longitude':longitude,'addressStatus':addressStatus,'profile_image':profile_image}
		else:
			db={'message': 'User Not Exist', "confirmation":0}

		resp = Response(json.dumps({ "response": db},ensure_ascii=False))
		return after_request(resp)




@app.route('/customer/add/user/',methods=['GET','POST'])
def APiadduser():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		name= userInfo['name']
		email = userInfo['email']
		mobile = userInfo['mobile']
		otp      = userInfo['otp']
		address = userInfo['address']
		latitude      = userInfo['latitude']
		longitude = userInfo['longitude']
		print address,latitude,longitude
		user_status =dbhelper.GetData().getUserStatus(mobile)
		if user_status==True:
			db={'message':'User Already Exist',"confirmation":0}
			resp = Response(json.dumps({"response": db},ensure_ascii=False))
			return after_request(resp)
		else:
			api_key ='NkHb13BxRBiZ0JSyxLbAU'
			AddUser = dbhelper.AddData().addUser(name,email,mobile,address,latitude,longitude)
			db={'message':'User Added',"confirmation":1,"mobile":mobile,"name":name,"email":email,"otp":otp,"api_key":api_key,"address":address,"latitude":latitude,"longitude":longitude}
			resp = Response(json.dumps({"response":db},ensure_ascii=False))
			return after_request(resp)


@app.route('/customer/update/user/address/',methods=['GET','POST'])
def APiaddAddData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		Id = userInfo['id']
		mobile= userInfo['mobile']
		address = userInfo['address']
		latitude = userInfo['latitude']
		longitude = userInfo['longitude']
		phone_number = userInfo['phone_number']
		name= userInfo['name']
		out  =dbhelper.UpdateData().updateAddress(Id,mobile,address,latitude,longitude,phone_number,name)
		db={'message':'Address Updated',"confirmation":1}
		resp = Response(json.dumps({"response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/update/user/profile/',methods=['GET','POST'])
def APiuserProfile():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile= userInfo['mobile']
		name = userInfo['name']
		email = userInfo['email']
		profileImage = userInfo['profileImage']
		out  =dbhelper.UpdateData().updateUserProfile(mobile,name,email,profileImage)
		db={'message':'Profile Updated',"confirmation":1}
		resp = Response(json.dumps({"response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/favourate/mom/',methods=['GET','POST'])
def APiMomFavour():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile= userInfo['mobile']
		momId = userInfo['momId']

		getMom = dbhelper.GetData().GetMomId(mobile)
		momIdstr = getMom[0][0]
		print momIdstr
		if momIdstr is None:
			momIdLst = []
		else:
			momIdLst= momIdstr.split(',')

		print momIdLst

		if momId in momIdLst:
			print momId
			momIdLst.remove(momId)
		else:
			momIdLst.append(momId)
			print momId

		out  =dbhelper.UpdateData().updateFavMom(mobile,','.join(momIdLst).strip(','))


		db={'message':'Favourate MomList Updated',"confirmation":1}
		resp = Response(json.dumps({"response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/get/favourate/mom/', methods=['GET','POST'])
def APiGetMomFavour():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		try:
			mobile    = userInfo['mobile']
			latitude  = userInfo['latitude']
			longitude = userInfo['longitude']
			if mobile !="":
				mom_info_data = dbhelper.GetData().GetMomFavouriteUser(mobile, latitude, longitude)
				mom_info_data_db = []
				for line in mom_info_data:
					vendor_info_data_dict = {}
					vendor_info_data_dict['id']=line[0]
					vendor_info_data_dict['momId']=line[0]
					vendor_info_data_dict['firstName']=line[1]
					vendor_info_data_dict['lastName']=line[2]
					vendor_info_data_dict['middleName']=line[3]
					vendor_info_data_dict['email']=line[4]
					vendor_info_data_dict['mobile']=line[5]
					partner_job = dbhelper.GetData().getPromocode(line[5])
					if (len(partner_job))>0:
						vendor_info_data_dict['promocode']  = partner_job[0][0]
					else:
						vendor_info_data_dict['promocode']  = ''
					vendor_info_data_dict['address']=line[6]
					vendor_info_data_dict['country']=line[7]
					vendor_info_data_dict['state']=line[8]
					vendor_info_data_dict['zipCode']=line[9]
					vendor_info_data_dict['foodLicenseNo']=line[10]
					vendor_info_data_dict['dob']=line[11]
					vendor_info_data_dict['specialization']=line[12]
					vendor_info_data_dict['comment']=line[13]
					vendor_info_data_dict['openTime']=line[14]
					vendor_info_data_dict['endTime']=line[15]
					vendor_info_data_dict['breakStart']=line[16]
					vendor_info_data_dict['breakEnd']=line[17]
					vendor_info_data_dict['profileStatus']=line[18]
					vendor_info_data_dict['image_name']=line[19]
					vendor_info_data_dict['latitude']=line[20]
					vendor_info_data_dict['rating']='4.5'
					vendor_info_data_dict['longitude']=line[21]



					# vendor_info_data_dict['status']=line[22]
					vendor_info_data_dict['image']=line[22]
					vendor_info_data_dict['description']=line[23]

					vendor_info_data_dict['onlineStatus']=line[24]
					mom_info_data_db.append(vendor_info_data_dict)
			else:
				mom_info_data_db = []
		except:
			mom_info_data_db = []
		print mom_info_data_db
		resp = Response(json.dumps({"success": True, "mom_data": mom_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/customer/add/user/address/',methods=['GET','POST'])
def APiaddAddress():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile= userInfo['mobile']
		address = userInfo['address']
		latitude = userInfo['latitude']
		longitude = userInfo['longitude']
		phone_number = userInfo['phone_number']
		name = userInfo['name']
		last =dbhelper.AddData().addAddress(mobile,address,latitude,longitude,phone_number,name)
		if last:
			db={'message':'Address Added',"confirmation":1}
		else:
			db={'message': 'Address not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/add/delivery/data/',methods=['GET','POST'])
def APiaddDelivery():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		name= userInfo['name']
		mobile= userInfo['mobile']

		address = userInfo['address']
		driveringLicense = userInfo['driveringLicense']
		aadharNo = userInfo['aadharNo']
		vehicleNo = userInfo['vehicleNo']
		companyName  = userInfo['companyName']
		companyId = userInfo['companyId']
		last =dbhelper.AddData().addDelivery(name,mobile,address,driveringLicense,aadharNo,vehicleNo,companyName,companyId)
		if last:
			db={'message':'Delivery Added',"confirmation":1}
		else:
			db={'message': 'Delivery not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/get/delivery/info/',methods=['GET','POST'])
def ApiGetDeliver():
	if request.method=='POST':
		delivery_info_data = dbhelper.GetData().DeliveryList()
		delivery_info_data_db = []

		if(len(delivery_info_data))>0:
			for line in delivery_info_data:
				delivery_info_data_dict = {}
				delivery_info_data_dict['id'] =line[0]
				delivery_info_data_dict['name'] =line[1]
				delivery_info_data_dict['mobile'] =line[2]
				delivery_info_data_dict['address']  =line[3]
				delivery_info_data_dict['driveringLicense'] =line[4]
				delivery_info_data_dict['aadharNo'] =line[5]
				delivery_info_data_dict['vehicleNo']  =line[6]
				delivery_info_data_dict['companyName'] =line[7]
				delivery_info_data_dict['companyId'] =line[8]

				delivery_info_data_db.append(delivery_info_data_dict)

		resp = Response(json.dumps({"success": True, "delivery_data": delivery_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/customer/customer/check/auth/', methods=['GET','POST'])
def CheckCustomerAuth():
	if request.method       == 'POST':
		user_data =json.loads(request.data)
		mobile= user_data['mobile']
		otp= user_data['otp']
		referal_code= user_data['referal_code']
		if referal_code[:5]=="MOMC":
			referal_type = "customer"
		elif referal_code == "" :
			referal_type =""
		else:
			referal_type = "Vendor"
		CheckReferal= dbhelper.GetData().getCheckReferal(referal_code)
		if CheckReferal==True or referal_code =="" :
			status= "0"
			AddCustomer= dbhelper.GetData().getCustomerLogin(mobile)
			try:
				if len(AddCustomer)==0:
					db={'message':'User Not Exist',"confirmation":0}
					# text="Your+OTP+is+:+%s+Note+:+Please+ DO+NOT+SHARE+this+OTP+with+anyone."%(str(otp))
					text ="Your + verification + code + is + %s ."%(str(otp))
					#text = "<#> +MOM: +Your +verification +code +is +%s+ /BPH4AP1pTx"%(str(otp))
					print text
					mobile=str(mobile)
					url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)

					urlfetch.set_default_fetch_deadline(45)
					resp = urlfetch.fetch(url=url,
						method=urlfetch.GET,
						headers={'Content-Type': 'text/html'})
					print resp.content
				else:
					db={'message': 'User Already Exist', "confirmation":1}
			except:
				pass
		else:
			db={'message': 'ReferalCode Not Exist', "confirmation":2}

		resp = Response(json.dumps({ "response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/resend/otp/', methods=['GET','POST'])
def AddResendOtp():
	if request.method       == 'POST':
		user_data           =json.loads(request.data)
		mobile              = user_data['mobile']
		otp                = user_data['otp']


		text ='MotherOnMission+ Your+ verification +code +is+ %s'%(str(otp))
		#text = "<#> +MOM: +Your +verification +code +is +%s+ /BPH4AP1pTx"%(str(otp))

		url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)

		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})
		resp = Response(json.dumps({ "response": "success"},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/customer/send/otp/', methods=['GET','POST'])
def CheckCustomerAuthOTP():
	if request.method       == 'POST':
		user_data           =json.loads(request.data)
		mobile              = user_data['mobile']
		otp                = user_data['otp']
		# text="Your+OTP+is+:+%s+Note+:+Please+ DO+NOT+SHARE+this+OTP+with+anyone."%(str(otp))
		text =" Welcome to Mother on Mission. Your Login OTP is %s."%(str(otp))
		#text = "<#> +MOM: +Your +verification +code +is +%s+ /BPH4AP1pTx"%(str(otp))

		mobile=str(mobile)
		url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)

		# url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=idwealth1&pwd=api@idwealth1&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})

		resp = Response(json.dumps({ "msg": "Sent Successfully"},ensure_ascii=False))
		return after_request(resp)


@app.route('/customer/get/offer/',methods=['GET','POST'])
def ApiGetOffer():
	if request.method=='POST':
		offer_info_data = dbhelper.GetData().VendorMenuList(mobile)
		offer_info_data_db = []

		if(len(offer_info_data))>0:
			for line in offer_info_data:
				offer_info_data_dict = {}
				offer_info_data_dict['id'] =line[0]
				offer_info_data_dict['image'] =line[1]
				offer_info_data_dict['offer'] =line[2]
				offer_info_data_dict['imageurl']  ='https://storage.googleapis.com/momvendor.appspot.com/offer/'

				offer_info_data_db.append(offer_info_data_dict)

		resp = Response(json.dumps({"success": True, "menu_data": offer_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/customer/get/customer/address/',methods=['GET','POST'])
def ApiCustomerAdd():
	if request.method=='POST':
		user_data =json.loads(request.data)
		try:
			mobile  = user_data['mobile']
		except:
			mobile=''
		user_status = dbhelper.GetData().GetCustomerAdd(mobile)
		if user_status==True:
			order_info_data = dbhelper.GetData().GetCustomerAddress(mobile)
			order_info_data_db = []

			if(len(order_info_data))>0:
				for line in order_info_data:
					order_info_data_dict = {}
					order_info_data_dict['id'] =line[0]
					order_info_data_dict['name'] =line[2]
					order_info_data_dict['address'] =line[4]
					order_info_data_dict['latitude'] =line[5]
					order_info_data_dict['longitude'] =line[6]
					order_info_data_db.append(order_info_data_dict)
			resp = Response(json.dumps({"success": True, "address_data": order_info_data_db },ensure_ascii=False))
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			order_info_data = dbhelper.GetData().GetCustomerAddress2(mobile)
			order_info_data_db = []

			if(len(order_info_data))>0:
				for line in order_info_data:
					order_info_data_dict = {}
					order_info_data_dict['id'] =line[0]
					order_info_data_dict['mobile'] =line[1]
					order_info_data_dict['address'] =line[2]
					order_info_data_dict['latitude']  =line[3]
					order_info_data_dict['longitude']  =line[4]
					order_info_data_dict['phone_number']  =line[5]
					order_info_data_dict['name']  =line[6]

					order_info_data_db.append(order_info_data_dict)

			resp = Response(json.dumps({"success": True, "address_data": order_info_data_db },ensure_ascii=False))
			resp.headers['Content-type']='application/json'
			return after_request(resp)


@app.route('/customer/get/address/',methods=['GET','POST'])
def ApiCustomerAddress():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile  = user_data['mobile']

		order_info_data = dbhelper.GetData().GetCustomerAddress3(mobile)
		order_info_data_db = []

		if(len(order_info_data))>0:
			for line in order_info_data:
				order_info_data_dict = {}
				order_info_data_dict['id'] =line[0]
				order_info_data_dict['mobile'] =line[1]

				order_info_data_dict['address'] =line[2]
				order_info_data_dict['latitude'] =line[3]
				order_info_data_dict['longitude'] =line[4]
				order_info_data_dict['phone_number'] =line[5]
				order_info_data_dict['name'] =line[6]
				order_info_data_db.append(order_info_data_dict)
		resp = Response(json.dumps({"success": True, "address_data": order_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/customer/customer/addtoken/', methods=['GET','POST'])
def fcmAuthEmployee():
	if request.method       == 'POST':
		token_data =json.loads(request.data)
		mobile=token_data['mobile']
		fcmToken =token_data['fcmToken']
		update =dbhelper.DeleteData().deleteToken(mobile)
		last =dbhelper.AddData().addToken(mobile,fcmToken)
		if last:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/delete/address/', methods=['GET','POST'])
def DeleteAddress():
	if request.method       == 'POST':
		user_data =json.loads(request.data)
		Id=user_data['id']
		last =dbhelper.DeleteData().DeleteAddress(Id)
		if last:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/offer/upload/',methods=['GET','POST'])
def apiSankalpUpload():
	if request.method=='POST':
		file_object = request.files['file']
		BUCKET_NAME = 'momvendor.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')

		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'offer'
		filename = file_object.filename
		print filename
		string_io_file = StringIO.StringIO(file_object.stream.read())

		fullName = GCS_UPLOAD_FOLDER + '/'+ filename
		body = {
			'name': fullName,
		}

		req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'application/octet-stream'))
		response = req.execute()
		resp = Response(json.dumps({"success": True, "datasets": 'Yahoo'},ensure_ascii=False))
		return after_request(resp)



######Api For Cash Transaction From Web ###########
@app.route('/customer/add/order/list/updated/web/',methods=['GET','POST'])
def APiAddorderlistWebUpdated():
	if request.method=='POST':
		subscriptionInfo= json.loads(request.data)
		print subscriptionInfo
		name= subscriptionInfo['name']
		location= subscriptionInfo['location']
		mobile= subscriptionInfo['mobile']

		latitude= subscriptionInfo['latitude']
		longitude= subscriptionInfo['longitude']
		mom_mobile= subscriptionInfo['mom_mobile']
		product_list= subscriptionInfo['product_list']
		note = subscriptionInfo['note'].replace("'","")
		lastId  =dbhelper.GetData().getLastIDNewOrderInfo()[0][0]
		promoCode  =subscriptionInfo['promoCode']

		subTotal= subscriptionInfo['sub_total']
		discount_amount  =subscriptionInfo['discount_amount']
		delivery_charge  =subscriptionInfo['delivery_charge']
		tax_amount=subscriptionInfo['tax_amount']
		totalPrice= subscriptionInfo['total_price']
		orderStatus=0
		subTotal = float(subTotal) - float(discount_amount)
		promo_info_data = dbhelper.GetData().applyoffer(promoCode)

		chefDiscountVal = 0
		if(len(promo_info_data))>0:
			discount=promo_info_data[0][3]
			max_amount=promo_info_data[0][4]
			chefDiscountVal = promo_info_data[0][11]
		momDiscountVal = float(discount_amount) - chefDiscountVal


		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		orderId = 'CRN' + str(mobile[-4:]) + newid

		menulist=[]

		chefPrice =0
		momPrice =0
		packagingPrice =0

		itemInfoListSet =[]
		for offline in product_list:
			itemInfoList =[]
			food_item  = offline['itemName']
			quantity = offline['qty']
			item_id = offline['id']
			pType = offline['food_type']
			itemActualPrice = offline['fullPrice']
			price = offline['fullPrice']
			itemDescription= offline['itemDescription']
			image=offline['item_image']

			##Chef Price Calculation
			chefItemPrice_Q = int((float(price) - 10)/1.25)
			if chefItemPrice_Q < 100:
				chefItemPrice = chefItemPrice_Q


			else:
				chefItemPrice = float(price) - 70

			momItemPrice = float(price) - float(chefItemPrice) - 10
			chefPrice = chefPrice + chefItemPrice
			momPrice = momPrice + momItemPrice
			packagingPrice = packagingPrice +10


			### Mom Price Calculation
			itemInfoList.append(orderId)
			itemInfoList.append(food_item)
			itemInfoList.append(quantity)
			itemInfoList.append(item_id)
			itemInfoList.append(pType)
			itemInfoList.append(itemActualPrice)
			itemInfoList.append(price)
			itemInfoList.append(itemDescription)
			itemInfoList.append(image)
			itemInfoListSet.append(itemInfoList)

		if promoCode !="":
			addUserPromoUsage = dbhelper.AddData().addUserPromoUsage(mobile, promoCode)
		addOrderInfo = dbhelper.AddData().addOrderInfo(orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note.replace("'",""), promoCode)
		addOrderItemInfo = dbhelper.AddData().addOrderItemInfo(itemInfoListSet)
		addPricingInfo = dbhelper.AddData().addPricingInfo(orderId, totalPrice, chefPrice, momPrice, packagingPrice, tax_amount, discount_amount, subTotal,  delivery_charge, promoCode, chefDiscountVal, momDiscountVal, 'Active')
		addOrderIdInfo = dbhelper.AddData().addOrderIdIncrease()
		try:
			fcmTokenList=dbhelper.GetData().getTokenCustomer(mom_mobile)
			print fcmTokenList

			message_data={ "data":  {"orderId":orderId,"customerName":name,"message":"You got a new order!", "customerMobile":mobile, "totalAmount":totalPrice, "address":location, "note":note, "promoCode":promoCode,"dateTime": str(datetime.now()), "cancallable":1 },"to" : fcmTokenList[0][0]
			}
			form_data = json.dumps(message_data,ensure_ascii=False)
			url='https://fcm.googleapis.com/fcm/send'
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.POST,
				payload=form_data,
				headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"}
				)
			print resp.content
		except:
			pass
		try:
			mobile=str(mom_mobile)
			text ="Mother + On + Mission : +You + received + a + new + order +"+orderId
			url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,method=urlfetch.GET, headers={'Content-Type': 'text/html'})
			adminmobile=str("7892348164")
			text2 ="Mother + On + Mission : MOM + CHEF +"+mobile+" + received + a + new + order +"+orderId
			url2 ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(adminmobile),text2)
			urlfetch.set_default_fetch_deadline(45)
			resp2 = urlfetch.fetch(url=url2,method=urlfetch.GET, headers={'Content-Type': 'text/html'})

		except:
			print "error sending sms"
	resp = Response(json.dumps({"success": True},ensure_ascii=False))
	return after_request(resp)

########Cash Transaction Vai App
@app.route('/customer/add/order/list/updated/',methods=['GET','POST'])
def APiAddorderlist():
	if request.method=='POST':
		subscriptionInfo= json.loads(request.data)
		name= subscriptionInfo['name']
		mobile= subscriptionInfo['mobile']
		location= subscriptionInfo['location']

		latitude= subscriptionInfo['latitude']
		longitude= subscriptionInfo['longitude']
		mom_mobile= subscriptionInfo['mom_mobile']
		product_list= subscriptionInfo['product_list']
		note = subscriptionInfo['note'].replace("'","")
		lastId  =dbhelper.GetData().getLastIDNewOrderInfo()[0][0]
		promoCode  =subscriptionInfo['promoCode']

		subTotal= subscriptionInfo['sub_total']
		discount_amount  =subscriptionInfo['discount_amount']
		delivery_charge  =subscriptionInfo['delivery_charge']
		tax_amount=subscriptionInfo['tax_amount']
		totalPrice= subscriptionInfo['total_price']
		orderStatus=0
		subTotal = float(subTotal) - float(discount_amount)
		promo_info_data = dbhelper.GetData().applyoffer(promoCode)

		##For Price Calculation
		chefDiscountVal = 0
		if(len(promo_info_data))>0:
			discount=promo_info_data[0][3]
			max_amount=promo_info_data[0][4]
			chefDiscountVal = promo_info_data[0][11]
		momDiscountVal = float(discount_amount) - chefDiscountVal


		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		orderId = 'CRN' + str(mobile[-4:]) + newid

		menulist=[]

		chefPrice =0
		momPrice =0
		packagingPrice =0
		itemInfoListSet =[]
		for offline in product_list:
			itemInfoList =[]
			food_item  = offline['food_item']
			quantity = offline['quantity']
			item_id = offline['item_id']
			pType = offline['type']
			itemActualPrice = offline['itemActualPrice']
			price = offline['price']
			itemDescription= offline['itemDescription']
			image=offline['image']

			##Chef Price Calculation
			chefItemPrice_Q = int((float(price) - 10)/1.25)
			if chefItemPrice_Q <= 100:
				chefItemPrice = chefItemPrice_Q


			else:
				chefItemPrice = float(price) - 70

			momItemPrice = float(price) - float(chefItemPrice) - 10
			chefPrice = chefPrice + chefItemPrice
			momPrice = momPrice + momItemPrice
			packagingPrice = packagingPrice +10


			### Mom Price Calculation
			itemInfoList.append(orderId)
			itemInfoList.append(food_item)
			itemInfoList.append(quantity)
			itemInfoList.append(item_id)
			itemInfoList.append(pType)
			itemInfoList.append(itemActualPrice)
			itemInfoList.append(price)
			itemInfoList.append(itemDescription)
			itemInfoList.append(image)
			itemInfoListSet.append(itemInfoList)

		if promoCode !="":
			addUserPromoUsage = dbhelper.AddData().addUserPromoUsage(mobile, promoCode)
		addOrderInfo = dbhelper.AddData().addOrderInfo(orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode)
		addOrderItemInfo = dbhelper.AddData().addOrderItemInfo(itemInfoListSet)
		addPricingInfo = dbhelper.AddData().addPricingInfo(orderId, totalPrice, chefPrice, momPrice, packagingPrice, tax_amount, discount_amount, subTotal,  delivery_charge, promoCode, chefDiscountVal, momDiscountVal, 'Active')
		addOrderIdInfo = dbhelper.AddData().addOrderIdIncrease()
		try:
			fcmTokenList=dbhelper.GetData().getTokenCustomer(mom_mobile)
			print "fcmTokenLIst :"
			print fcmTokenList
			if(len(fcmTokenList)==0):
				print " The fcm token list is empty"

			message_data={ "data":  {"orderId":orderId,"customerName":name, "message":"You got a new order!","customerMobile":mobile, "totalAmount":totalPrice, "address":location, "note":note, "promoCode":promoCode,"dateTime": str(datetime.now()), "cancallable":1 },"to" : fcmTokenList[0][0]
			}
			print "message_data :"
			print message_data
			form_data = json.dumps(message_data,ensure_ascii=False)
			url='https://fcm.googleapis.com/fcm/send'
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.POST,
				payload=form_data,
				headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"}
				)
			print "fcm response"
			print resp
			print resp.content
		except:
			print "error sending fcm notification "
		try:
			mobile=str(mom_mobile)
			text ="Mother + On + Mission : +You + received + a + new + order +"+orderId
			url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,method=urlfetch.GET, headers={'Content-Type': 'text/html'})
			adminmobile=str("7892348164")
			text2 ="Mother + On + Mission : MOM + CHEF +"+mobile+" + received + a + new + order +"+orderId
			url2 ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(adminmobile),text2)
			urlfetch.set_default_fetch_deadline(45)
			resp2 = urlfetch.fetch(url=url2,method=urlfetch.GET, headers={'Content-Type': 'text/html'})

		except:
			print "error sending sms"

	resp = Response(json.dumps({"success": True},ensure_ascii=False))
	return after_request(resp)


@app.route('/customer/add/order/list/updated/app/online/',methods=['GET','POST'])
def APiAddorderlistonline():
	if request.method=='POST':
		subscriptionInfo= json.loads(request.data)
		name= subscriptionInfo['name']
		location= subscriptionInfo['location']
		mobile= subscriptionInfo['mobile']

		latitude= subscriptionInfo['latitude']
		longitude= subscriptionInfo['longitude']
		mom_mobile= subscriptionInfo['mom_mobile']
		product_list= subscriptionInfo['product_list']
		note = subscriptionInfo['note'].replace("'","")
		lastId  =dbhelper.GetData().getLastIDNewOrderInfo()[0][0]
		promoCode  =subscriptionInfo['promoCode']

		subTotal= subscriptionInfo['sub_total']
		discount_amount  =subscriptionInfo['discount_amount']
		delivery_charge  =subscriptionInfo['delivery_charge']
		tax_amount=subscriptionInfo['tax_amount']
		totalPrice= subscriptionInfo['total_price']
		payment_mode= subscriptionInfo['payment_mode']
		orderStatus=0
		subTotal = float(subTotal) - float(discount_amount)
		promo_info_data = dbhelper.GetData().applyoffer(promoCode)

		##For Price Calculation
		chefDiscountVal = 0
		if(len(promo_info_data))>0:
			discount=promo_info_data[0][3]
			max_amount=promo_info_data[0][4]
			chefDiscountVal = promo_info_data[0][11]
		momDiscountVal = float(discount_amount) - chefDiscountVal


		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		orderId = 'CRN' + str(mobile[-4:]) + newid

		menulist=[]

		chefPrice =0
		momPrice =0
		packagingPrice =0
		itemInfoListSet =[]
		for offline in product_list:
			itemInfoList =[]
			food_item  = offline['food_item']
			quantity = offline['quantity']
			item_id = offline['item_id']
			pType = offline['type']
			itemActualPrice = offline['itemActualPrice']
			price = offline['price']
			itemDescription= offline['itemDescription']
			image=offline['image']

			##Chef Price Calculation
			chefItemPrice_Q = int((float(price) - 10)/1.25)
			if chefItemPrice_Q <= 100:
				chefItemPrice = chefItemPrice_Q


			else:
				chefItemPrice = float(price) - 70

			momItemPrice = float(price) - float(chefItemPrice) - 10
			chefPrice = chefPrice + chefItemPrice
			momPrice = momPrice + momItemPrice
			packagingPrice = packagingPrice +10


			### Mom Price Calculation
			itemInfoList.append(orderId)
			itemInfoList.append(food_item)
			itemInfoList.append(quantity)
			itemInfoList.append(item_id)
			itemInfoList.append(pType)
			itemInfoList.append(itemActualPrice)
			itemInfoList.append(price)
			itemInfoList.append(itemDescription)
			itemInfoList.append(image)
			itemInfoListSet.append(itemInfoList)

		if promoCode !="":
			addUserPromoUsage = dbhelper.AddData().addUserPromoUsage(mobile, promoCode)
		addOrderInfo = dbhelper.AddData().addOrderInfoStatus(orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, -1, note, promoCode)
		addOrderItemInfo = dbhelper.AddData().addOrderItemInfo(itemInfoListSet)
		addPricingInfo = dbhelper.AddData().addPricingInfo(orderId, totalPrice, chefPrice, momPrice, packagingPrice, tax_amount, discount_amount, subTotal,  delivery_charge, promoCode, chefDiscountVal, momDiscountVal, 'Active')
		addOrderIdInfo = dbhelper.AddData().addOrderIdIncrease()

		try:
			fcmTokenList=dbhelper.GetData().getTokenCustomer(mom_mobile)
			print fcmTokenList

			message_data={ "data":  {"orderId":orderId,"customerName":name, "message":"You got a new order!", "customerMobile":mobile, "totalAmount":totalPrice, "address":location, "note":note, "promoCode":promoCode,"dateTime": str(datetime.now()), "cancallable":1 },"to" : fcmTokenList[0][0]
			}
			form_data = json.dumps(message_data,ensure_ascii=False)
			url='https://fcm.googleapis.com/fcm/send'
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.POST,
				payload=form_data,
				headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"}
				)
			print resp.content
		except:
			pass
		try:
			mobile=str(mom_mobile)
			text ="Mother + On + Mission : +You + received + a + new + order +"+orderId
			url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,method=urlfetch.GET, headers={'Content-Type': 'text/html'})
			adminmobile=str("7892348164")
			text2 ="Mother + On + Mission : MOM + CHEF +"+mobile+" + received + a + new + order +"+orderId
			url2 ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(adminmobile),text2)
			urlfetch.set_default_fetch_deadline(45)
			resp2 = urlfetch.fetch(url=url2,method=urlfetch.GET, headers={'Content-Type': 'text/html'})

		except:
			print "error sending sms"

	resp = Response(json.dumps({"success": True, "orderId": orderId},ensure_ascii=False))
	return after_request(resp)



@app.route('/customer/add/order/list/updated/web/online/',methods=['GET','POST'])
def APiAddorderlistWebUpdatedOnline():
	if request.method=='POST':
		subscriptionInfo= json.loads(request.data)
		name= subscriptionInfo['name']
		location= subscriptionInfo['location']
		mobile= subscriptionInfo['mobile']

		latitude= subscriptionInfo['latitude']
		longitude= subscriptionInfo['longitude']
		mom_mobile= subscriptionInfo['mom_mobile']
		product_list= subscriptionInfo['product_list']
		note = subscriptionInfo['note'].replace("'","")
		lastId  =dbhelper.GetData().getLastIDNewOrderInfo()[0][0]
		promoCode  =subscriptionInfo['promoCode']

		subTotal= subscriptionInfo['sub_total']
		discount_amount  =subscriptionInfo['discount_amount']
		delivery_charge  =subscriptionInfo['delivery_charge']
		tax_amount=subscriptionInfo['tax_amount']
		totalPrice= subscriptionInfo['total_price']
		payment_mode= subscriptionInfo['payment_mode']
		orderStatus=0
		subTotal = float(subTotal) - float(discount_amount)
		promo_info_data = dbhelper.GetData().applyoffer(promoCode)

		chefDiscountVal = 0
		if(len(promo_info_data))>0:
			discount=promo_info_data[0][3]
			max_amount=promo_info_data[0][4]
			chefDiscountVal = promo_info_data[0][11]
		momDiscountVal = float(discount_amount) - chefDiscountVal


		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		orderId = 'CRN' + str(mobile[-4:]) + newid

		menulist=[]

		chefPrice =0
		momPrice =0
		packagingPrice =0

		itemInfoListSet =[]
		for offline in product_list:
			itemInfoList =[]
			food_item  = offline['itemName']
			quantity = offline['qty']
			item_id = offline['id']
			pType = offline['food_type']
			itemActualPrice = offline['fullPrice']
			price = offline['fullPrice']
			itemDescription= offline['itemDescription']
			image=offline['item_image']

			##Chef Price Calculation
			chefItemPrice_Q = int((float(price) - 10)/1.25)
			if chefItemPrice_Q < 100:
				chefItemPrice = chefItemPrice_Q


			else:
				chefItemPrice = float(price) - 70

			momItemPrice = float(price) - float(chefItemPrice) - 10
			chefPrice = chefPrice + chefItemPrice
			momPrice = momPrice + momItemPrice
			packagingPrice = packagingPrice +10


			### Mom Price Calculation
			itemInfoList.append(orderId)
			itemInfoList.append(food_item)
			itemInfoList.append(quantity)
			itemInfoList.append(item_id)
			itemInfoList.append(pType)
			itemInfoList.append(itemActualPrice)
			itemInfoList.append(price)
			itemInfoList.append(itemDescription)
			itemInfoList.append(image)
			itemInfoListSet.append(itemInfoList)

		orderStatus =-1
		addOrderInfo = dbhelper.AddData().addOrderInfoStatus(orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode)
		addOrderItemInfo = dbhelper.AddData().addOrderItemInfo(itemInfoListSet)
		addPricingInfo = dbhelper.AddData().addPricingInfo(orderId, totalPrice, chefPrice, momPrice, packagingPrice, tax_amount, discount_amount, subTotal,  delivery_charge, promoCode, chefDiscountVal, momDiscountVal, 'Pending')
		addOrderIdInfo = dbhelper.AddData().addOrderIdIncrease()

		try:
			fcmTokenList=dbhelper.GetData().getTokenCustomer(mom_mobile)
			print fcmTokenList

			message_data={ "data":  {"orderId":orderId,"customerName":name, "message":"You got a new order!", "customerMobile":mobile, "totalAmount":totalPrice, "address":location, "note":note, "promoCode":promoCode,"dateTime":str(datetime.now()), "cancallable":1 },"to" : fcmTokenList[0][0]
			}
			form_data = json.dumps(message_data,ensure_ascii=False)
			url='https://fcm.googleapis.com/fcm/send'
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.POST,
				payload=form_data,
				headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"}
				)
			print resp.content
		except:
			pass

		try:
			mobile=str(mom_mobile)
			text ="Mother + On + Mission : +You + received + a + new + order +"+orderId
			url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,method=urlfetch.GET, headers={'Content-Type': 'text/html'})
			adminmobile=str("7892348164")
			text2 ="Mother + On + Mission : MOM + CHEF +"+mobile+" + received + a + new + order +"+orderId
			url2 ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(adminmobile),text2)
			urlfetch.set_default_fetch_deadline(45)
			resp2 = urlfetch.fetch(url=url2,method=urlfetch.GET, headers={'Content-Type': 'text/html'})

		except:
			print "error sending sms"
	resp = Response(json.dumps({"success": True, "orderId": orderId},ensure_ascii=False))
	return after_request(resp)




@app.route('/customer/add/order/list/updated/new/',methods=['GET','POST'])
def APiAddorderlistNew():
	if request.method=='POST':
		subscriptionInfo= json.loads(request.data)
		name= subscriptionInfo['name']
		location= subscriptionInfo['location']
		mobile= subscriptionInfo['mobile']

		latitude= subscriptionInfo['latitude']
		longitude= subscriptionInfo['longitude']
		mom_mobile= subscriptionInfo['mom_mobile']
		product_list= subscriptionInfo['product_list']
		note = subscriptionInfo['note'].replace("'","")
		lastId  =dbhelper.GetData().getLastIDNewOrderInfo()[0][0]
		promoCode  =subscriptionInfo['promoCode']

		subTotal= subscriptionInfo['sub_total']
		discount_amount  =subscriptionInfo['discount_amount']
		delivery_charge  =subscriptionInfo['delivery_charge']
		tax_amount=subscriptionInfo['tax_amount']
		totalPrice= subscriptionInfo['total_price']
		payment_mode= subscriptionInfo['payment_mode']
		orderStatus=0
		subTotal = float(subTotal) - float(discount_amount)
		promo_info_data = dbhelper.GetData().applyoffer(promoCode)

		##For Price Calculation
		chefDiscountVal = 0
		if(len(promo_info_data))>0:
			discount=promo_info_data[0][3]
			max_amount=promo_info_data[0][4]
			chefDiscountVal = promo_info_data[0][11]
		momDiscountVal = float(discount_amount) - chefDiscountVal


		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		orderId = 'CRN' + str(mobile[-4:]) + newid

		menulist=[]

		chefPrice =0
		momPrice =0
		packagingPrice =0
		itemInfoListSet =[]
		for offline in product_list:
			itemInfoList =[]
			food_item  = offline['food_item']
			quantity = offline['quantity']
			item_id = offline['item_id']
			pType = offline['type']
			itemActualPrice = offline['itemActualPrice']
			price = offline['price']
			itemDescription= offline['itemDescription']
			image=offline['image']

			##Chef Price Calculation
			chefItemPrice_Q = int((float(price) - 10)/1.25)
			if chefItemPrice_Q <= 100:
				chefItemPrice = chefItemPrice_Q


			else:
				chefItemPrice = float(price) - 70

			momItemPrice = float(price) - float(chefItemPrice) - 10
			chefPrice = chefPrice + chefItemPrice
			momPrice = momPrice + momItemPrice
			packagingPrice = packagingPrice +10


			### Mom Price Calculation
			itemInfoList.append(orderId)
			itemInfoList.append(food_item)
			itemInfoList.append(quantity)
			itemInfoList.append(item_id)
			itemInfoList.append(pType)
			itemInfoList.append(itemActualPrice)
			itemInfoList.append(price)
			itemInfoList.append(itemDescription)
			itemInfoList.append(image)
			itemInfoListSet.append(itemInfoList)

		if promoCode !="":
			addUserPromoUsage = dbhelper.AddData().addUserPromoUsage(mobile, promoCode)
		addOrderInfo = dbhelper.AddData().addOrderInfo(orderId, name, mobile, location, latitude, longitude, mom_mobile, totalPrice, orderStatus, note, promoCode)
		addOrderItemInfo = dbhelper.AddData().addOrderItemInfo(itemInfoListSet)
		addPricingInfo = dbhelper.AddData().addPricingInfo(orderId, totalPrice, chefPrice, momPrice, packagingPrice, tax_amount, discount_amount, subTotal,  delivery_charge, promoCode, chefDiscountVal, momDiscountVal, 'Active')
		addOrderIdInfo = dbhelper.AddData().addOrderIdIncrease()
		try:
			fcmTokenList=dbhelper.GetData().getTokenCustomer(mom_mobile)
			print fcmTokenList

			message_data={ "data":  {"orderId":orderId,"customerName":name, "message":"You got a new order!", "customerMobile":mobile, "totalAmount":totalPrice, "address":location, "note":note, "promoCode":promoCode,"dateTime":str(datetime.now()), "cancallable":1 },"to" : fcmTokenList[0][0]
			}
			form_data = json.dumps(message_data,ensure_ascii=False)
			url='https://fcm.googleapis.com/fcm/send'
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.POST,
				payload=form_data,
				headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"}
				)
			print resp.content
		except:
			pass
		try:
			mobile=str(mom_mobile)
			text ="Mother + On + Mission : +You + received + a + new + order +"+orderId
			url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,method=urlfetch.GET, headers={'Content-Type': 'text/html'})
			adminmobile=str("7892348164")
			text2 ="Mother + On + Mission : MOM + CHEF +"+mobile+" + received + a + new + order : +"+orderId
			url2 ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(adminmobile),text2)
			urlfetch.set_default_fetch_deadline(45)
			resp2 = urlfetch.fetch(url=url2,method=urlfetch.GET, headers={'Content-Type': 'text/html'})

		except:
			print "error sending sms"

	resp = Response(json.dumps({"success": True},ensure_ascii=False))
	return after_request(resp)

@app.route('/customer/update/payment/status/',methods=['GET','POST'])
def apiUpdatePaymentStatus():
	if request.method=='POST':
		subscriptionInfo= json.loads(request.data)

		orderId= subscriptionInfo['orderId']
		getOrderDataStatus= dbhelper.GetData().getOrderDataBy(orderId)
		print getOrderDataStatus
		if len(getOrderDataStatus)==0:
			resp = Response(json.dumps({"success": True, "confirmation":0},ensure_ascii=False))
			return after_request(resp)
		else:
			if getOrderDataStatus[0][9]==-1:
				resp = Response(json.dumps({"success": True, "confirmation":0},ensure_ascii=False))
				return after_request(resp)
			elif getOrderDataStatus[0][9]==-2:
				resp = Response(json.dumps({"success": True, "confirmation":2},ensure_ascii=False))
				return after_request(resp)
			else:
				# try:
				# 	fcmTokenList=dbhelper.GetData().getTokenCustomer(mobile)
				# 	print fcmTokenList
				#
				# 	message_data={ "data":  {"orderId":orderId,"customerName":name, "customerMobile":mobile, "totalAmount":totalPrice, "address":location, "note":note, "promoCode":promoCode,"dateTime":'', "cancallable":1 },"to" : fcmTokenList[0][0]
				# 	}
				# 	form_data = json.dumps(message_data)
				# 	url='https://fcm.googleapis.com/fcm/send'
				# 	urlfetch.set_default_fetch_deadline(45)
				# 	resp = urlfetch.fetch(url=url,
				# 		method=urlfetch.POST,
				# 		payload=form_data,
				# 		headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"}
				# 		)
				# 	print resp.content
				# except:
				# 	pass
				resp = Response(json.dumps({"success": True, "confirmation":1},ensure_ascii=False))
				return after_request(resp)



@app.route('/customer/generate/orderid/online/',methods=['GET','POST'])
def APiGenerateOnlineApi():
	if request.method=='POST':
		subscriptionInfo= json.loads(request.data)

		mobile= subscriptionInfo['mobile']
		lastId  =dbhelper.GetData().getLastIDNewOrderInfo()[0][0]
		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		orderId = 'CRN' + str(mobile[-4:]) + newid
		resp = Response(json.dumps({"orderId": orderId},ensure_ascii=False))
		return after_request(resp)


@app.route('/customer/add/offer/', methods=['GET','POST'])
def fcmAddOffer():
	if request.method       == 'POST':
		token_data =json.loads(request.data)
		offer=token_data['offer']
		image_name =token_data['image_name']
		last =dbhelper.AddData().addImages(offer,image_name)
		if last:
			db={'message':'Image Added',"confirmation":1}
		else:
			db={'message': 'Image not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db},ensure_ascii=False))
		return after_request(resp)

@app.route('/customer/get/vendor/list/web/',methods=['GET','POST'])
def ApiGetVendorListWeb():
	if request.method=='POST':
		vendor_data =json.loads(request.data)
		Lat=vendor_data['latitude']
		Lang =vendor_data['longitude']
		vendor_info_data = dbhelper.GetData().VendorList(Lat, Lang)
		vendor_info_data_db = []
		if(len(vendor_info_data))>0:
			for line in vendor_info_data:
				vendor_info_data_dict = {}
				vendor_info_data_dict['id']=line[0]
				vendor_info_data_dict['name']=line[1]
				vendor_info_data_dict['mobile']=line[2]
				vendor_info_data_dict['idType']=line[3]
				vendor_info_data_dict['idNumber']=line[4]
				vendor_info_data_dict['frontImage']=line[5]
				vendor_info_data_dict['backImage']=line[6]
				vendor_info_data_dict['dob']=line[7]
				vendor_info_data_dict['profileImage']=line[8]
				vendor_info_data_dict['pimagePath']=line[9]
				vendor_info_data_dict['awardImage']=line[10]
				vendor_info_data_dict['awardImagePath']=line[11]
				vendor_info_data_dict['accountNo']=line[12]
				vendor_info_data_dict['ifsc']=line[13]
				vendor_info_data_dict['bankName']=line[14]
				vendor_info_data_dict['status']=line[15]
				vendor_info_data_dict['partnerName']=line[16]
				vendor_info_data_dict['bankIdType']=line[17]
				vendor_info_data_dict['bankImageName']=line[18]
				vendor_info_data_dict['licenseNo']=line[19]
				vendor_info_data_dict['licenseName']=line[20]
				vendor_info_data_dict['licenceImage']=line[21]
				vendor_info_data_dict['parentName']=line[22]
				vendor_info_data_dict['houseNo']=line[23]
				vendor_info_data_dict['locality']=line[24]
				vendor_info_data_dict['state']=line[25]
				vendor_info_data_dict['pincode']=line[26]
				vendor_info_data_dict['city']=line[27]
				vendor_info_data_dict['referalCode']=line[28]
				vendor_info_data_dict['partnerReferal']=line[29]
				vendor_info_data_dict['referalType']=line[30]
				vendor_info_data_dict['declaration']=line[31]
				vendor_info_data_dict['skillName']=line[32]
				vendor_info_data_dict['totalCall']=line[33]
				vendor_info_data_dict['subscriptionDate']=line[34]
				vendor_info_data_dict['subscriptionAmount']=line[35]
				vendor_info_data_dict['walletBalance']=line[36]
				vendor_info_data_dict['identityStatus']=line[37]
				vendor_info_data_dict['personalStatus']=line[38]
				vendor_info_data_dict['declarationStatus']=line[39]
				vendor_info_data_dict['identityVerification']=line[40]
				vendor_info_data_dict['awardStatus']=line[41]
				vendor_info_data_dict['bankStatus']=line[42]
				vendor_info_data_dict['licenseStatus']=line[43]
				vendor_info_data_dict['documentStatus']=line[44]
				vendor_info_data_dict['fcmToken']=line[45]
				vendor_info_data_dict['partnerType']=line[46]
				vendor_info_data_dict['latitude']=line[47]
				vendor_info_data_dict['rating']='4.5'
				vendor_info_data_dict['longitude']=line[48]

				vendor_info_data_dict['updatedAt']=str(line[49])
				order_ist_time= (line[50]+ timedelta(hours=5, minutes=30))
				vendor_info_data_dict['createdAt']=str(order_ist_time)
				# vendor_info_data_dict['createdAt']=str(line[50])

				vendor_info_data_db.append(vendor_info_data_dict)

		resp = Response(json.dumps({"success": True, "vendor_data": vendor_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/customer/get/customer/order/list/',methods=['GET','POST'])
def ApiGetListOrder():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile=user_data['mobile']
		order_info_data = dbhelper.GetData().OrderList(mobile)
		order_info_data_db = []
		if(len(order_info_data))>0:
			for line in order_info_data:
				order_info_data_dict = {}
				order_info_data_dict['id']=line[0]
				order_info_data_dict['name']=line[1]
				order_info_data_dict['location']=line[2]
				order_info_data_dict['price']=line[3]
				order_info_data_dict['mobile']=line[4]
				order_info_data_dict['total_price']=line[5]
				order_info_data_dict['latitude']=line[6]
				order_info_data_dict['longitude']=line[7]
				order_info_data_dict['food_item']=line[8]
				order_info_data_dict['quantity']=line[9]
				order_info_data_dict['item_id']=line[10]
				order_info_data_dict['type']=line[11]
				order_info_data_dict['itemActualPrice']=line[12]
				order_info_data_dict['mom_mobile']=line[13]
				try:
					mom_name = dbhelper.GetData().getVendorLoginStatus(line[13])
					vendor_name=str(mom_name[0][0])+str(mom_name[0][2])
				except:
					vendor_name=''

				order_info_data_dict['vendor_name']=vendor_name

				order_info_data_db.append(order_info_data_dict)

		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/customer/get/running/order/list/',methods=['GET','POST'])
def ApiGetRunOrder():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile=user_data['mobile']
		order_info_data = dbhelper.GetData().RunOrderList(mobile)
		order_info_data_db = []
		if(len(order_info_data))>0:
			for line in order_info_data:
				order_info_data_dict = {}
				order_info_data_dict['id']=line[0]
				order_info_data_dict['orderId']=line[1]
				order_info_data_dict['name']=line[2]
				order_info_data_dict['mobile']=line[3]
				order_info_data_dict['location']=line[4]
				order_info_data_dict['latitude']=line[5]
				order_info_data_dict['longitude']=line[6]
				order_info_data_dict['mom_mobile']=line[7]
				order_info_data_dict['total_price']=line[8]
				order_info_data_db.append(order_info_data_dict)

		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/customer/get/vendor/list/',methods=['GET','POST'])
def ApiGetVendorList():
	if request.method=='POST':
		vendor_data =json.loads(request.data)
		strDate = str(date.today())
		dateNow= datetime.strptime(strDate, "%Y-%m-%d").strftime("%d/%m/%Y")
		Lat=vendor_data['latitude']
		Lang =vendor_data['longitude']
		try:
			mobile = vendor_data['mobile']
		except:
			mobile =''
		offer_info_data = dbhelper.GetData().offerList()
		offer_info_data_db = []
		if(len(offer_info_data))>0:
			for line in offer_info_data:
				offer_info_data_dict = {}
				offer_info_data_dict['id']=line[0]
				offer_info_data_dict['offer']=line[1]
				offer_info_data_dict['imagePath']='https://storage.googleapis.com/momvendor.appspot.com/offer/'

				offer_info_data_db.append(offer_info_data_dict)

		vendor_info_data = dbhelper.GetData().VendorDataList(Lat,Lang)
		vendor_info_data_db = []


		fav_mom_idstr = dbhelper.GetData().GetMomFavouriteUserLst(mobile)

		if fav_mom_idstr is None:
			fav_mom_lst =[]
		else:
			fav_mom_lst = fav_mom_idstr.split(',')



		if(len(vendor_info_data))>0:
			for line in vendor_info_data:
				vendor_info_data_dict = {}
				vendor_info_data_dict['id']=line[0]
				if str(line[0]) in fav_mom_lst:
					vendor_info_data_dict['flag']=1
				else:
					vendor_info_data_dict['flag']=0
				vendor_info_data_dict['fisrtName']=line[1]
				vendor_info_data_dict['lastName']=line[2]
				vendor_info_data_dict['middleName']=line[3]
				vendor_info_data_dict['email']=line[4]
				vendor_info_data_dict['mobile']=line[5]
				partner_job = dbhelper.GetData().getPromocode(line[5])
				if (len(partner_job))>0:
					vendor_info_data_dict['promocode']  = partner_job[0][0]
				else:
					vendor_info_data_dict['promocode']  = ''
				vendor_info_data_dict['address']=line[6]
				vendor_info_data_dict['country']=line[7]
				vendor_info_data_dict['state']=line[8]
				vendor_info_data_dict['zipCode']=line[9]
				vendor_info_data_dict['foodLicenseNo']=line[10]
				vendor_info_data_dict['dob']=line[11]
				vendor_info_data_dict['specialization']=line[12]
				vendor_info_data_dict['comment']=line[13]
				vendor_info_data_dict['openTime']=line[14]
				vendor_info_data_dict['endTime']=line[15]
				vendor_info_data_dict['breakStart']=line[16]
				vendor_info_data_dict['breakEnd']=line[17]
				vendor_info_data_dict['profileStatus']=line[18]
				vendor_info_data_dict['image_name']=line[19]
				vendor_info_data_dict['latitude']=line[20]
				vendor_info_data_dict['rating']='4.5'
				vendor_info_data_dict['longitude']=line[21]

				checkStringLst= dbhelper.GetData().VendorMenuList(line[5])
				# checkStringLst= data[13].split(',')
				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['food_type'] = check[2]
					check_dict['itemName'] = check[3]
					check_dict['itemName'] = check[3]
					check_dict['itemName'] = check[3]
					check_dict['itemName'] = check[3]
					check_dict['itemName'] = check[3]
					check_dict['itemName'] = check[3]


					checkList.append(check_dict)

				vendor_info_data_dict['menuList']=checkList



				# vendor_info_data_dict['status']=line[22]
				vendor_info_data_dict['image']=line[22]
				vendor_info_data_dict['description']=line[23]

				vendor_info_data_dict['onlineStatus']=line[24]
				try:
					tDist = haversine(float(Lat),float(Lang),float(line[20]),float(line[21]))
				except:
					tDist = 0
				try:
					vendor_info_data_dict['estimateTime']=int(float(tDist)/8 *60)
				except:
					vendor_info_data_dict['estimateTime']=0
				vendor_info_data_db.append(vendor_info_data_dict)

		resp = Response(json.dumps({"success": True, "vendor_data": vendor_info_data_db ,"toprated_list": vendor_info_data_db,"offer":offer_info_data_db,"position":0},ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/customer/get/vendor/list/paginated/<id>/',methods=['GET','POST'])
def ApiGetVendorListPaginated(id):
	if request.method=='POST':
		vendor_data =json.loads(request.data)
		Lat=vendor_data['latitude']
		Lang =vendor_data['longitude']
		try:
			mobile = vendor_data['mobile']
		except:
			mobile =''

		# draw = request.args.get('draw')
		# length = request.args.get('length')
		# start = request.args.get('start')
		# # search_val = request.args.get('search[value]')
		# Lat = request.args.get('latitude')
		# Lang = request.args.get('longitude')
		# mobile = request.args.get('mobile')



		vendor_info_data = dbhelper.GetData().VendorDataListWithMenu(Lat,Lang, id)
		vendor_info_data_db = []
		fav_mom_lst =[]
		#fav_mom_idstr = dbhelper.GetData().GetMomFavouriteUserLst(mobile)
		#if fav_mom_idstr is None:
		#	fav_mom_lst =[]
		#else:
		#	fav_mom_lst = fav_mom_idstr.split(',')



		if(len(vendor_info_data))>0:
			for line in vendor_info_data:
				try:
					vendor_info_data_dict = {}
					print "current mom : "+line[5]
					vendor_info_data_dict['id']=line[0]
					if str(line[0]) in fav_mom_lst:
						vendor_info_data_dict['flag']=1
					else:
						vendor_info_data_dict['flag']=0
					vendor_info_data_dict['fisrtName']=line[1]
					vendor_info_data_dict['lastName']=line[2]
					vendor_info_data_dict['middleName']=line[3]
					vendor_info_data_dict['email']=line[4]
					vendor_info_data_dict['mobile']=line[5]
					partner_job = dbhelper.GetData().getPromocode(line[5])
					if (len(partner_job))>0:
						vendor_info_data_dict['promocode']  = partner_job[0][0]
					else:
						vendor_info_data_dict['promocode']  = ''
					vendor_info_data_dict['address']=line[6]
					vendor_info_data_dict['country']=line[7]
					vendor_info_data_dict['state']=line[8]
					vendor_info_data_dict['zipCode']=line[9]
					vendor_info_data_dict['foodLicenseNo']=line[10]
					vendor_info_data_dict['dob']=line[11]
					vendor_info_data_dict['specialization']=line[12]
					vendor_info_data_dict['comment']=line[13]
					vendor_info_data_dict['openTime']=line[14]
					vendor_info_data_dict['endTime']=line[15]
					vendor_info_data_dict['breakStart']=line[16]
					vendor_info_data_dict['breakEnd']=line[17]
					vendor_info_data_dict['profileStatus']=line[18]
					vendor_info_data_dict['image_name']=line[19]
					vendor_info_data_dict['latitude']=line[20]
					vendor_info_data_dict['rating']='4.5'
					vendor_info_data_dict['longitude']=line[21]

					checkStringLst= dbhelper.GetData().VendorMenuList(line[5])
					# checkStringLst= data[13].split(',')
					checkList=[]
					for check in checkStringLst:
						print "menu under process : "+check[3]
						check_dict={}
						check_dict['id'] = check[1]
						check_dict['food_type'] = check[2]
						check_dict['itemName'] = check[3]
						check_dict['itemDescription'] = check[4]
						check_dict['itemGroup'] = check[5]
						check_dict['halfPrice'] = check[9]
						check_dict['quarterPrice'] = check[10]
						check_dict['fullPrice'] = check[11]
						check_dict['item_image'] = check[12]
						check_dict['image_name'] = check[13]
						check_dict['specialItem'] = check[14]
						check_dict['itemPreparationTime'] = check[16]
						check_dict['status'] = check[17]



						checkList.append(check_dict)

					vendor_info_data_dict['menuList']=checkList



					# vendor_info_data_dict['status']=line[22]
					vendor_info_data_dict['image']=line[22]
					vendor_info_data_dict['description']=line[23]

					vendor_info_data_dict['onlineStatus']=line[24]
					try:
						tDist = haversine(float(Lat),float(Lang),float(line[20]),float(line[21]))
					except:
						tDist = 0
					try:
						vendor_info_data_dict['estimateTime']=int(float(tDist)/8 *60)
					except:
						vendor_info_data_dict['estimateTime']=0
					vendor_info_data_db.append(vendor_info_data_dict)
				except Exception as e:
					print e
		print "the response back :"
		print vendor_info_data_db
		try:
			print json.dumps({"success": True, "vendor_data": vendor_info_data_db ,"position":0},ensure_ascii=False)
		except Exception as e:
			print "here mus tbe the issue"
			print e
		resp = Response(json.dumps({"success": True, "vendor_data": vendor_info_data_db ,"position":0},ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# @app.route('/customer/get/vendor/list/paginated/<id>/',methods=['GET','POST'])
# def ApiGetVendorListPaginated(id):
# 	if request.method=='POST':
# 		vendor_data =json.loads(request.data)
# 		Lat=vendor_data['latitude']
# 		Lang =vendor_data['longitude']
# 		try:
# 			mobile = vendor_data['mobile']
# 		except:
# 			mobile =''
#
# 		vendor_info_data = dbhelper.GetData().VendorDataListWithMenuUpdated(Lat,Lang, id)
#
# 		fav_mom_idstr = dbhelper.GetData().GetMomFavouriteUserLst(mobile)
# 		if fav_mom_idstr is None:
# 			fav_mom_lst =[]
# 		else:
# 			fav_mom_lst = fav_mom_idstr.split(',')
#
#
# 		vendor_info_data_db = []
# 		vendor_list_with_menu = []
# 		vendor_added = {}
#
# 		if(len(vendor_info_data))>0:
# 			for line in vendor_info_data:
# 				# isVendorAdded = vendor_added[line[5]]
# 				if(line[5] not in vendor_added):
# 					vendor_info_data_dict = {}
# 					vendor_info_data_dict['id']=line[0]
# 					if str(line[0]) in fav_mom_lst:
# 						vendor_info_data_dict['flag']=1
# 					else:
# 						vendor_info_data_dict['flag']=0
# 					vendor_info_data_dict['fisrtName']=line[1]
# 					vendor_info_data_dict['lastName']=line[2]
# 					vendor_info_data_dict['middleName']=line[3]
# 					vendor_info_data_dict['email']=line[4]
# 					vendor_info_data_dict['mobile']=line[5]
# 					partner_job = dbhelper.GetData().getPromocode(line[5])
# 					if (len(partner_job))>0:
# 						vendor_info_data_dict['promocode']  = partner_job[0][0]
# 					else:
# 						vendor_info_data_dict['promocode']  = ''
# 					vendor_info_data_dict['address']=line[6]
# 					vendor_info_data_dict['country']=line[7]
# 					vendor_info_data_dict['state']=line[8]
# 					vendor_info_data_dict['zipCode']=line[9]
# 					vendor_info_data_dict['foodLicenseNo']=line[10]
# 					vendor_info_data_dict['dob']=line[11]
# 					vendor_info_data_dict['specialization']=line[12]
# 					vendor_info_data_dict['comment']=line[13]
# 					vendor_info_data_dict['openTime']=line[14]
# 					vendor_info_data_dict['endTime']=line[15]
# 					vendor_info_data_dict['breakStart']=line[16]
# 					vendor_info_data_dict['breakEnd']=line[17]
# 					vendor_info_data_dict['profileStatus']=line[18]
# 					vendor_info_data_dict['image_name']=line[19]
# 					vendor_info_data_dict['latitude']=line[20]
# 					vendor_info_data_dict['rating']='4.5'
# 					vendor_info_data_dict['longitude']=line[21]
#
# 					# checkStringLst= dbhelper.GetData().VendorMenuList(line[5])
# 					# # checkStringLst= data[13].split(',')
# 					# checkList=[]
# 					# for check in checkStringLst:
# 					# 	check_dict={}
# 					# 	check_dict['food_type'] = check[2]
# 					# 	check_dict['itemName'] = check[3]
# 					#
# 					#
# 					# 	checkList.append(check_dict)
# 					#
# 					# vendor_info_data_dict['menuList']=checkList
#
#
#
# 					# vendor_info_data_dict['status']=line[22]
# 					vendor_info_data_dict['image']=line[22]
# 					vendor_info_data_dict['description']=line[23]
#
# 					vendor_info_data_dict['onlineStatus']=line[24]
# 					try:
# 						tDist = haversine(float(Lat),float(Lang),float(line[20]),float(line[21]))
# 					except:
# 						tDist = 0
# 					try:
# 						vendor_info_data_dict['estimateTime']=int(float(tDist)/8 *60)
# 					except:
# 						vendor_info_data_dict['estimateTime']=0
# 					vendor_info_data_dict["menuList"] = []
# 					vendor_info_data_db.append(vendor_info_data_dict)
# 					vendor_added[line[5]] = vendor_info_data_dict
# 				if(line[5] in vendor_added):
# 					vendor = vendor_added[line[5]]
# 					menu_info_data_dict = {}
# 					menu_info_data_dict['food_type'] = line[25]
# 					menu_info_data_dict['itemName'] = line[26]
# 					vendor["menuList"].append(menu_info_data_dict)
#
# 		resp = Response(json.dumps({"success": True, "vendor_data": vendor_info_data_db ,"position":0}))
# 		resp.headers['Content-type']='application/json'
# 		return after_request(resp)

@app.route('/customer/get/vendor/menu/',methods=['GET','POST'])
def ApiGetVendormenuList():
	if request.method=='POST':
		vendor_data =json.loads(request.data)
		Lat=vendor_data['latitude']
		Lang =vendor_data['longitude']
		vendor_info_data = dbhelper.GetData().VendorList(Lat,Lang)
		vendor_info_data_db = []
		if(len(vendor_info_data))>0:
			for line in vendor_info_data:
				vendor_info_data_dict = {}
				vendor_info_data_dict['id']=line[0]
				vendor_info_data_dict['fisrtName']=line[1]
				vendor_info_data_dict['lastName']=line[2]
				vendor_info_data_dict['middleName']=line[3]
				vendor_info_data_dict['email']=line[4]
				vendor_info_data_dict['mobile']=line[5]
				checkStringLst= dbhelper.GetData().VendorMenuList(line[5])
				# checkStringLst= data[13].split(',')
				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['food_type'] = check[2]
					check_dict['itemName'] = check[3]


					checkList.append(check_dict)

				vendor_info_data_dict['menuList']=checkList
				vendor_info_data_dict['address']=line[6]
				vendor_info_data_dict['country']=line[7]
				vendor_info_data_dict['state']=line[8]
				vendor_info_data_dict['zipCode']=line[9]
				vendor_info_data_dict['foodLicenseNo']=line[10]
				vendor_info_data_dict['dob']=line[11]
				vendor_info_data_dict['specialization']=line[12]
				vendor_info_data_dict['comment']=line[13]
				vendor_info_data_dict['openTime']=line[14]
				vendor_info_data_dict['endTime']=line[15]
				vendor_info_data_dict['breakStart']=line[16]
				vendor_info_data_dict['breakEnd']=line[17]
				vendor_info_data_dict['profileStatus']=line[18]
				vendor_info_data_dict['image_name']=line[19]
				vendor_info_data_dict['latitude']=line[20]
				vendor_info_data_dict['rating']='4.5'
				vendor_info_data_dict['longitude']=line[21]
				# vendor_info_data_dict['itemName']=line[22]
				try:
					tDist = haversine(float(Lat),float(Lang),float(line[20]),float(line[21]))
				except:
					tDist = 0
				try:
					vendor_info_data_dict['estimateTime']=int(float(tDist)/8 *60)
				except:
					vendor_info_data_dict['estimateTime']=0
				vendor_info_data_db.append(vendor_info_data_dict)

		resp = Response(json.dumps({"success": True, "vendor_data": vendor_info_data_db},ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/customer/get/vendor/menu/updated/',methods=['GET','POST'])
def ApiGetVendormenuListUpdated():
	if request.method=='POST':
		vendor_data =json.loads(request.data)
		Lat=vendor_data['latitude']
		Lang =vendor_data['longitude']
		vendor_info_data = dbhelper.GetData().VendorList(Lat,Lang)
		vendor_info_data_dict_final = []
		if(len(vendor_info_data))>0:
			for line in vendor_info_data:
				vendor_info_data_dict = {}
				vendor_info_data_dict['id']=line[0]
				vendor_info_data_dict['fisrtName']=line[1]
				vendor_info_data_dict['lastName']=line[2]
				vendor_info_data_dict['middleName']=line[3]
				vendor_info_data_dict['email']=line[4]
				vendor_info_data_dict['mobile']=line[5]
				checkStringLst= dbhelper.GetData().VendorMenuList(line[5])
				# checkStringLst= data[13].split(',')
				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['food_type'] = check[2]
					check_dict['itemName'] = check[3]


					checkList.append(check_dict)

				vendor_info_data_dict['menuList']=checkList
				vendor_info_data_dict['address']=line[6]
				vendor_info_data_dict['country']=line[7]
				vendor_info_data_dict['state']=line[8]
				vendor_info_data_dict['zipCode']=line[9]
				vendor_info_data_dict['foodLicenseNo']=line[10]
				vendor_info_data_dict['dob']=line[11]
				vendor_info_data_dict['specialization']=line[12]
				vendor_info_data_dict['comment']=line[13]
				vendor_info_data_dict['openTime']=line[14]
				vendor_info_data_dict['endTime']=line[15]
				vendor_info_data_dict['breakStart']=line[16]
				vendor_info_data_dict['breakEnd']=line[17]
				vendor_info_data_dict['profileStatus']=line[18]
				vendor_info_data_dict['image_name']=line[19]
				vendor_info_data_dict['latitude']=line[20]
				vendor_info_data_dict['rating']='4.5'
				vendor_info_data_dict['longitude']=line[21]
				# vendor_info_data_dict['itemName']=line[22]
				try:
					tDist = haversine(float(Lat),float(Lang),float(line[20]),float(line[21]))
				except:
					tDist = 0
				try:
					vendor_info_data_dict['estimateTime']=int(float(tDist)/8 *60)
				except:
					vendor_info_data_dict['estimateTime']=0
				vendor_info_data_dict_final[line[0]]=vendor_info_data_dict

		resp = Response(json.dumps({"success": True, "vendor_data": vendor_info_data_dict_final},ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/customer/apply/promocode/',methods=['GET','POST'])
def ApiGetPromoList():
	if request.method=='POST':
		promo_data =json.loads(request.data)
		promocode=promo_data['promocode']
		total_price= promo_data['total_price']
		mobile = promo_data['mobile']

		promo_info_data = dbhelper.GetData().applyoffer(promocode)
		getUsageLimit = dbhelper.GetData().getUsageLimit(mobile, promocode)
		print '**', getUsageLimit
		if(len(promo_info_data))>0:

			discount=promo_info_data[0][3]
			max_amount=promo_info_data[0][4]

			chefVal = promo_info_data[0][11]
			momVal = promo_info_data[0][12]
			minVal = promo_info_data[0][13]
			maxVal = promo_info_data[0][14]

			usage_limit =  promo_info_data[0][5]

			#Increase Size
			min_cart_val = promo_info_data[0][15]
			min_cart_val=101


			if len(getUsageLimit)!=0:
				if int(getUsageLimit[0][0]) < int(usage_limit):
					if float(total_price) >= float(min_cart_val):
						discount_price = chefVal + momVal+ random.randint(minVal, maxVal)
						discounted_price = float(total_price) - discount_price
						msg= "PromoCode Successfully Applied"
						promo_status = 1
					else:
						discount_price=0
						discounted_price= total_price
						msg= "PromoCode Can't be Applied"
						promo_status = 2
				else:
					discount_price=0
					discounted_price= total_price
					msg= "PromoCode Can't be Applied"
					promo_status = 3
			else:
				if float(total_price) >= float(min_cart_val):
					discount_price = chefVal + momVal+ random.randint(minVal, maxVal)
					discounted_price = float(total_price) - discount_price
					msg= "PromoCode Successfully Applied"
					promo_status = 1
				else:
					discount_price=0
					discounted_price= total_price
					msg= "PromoCode Can't be Applied"
					promo_status = 2

			resp = Response(json.dumps({"success": True, "total_discount":discount_price , "discounted_price":discounted_price, "promo_status": promo_status },ensure_ascii=False))
			resp.headers['Content-type']='application/json'
			return after_request(resp)

		else:
			resp = Response(json.dumps({"success": True, "total_discount":0, "promo_status": 4},ensure_ascii=False))
			resp.headers['Content-type']='application/json'
			return after_request(resp)


@app.route('/customer/get/customer/running/order/',methods=['GET','POST'])
def ApiGetRunningOrder():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile=user_data['mobile']
		order_info_data = dbhelper.GetData().OrderList2(mobile)
		order_info_data_db = []
		for line in order_info_data:
			order_info_data_dict = {}
			order_info_data_dict['id']=line[0]
			order_info_data_dict['orderId']=line[1]
			order_info_data_dict['name']=line[2]
			order_info_data_dict['mobile']=line[3]


			order_info_data_dict['location']=line[4]
			order_info_data_dict['latitude']=line[5]
			order_info_data_dict['longitude']=line[6]
			order_info_data_dict['mom_mobile']=line[7]
			order_info_data_dict['total_price']=line[8]


			order_info_data_dict['orderStatus']=line[9]


			order_info_data_dict['createdAt']=str(line[20])
			order_ist_time= (line[20]+ timedelta(hours=5, minutes=30))
			order_info_data_dict['createdAt']=str(order_ist_time)
			order_info_data_dict['deliver_number']= line[10]
			try:
				login_info_data= dbhelper.GetData().getDeliveryLogin(line[10])
				order_info_data_dict['deliverBoyName']=login_info_data[0][0]
			except:
				login_info_data= ''
				order_info_data_dict['deliverBoyName']=''

			order_info_data_dict['customerRating']= line[14]
			order_info_data_dict['ratingStatus']= line[19]
			order_info_data_dict['note']=line[17]
			checkStringLst= dbhelper.GetData().orderItemInfo(line[1])
			# checkStringLst= data[13].split(',')
			checkList=[]
			for check in checkStringLst:
				check_dict={}
				check_dict['food_item'] = check[2]
				check_dict['quantity'] = check[3]
				check_dict['itemId'] = check[4]
				check_dict['pType'] = check[5]
				check_dict['itemActualPrice'] = check[6]
				check_dict['image']= check[9]

				checkList.append(check_dict)

			order_info_data_dict['productList']=checkList
			order_info_data_db.append(order_info_data_dict)

		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/customer/cancel/order/',methods=['GET','POST'])
def CompleteCancelorder():
	if request.method == 'POST':
		order_info=json.loads(request.data)
		orderId = order_info['orderId']
		# order_status =dbhelper.GetData().getOrderStatus(orderId)[0][0]
		# if order_status==0:
		last=dbhelper.AddData().addCancelBooking(orderId)
		EditAssign = dbhelper.DeleteData().deleteorder(orderId)
		EditAccount = dbhelper.UpdateData().UpdateCancelOrder(orderId)
		response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId, "message":"This Order has been cancelled" }},ensure_ascii=False))
		return after_request(response)
		# else:
		# 	response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"This Order has not been cancelled"}}))
		# 	return after_request(response)





@app.route('/customer/get/new/order/list/',methods=['GET','POST'])
def ApiGetNewListOrder():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile=user_data['mobile']
		order_info_data = dbhelper.GetData().OrderList(mobile)
		order_info_data_db = []
		if(len(order_info_data))>0:
			for line in order_info_data:
				order_info_data_dict = {}
				order_info_data_dict['id']=line[0]
				order_info_data_dict['orderId']=line[1]
				order_info_data_dict['name']=line[2]
				order_info_data_dict['mobile']=line[3]

				if '\n' in line[4]:
					str_add= ' '.join(line[4].split('\n')[:2])
				else:
					str_add= line[4]
				order_info_data_dict['location']=str_add
				order_info_data_dict['latitude']=line[5]
				order_info_data_dict['longitude']=line[6]
				order_info_data_dict['mom_mobile']=line[7]
				order_info_data_dict['total_price']=line[8]
				order_info_data_dict['createdAt']=str(line[9])
				# database_datetime= datetime.strptime(line[9], "%d/%m/%Y %I %p")
				order_ist_time= (line[9]+ timedelta(hours=5, minutes=30))
				order_info_data_dict['createdAt']=str(order_ist_time)




				order_info_data_dict['firstName']=str(line[10])
				order_info_data_dict['middleName']=str(line[11])
				order_info_data_dict['lastName']=str(line[12])
				order_info_data_dict['image_name']=str(line[13])



				order_info_data_dict['note']=line[14]
				order_info_data_dict['mom_name']=str(line[10]) + str(line[11]) + str(line[12])

				checkStringLst= dbhelper.GetData().orderItemInfo(line[1])
				# checkStringLst= data[13].split(',')
				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['food_item'] = check[2]
					check_dict['quantity'] = check[3]
					check_dict['itemId'] = check[4]
					check_dict['pType'] = check[5]
					check_dict['itemActualPrice'] = check[6]
					check_dict['image']= check[9]

					checkList.append(check_dict)

				order_info_data_dict['productList']=checkList
				order_info_data_db.append(order_info_data_dict)
		print order_info_data_db
		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/customer/get/new/order/list/datewise/',methods=['GET','POST'])
def ApiGetNewListOrderDateWise():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile=user_data['mobile']
		start_date=user_data['start_date']
		end_date=user_data['end_date']
		print start_date, end_date
		start_date = datetime.strptime(start_date, '%d/%m/%Y')
		end_date = datetime.strptime(end_date, '%d/%m/%Y')
		order_info_data = dbhelper.GetData().OrderListDateWise(mobile, start_date, end_date)
		order_info_data_db = []
		if(len(order_info_data))>0:
			for line in order_info_data:


				order_info_data_dict = {}
				order_info_data_dict['id']=line[0]
				order_info_data_dict['orderId']=line[1]
				order_info_data_dict['name']=line[2]
				order_info_data_dict['mobile']=line[3]

				if '\n' in line[4]:
					str_add = ' '.join(line[4].split('\n')[:2])
				else:
					str_add = line[4]

				order_info_data_dict['location']= str_add
				order_info_data_dict['latitude']=line[5]
				order_info_data_dict['longitude']=line[6]
				order_info_data_dict['mom_mobile']=line[7]
				order_info_data_dict['total_price']=line[8]


				order_ist_time= (line[9]+ timedelta(hours=5, minutes=30))
				order_info_data_dict['createdAt']=str(order_ist_time)

				order_info_data_dict['firstName']=str(line[10])
				order_info_data_dict['middleName']=str(line[11])
				order_info_data_dict['lastName']=str(line[12])
				order_info_data_dict['image_name']=str(line[13])



				order_info_data_dict['note']=line[14]

				checkStringLst= dbhelper.GetData().orderItemInfo(line[1])
				# checkStringLst= data[13].split(',')
				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['food_item'] = check[2]
					check_dict['quantity'] = check[3]
					check_dict['itemId'] = check[4]
					check_dict['pType'] = check[5]
					check_dict['itemActualPrice'] = check[6]
					check_dict['image']= check[9]

					checkList.append(check_dict)

				order_info_data_dict['productList']=checkList
				order_info_data_db.append(order_info_data_dict)
		print order_info_data_db
		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/customer/get/complete/order/list/',methods=['GET','POST'])
def ApiGetNewComOrder():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile=user_data['mobile']
		order_info_data = dbhelper.GetData().ComOrderList(mobile)
		order_info_data_db = []
		if(len(order_info_data))>0:
			for line in order_info_data:
				order_info_data_dict = {}
				order_info_data_dict['id']=line[0]
				order_info_data_dict['orderId']=line[1]
				order_info_data_dict['name']=line[2]
				order_info_data_dict['mobile']=line[3]

				if '\n' in line[4]:
					str_add = ' '.join(line[4].split('\n')[:2])
				else:
					str_add = line[4]
				order_info_data_dict['location']=line[4]
				order_info_data_dict['latitude']=line[5]
				order_info_data_dict['longitude']=line[6]
				order_info_data_dict['mom_mobile']=line[7]
				order_info_data_dict['total_price']=line[8]


				order_info_data_dict['orderStatus']=line[9]




				order_ist_time= (line[20]+ timedelta(hours=5, minutes=30))
				order_info_data_dict['createdAt']=str(order_ist_time)

				order_info_data_dict['customerRating']= line[14]
				order_info_data_dict['ratingStatus']= line[19]
				order_info_data_dict['note']=line[17]
				try:
					mom_data= dbhelper.GetData().GetPartnerName(line[7])
					mom_name = str(mom_data[0][0])+str(mom_data[0][1])+str(mom_data[0][2])
					momId = mom_data[0][4]

				except:
					mom_name=''
					momId =''

				order_info_data_dict['deliver_number']= line[10]
				try:
					delivery_name= dbhelper.GetData().GetDeliveryName(line[10])[0][0]
				except:
					delivery_name=''
				order_info_data_dict['delivery_name']=delivery_name


				order_info_data_dict['mom_name']=mom_name
				order_info_data_dict['momId']=momId
				# order_info_data_dict['favourate']= line[25]
				checkStringLst= dbhelper.GetData().orderItemInfo(line[1])
				# checkStringLst= data[13].split(',')
				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['food_item'] = check[2]
					check_dict['quantity'] = check[3]
					check_dict['itemId'] = check[4]
					check_dict['pType'] = check[5]
					check_dict['itemActualPrice'] = check[6]
					check_dict['image']= check[9]

					checkList.append(check_dict)

				order_info_data_dict['productList']=checkList
				order_info_data_db.append(order_info_data_dict)

		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/customer/get/complete/order/list/datewise/',methods=['GET','POST'])
def ApiGetNewComOrderDateWise():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile=user_data['mobile']
		start_date=user_data['start_date']
		end_date=user_data['end_date']

		print start_date, end_date
		start_date = datetime.strptime(start_date, '%d/%m/%Y') - timedelta(hours=5, minutes=30)
		end_date = datetime.strptime(end_date, '%d/%m/%Y') + timedelta(hours=18, minutes=30)

		order_info_data = dbhelper.GetData().ComOrderListDateWsie(mobile, start_date, end_date)
		order_info_data_db = []
		if(len(order_info_data))>0:
			for line in order_info_data:
				order_info_data_dict = {}
				order_info_data_dict['id']=line[0]
				order_info_data_dict['orderId']=line[1]
				order_info_data_dict['name']=line[2]
				order_info_data_dict['mobile']=line[3]


				order_info_data_dict['location']=line[4]
				order_info_data_dict['latitude']=line[5]
				order_info_data_dict['longitude']=line[6]
				order_info_data_dict['mom_mobile']=line[7]
				order_info_data_dict['total_price']=line[8]


				order_info_data_dict['orderStatus']=line[9]
				order_info_data_dict['deliver_number']= line[10]


				# order_info_data_dict['createdAt']=str(line[11])

				order_ist_time= (line[11]+ timedelta(hours=5, minutes=30))
				order_info_data_dict['createdAt']=str(order_ist_time)


				order_info_data_dict['customerRating']= line[12]
				order_info_data_dict['ratingStatus']= line[13]
				order_info_data_dict['note']=line[14]

				mom_name = str(line[15])+str(line[16])+str(line[17])
				momId = line[18]

				order_info_data_dict['delivery_name']=line[20]


				order_info_data_dict['mom_name']=mom_name
				order_info_data_dict['momId']=momId
				order_info_data_dict['mom_image']=line[19]
				# order_info_data_dict['favourate']= line[25]
				checkStringLst= dbhelper.GetData().orderItemInfo(line[1])
				# checkStringLst= data[13].split(',')
				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['food_item'] = check[2]
					check_dict['quantity'] = check[3]
					check_dict['itemId'] = check[4]
					check_dict['pType'] = check[5]
					check_dict['itemActualPrice'] = check[6]
					check_dict['image']= check[9]

					checkList.append(check_dict)

				order_info_data_dict['productList']=checkList
				order_info_data_db.append(order_info_data_dict)

		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# @app.route('/customer/get/cancel/order/list/',methods=['GET','POST'])
# def ApiGetNewCancelOrder():
# 	if request.method=='POST':
#
# 		order_info_data = dbhelper.GetData().ComCancelOrderList()
# 		order_info_data_db = []
# 		if(len(order_info_data))>0:
# 			for line in order_info_data:
# 				order_info_data_dict = {}
# 				order_info_data_dict['id']=line[0]
# 				order_info_data_dict['name']=line[1]
# 				order_info_data_dict['location']=line[2]
# 				order_info_data_dict['price']=line[3]
# 				order_info_data_dict['mobile']=line[4]
# 				order_info_data_dict['total_price']=line[5]
# 				order_info_data_dict['latitude']=line[6]
# 				order_info_data_dict['longitude']=line[7]
# 				order_info_data_dict['mom_mobile']=line[13]
# 				try:
# 					mom_data= dbhelper.GetData().GetPartnerName(line[13])
# 					mom_name = str(mom_data[0][0])+str(mom_data[0][1])+str(mom_data[0][2])
#
# 				except:
# 					mom_name=''
# 				order_info_data_dict['mom_name']=mom_name
# 				order_info_data_dict['orderStatus']=line[14]
# 				try:
# 					momId= dbhelper.GetData().GetMomnameId(line[13])[0][0]
# 				except:
# 					momId=''
# 				order_info_data_dict['orderId']=line[15]
# 				order_info_data_dict['momId']=momId
#
# 				order_info_data_dict['createdAt']=str(line[16])
# 				order_info_data_dict['deliver_number']= line[17]
# 				try:
# 					delivery_name= dbhelper.GetData().GetDeliveryName(line[17])[0][0]
# 				except:
# 					delivery_name=''
# 				order_info_data_dict['delivery_name']=delivery_name
# 				order_info_data_dict['customerRating']= line[21]
# 				order_info_data_dict['ratingStatus']= line[23]
# 				order_info_data_dict['image']= line[26]
# 				order_info_data_dict['note']= line[27]
# 				# order_info_data_dict['favourate']= line[25]
# 				checkStringLst= dbhelper.GetData().ComOrder_List(line[15])
# 				# checkStringLst= data[13].split(',')
# 				checkList=[]
# 				for check in checkStringLst:
# 					check_dict={}
# 					check_dict['food_item'] = check[0]
# 					check_dict['quantity'] = check[1]
# 					check_dict['itemId'] = check[2]
# 					check_dict['pType'] = check[3]
# 					check_dict['itemActualPrice'] = check[4]
# 					check_dict['itemDescription'] = check[6]
# 					check_dict['image'] = check[7]
#
# 					checkList.append(check_dict)
#
# 				order_info_data_dict['productList']=checkList
# 				order_info_data_db.append(order_info_data_dict)
#
# 		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db }))
# 		resp.headers['Content-type']='application/json'
# 		return after_request(resp)


@app.route('/api/get/user/report/',methods=['GET','POST'])
def APiGetuserReport():
	if request.method=='POST':
		user_data = dbhelper.GetData().getUserreport()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['name']  = line[1]
				user_data_dict['email']  = line[2]
				user_data_dict['mobile']  = line[3]
				user_data_dict['status'] = line[4]

				user_data_db.append(user_data_dict)
		resp = Response(json.dumps({"success": True, "user_data": user_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/customer/get/delivery/charge/cal/',methods=['GET','POST'])
def APIGetCharge():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mom_lat=user_data['mom_lat']
		mom_lang=user_data['mom_lang']
		delivery_lat=user_data['delivery_lat']
		delivery_lang=user_data['delivery_lang']
		delivery_dist = user_data['distance']

		if float(delivery_dist) <=1:
			delivery_charge = 25
		elif float(delivery_dist) <=3:
			delivery_charge = 28

		elif float(delivery_dist) <=6:
			delivery_charge = 32
		else:
			delivery_charge = 0


		resp = Response(json.dumps({"success": True, "delivery_charge": delivery_charge },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/customer/latest/app/version/',methods=['GET','POST'])
def APiCustomerVersion():
	if request.method=='POST':
		app_data = dbhelper.GetData().getCustomerVersion()
		app_data_db=[]

		for line in app_data:
			app_data_dict={}
			app_data_dict['id']                                = line[0]
			app_data_dict['appName']                           = line[1]
			app_data_dict['version']                           = line[2]
			app_data_dict['versionCode']                       = line[3]
			app_data_dict['flag']							= line[4]
			app_data_dict['updateOn']                          = str(line[5])
			app_data_dict['momCheffVersion'] = line[6]

			app_data_db.append(app_data_dict)

		resp = Response(json.dumps({"success": True, "app_data": app_data_db },ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/customer/get/vendor/search/list/',methods=['GET','POST'])
def ApiGetVendorListWebListTab():
	if request.method=='POST':
		vendor_data =json.loads(request.data)
		strDate = str(date.today())
		dateNow= datetime.strptime(strDate, "%Y-%m-%d").strftime("%d/%m/%Y")
		Lat=vendor_data['latitude']
		Lang =vendor_data['longitude']

		vendor_info_data = dbhelper.GetData().VendorDataListSearchLst(Lat,Lang)
		vendor_info_data_db = []
		vendor_dict ={}

		vendor_list_with_menu = []
		vendor_added = {}
		print vendor_info_data
		if(len(vendor_info_data))>0:
			for line in vendor_info_data:
				print line[4]
				if line[5] not in vendor_added:
					vendor_info_data_dict = {}
					vendor_info_data_dict['id']=line[0]
					vendor_info_data_dict['flag']=0
					vendor_info_data_dict['fisrtName']=line[1]
					vendor_info_data_dict['lastName']=line[2]
					vendor_info_data_dict['middleName']=line[3]
					vendor_info_data_dict['email']=line[4]
					vendor_info_data_dict['mobile']=line[5]
					vendor_info_data_dict['promocode']  = ''
					vendor_info_data_dict['address']=line[6]
					vendor_info_data_dict['country']=line[7]
					vendor_info_data_dict['state']=line[8]
					vendor_info_data_dict['zipCode']=line[9]
					vendor_info_data_dict['foodLicenseNo']=line[10]
					vendor_info_data_dict['dob']=line[11]
					vendor_info_data_dict['specialization']=line[12]
					vendor_info_data_dict['comment']=line[13]
					vendor_info_data_dict['openTime']=line[14]
					vendor_info_data_dict['endTime']=line[15]
					vendor_info_data_dict['breakStart']=line[16]
					vendor_info_data_dict['breakEnd']=line[17]
					vendor_info_data_dict['profileStatus']=line[18]
					vendor_info_data_dict['image_name']=line[19]
					vendor_info_data_dict['latitude']=line[20]
					vendor_info_data_dict['rating']='4.5'
					vendor_info_data_dict['longitude']=line[21]
					vendor_info_data_dict['image']=line[22]
					vendor_info_data_dict['description']=line[23]
					vendor_info_data_dict['onlineStatus']=line[24]
					try:
						tDist = haversine(float(Lat),float(Lang),float(line[20]),float(line[21]))
					except:
						tDist = 0
					try:
						vendor_info_data_dict['estimateTime']=int(float(tDist)/8 *60)
					except:
						vendor_info_data_dict['estimateTime']=0


					vendor_info_data_dict["menuList"] = []
					menu_info_data_dict = {}
					menu_info_data_dict['food_type'] = line[26]
					menu_info_data_dict['itemName'] = line[27]
					menu_info_data_dict['itemDescription'] = line[28]
					menu_info_data_dict['itemGroup'] = line[29]

					if float(line[30]) > 100:
						fullPrice = float(line[30]) + float(70)
						print fullPrice
					else:
						fullPrice = float(line[30]) * float(0.25) + float(10) + float(line[30])
						print fullPrice
					menu_info_data_dict['item_image'] = line[31]
					menu_info_data_dict['fullPrice'] = fullPrice
					menu_info_data_dict['itemPreparationTime'] = line[32]
					vendor_info_data_dict["menuList"].append(menu_info_data_dict)
					vendor_info_data_db.append(vendor_info_data_dict)
					vendor_added[line[5]] = vendor_info_data_dict
				else:
					vendor = vendor_added[line[5]]
					menu_info_data_dict = {}
					menu_info_data_dict['food_type'] = line[26]
					menu_info_data_dict['itemName'] = line[27]
					menu_info_data_dict['itemDescription'] = line[28]
					menu_info_data_dict['itemGroup'] = line[29]

					if float(line[30]) > 100:
						fullPrice = float(line[30]) + float(70)
						print fullPrice
					else:
						fullPrice = float(line[30]) * float(0.25) + float(10) + float(line[30])
						print fullPrice
					menu_info_data_dict['item_image'] = line[31]
					menu_info_data_dict['fullPrice'] = fullPrice
					menu_info_data_dict['itemPreparationTime'] = line[32]
					vendor["menuList"].append(menu_info_data_dict)

		resp = Response(json.dumps({"success": True, "vendor_data": vendor_info_data_db ,"position":0},ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		print resp
		return after_request(resp)

@app.route('/customer/get/vendor/search/keyword/',methods=['GET','POST'])
def ApiGetVendorListWebListTabKeywords():
	if request.method=='POST':
		vendor_data =json.loads(request.data)
		Lat=vendor_data['latitude']
		Lang =vendor_data['longitude']
		keyword =vendor_data['key']

		vendor_info_data = dbhelper.GetData().VendorDataListSearchLstSearch(Lat,Lang,keyword)
		vendor_info_data_db = []
		vendor_dict ={}

		vendor_list_with_menu = []
		vendor_added = {}
		if(len(vendor_info_data))>0:
			for line in vendor_info_data:
				if line[5] not in vendor_added:
					vendor_info_data_dict = {}
					vendor_info_data_dict['id']=line[0]
					vendor_info_data_dict['flag']=0
					vendor_info_data_dict['fisrtName']=line[1]
					vendor_info_data_dict['lastName']=line[2]
					vendor_info_data_dict['middleName']=line[3]
					vendor_info_data_dict['email']=line[4]
					vendor_info_data_dict['mobile']=line[5]
					vendor_info_data_dict['promocode']  = ''
					vendor_info_data_dict['address']=line[6]
					vendor_info_data_dict['country']=line[7]
					vendor_info_data_dict['state']=line[8]
					vendor_info_data_dict['zipCode']=line[9]
					vendor_info_data_dict['foodLicenseNo']=line[10]
					vendor_info_data_dict['dob']=line[11]
					vendor_info_data_dict['specialization']=line[12]
					vendor_info_data_dict['comment']=line[13]
					vendor_info_data_dict['openTime']=line[14]
					vendor_info_data_dict['endTime']=line[15]
					vendor_info_data_dict['breakStart']=line[16]
					vendor_info_data_dict['breakEnd']=line[17]
					vendor_info_data_dict['profileStatus']=line[18]
					vendor_info_data_dict['image_name']=line[19]
					vendor_info_data_dict['latitude']=line[20]
					vendor_info_data_dict['rating']='4.5'
					vendor_info_data_dict['longitude']=line[21]
					vendor_info_data_dict['image']=line[22]
					vendor_info_data_dict['description']=line[23]
					vendor_info_data_dict['onlineStatus']=line[24]
					try:
						tDist = haversine(float(Lat),float(Lang),float(line[20]),float(line[21]))
					except:
						tDist = 0
					try:
						vendor_info_data_dict['estimateTime']=int(float(tDist)/8 *60)
					except:
						vendor_info_data_dict['estimateTime']=0


					vendor_info_data_dict["menuList"] = []
					menu_info_data_dict = {}
					menu_info_data_dict['food_type'] = line[26]
					menu_info_data_dict['itemName'] = line[27]
					menu_info_data_dict['itemDescription'] = line[28]
					menu_info_data_dict['itemGroup'] = line[29]

					if float(line[30]) > 100:
						fullPrice = float(line[30]) + float(70)
						print fullPrice
					else:
						fullPrice = float(line[30]) * float(0.25) + float(10) + float(line[30])
						print fullPrice
					menu_info_data_dict['item_image'] = line[31]
					menu_info_data_dict['fullPrice'] = fullPrice
					menu_info_data_dict['itemPreparationTime'] = line[32]
					vendor_info_data_dict["menuList"].append(menu_info_data_dict)
					vendor_info_data_db.append(vendor_info_data_dict)
					vendor_added[line[5]] = vendor_info_data_dict
				else:
					vendor = vendor_added[line[5]]
					menu_info_data_dict = {}
					menu_info_data_dict['food_type'] = line[26]
					menu_info_data_dict['itemName'] = line[27]
					menu_info_data_dict['itemDescription'] = line[28]
					menu_info_data_dict['itemGroup'] = line[29]

					if float(line[30]) > 100:
						fullPrice = float(line[30]) + float(70)
						print fullPrice
					else:
						fullPrice = float(line[30]) * float(0.25) + float(10) + float(line[30])
						print fullPrice
					menu_info_data_dict['item_image'] = line[31]
					menu_info_data_dict['fullPrice'] = fullPrice
					menu_info_data_dict['itemPreparationTime'] = line[32]
					vendor["menuList"].append(menu_info_data_dict)

		resp = Response(json.dumps({"success": True, "vendor_data": vendor_info_data_db ,"position":0},ensure_ascii=False))
		resp.headers['Content-type']='application/json'
		return after_request(resp)
