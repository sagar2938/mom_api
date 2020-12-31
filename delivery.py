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
import deliverCloudDbHandler as dbhelper
from sets import  Set
import unicodedata
import urllib
import urllib2
from datetime import date, timedelta
# from datetime import datetime
import googleapiclient.discovery
import googleapiclient.http
from google.appengine.api import urlfetch
from datetime import timedelta, date, datetime
from time import gmtime, strftime,time,localtime


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

@app.route('/delivery/login/', methods=['GET','POST'])
def ApiDeliveryLogin():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = user_data['otp']
		login_info_data= dbhelper.GetData().getDeliveryLogin(mobile)
		login_info_data_db = []
		if(len(login_info_data))>0:
			for line in login_info_data:
				login_info_data_dict = {}
				login_info_data_dict['name'] =line[0]
				login_info_data_dict['mobile'] =line[1]
				login_info_data_dict['address'] =line[2]
				login_info_data_dict['driveringLicense']  =line[3]
				login_info_data_dict['aadharNo']=line[4]
				login_info_data_dict['vehicleNo']=line[5]
				login_info_data_dict['companyName']=line[6]
				login_info_data_dict['companyId']=line[7]
				login_info_data_dict['image']=''

				login_info_data_db.append(login_info_data_dict)
				text =" Welcome +to + Mother + on + Mission. Your + Login + OTP + is %s."%(str(otp))
				url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
				urlfetch.set_default_fetch_deadline(45)
				resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
				db={'message':'User Exist',"confirmation":1,"otp":otp,"user_data":login_info_data_db}
		else:
			db={'message': 'User Not Exist', "confirmation":0}
		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/delivery/live/location/', methods=['GET', 'POST'])
def AddLiveLocationByEmpCode():
	if request.method == 'POST':
		try:
			location_data=json.loads(request.data)
			mobile = location_data['mobile']
			lastUpdate = location_data['lastUpdate']
			lat = location_data['lat']
			longitude= location_data['long']
			try:
				loc_url = 'https://locationapi-100.appspot.com/location/reverse?lat='+str(lat)+'&lon='+str(longitude)
				address = json.loads(urllib2.urlopen(urllib2.Request(loc_url)).read())
				print address
				formatted_address = address['display_name']
			except:
				formatted_address=""

			CheckLocation       = dbhelper.GetData().getCheckLocation(mobile)

			if CheckLocation==True:
				updateLocation=dbhelper.UpdateData().updateLiveLocation(mobile,lastUpdate,lat,longitude,formatted_address)

			else:
				addLiveLocation = dbhelper.AddData().addLiveLocationEmp(mobile, lastUpdate, lat, longitude, formatted_address)
		except:
			msg="Try Again"
		resp = Response(json.dumps({"success": True, "Msg": "Successfuly Added" }))
		return after_request(resp)

@app.route('/delivery/partner/addtoken/', methods=['GET','POST'])
def fcmAuthPartner():
	if request.method       == 'POST':
		token_data          =json.loads(request.data)
		mobile             =token_data['mobile']
		fcmToken           =token_data['fcmToken']

		last                =dbhelper.AddData().addDeliveryToken(mobile,fcmToken)
		if last:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/delivery/partner/online/status/', methods=['GET','POST'])
def StatusPartner():
	if request.method       == 'POST':
		live_location      =json.loads(request.data)
		mobile             =live_location['mobile']
		timeStamp          =live_location['timeStamp']
		status             =live_location['status']
		out                  =dbhelper.UpdateData().updateOnlineStatus(mobile,timeStamp,status)

		db={'message':'Status Added',"confirmation":1}


		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/delivery/get/deliver/status/', methods=['GET','POST'])
def StatusPartnerGet():
	if request.method       == 'POST':
		live_location      =json.loads(request.data)
		mobile             =live_location['mobile']
		out = dbhelper.GetData().getOnlineStatus(mobile)
		if out[0][0]=="True":
			db={'message':'Status Online',"confirmation":1}
		else:
			db={'message': 'Status offline', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


@app.route('/delivery/get/new/order/list/',methods=['GET','POST'])
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
				order_info_data_dict['location']=line[4]
				order_info_data_dict['latitude']=line[5]
				order_info_data_dict['longitude']=line[6]
				order_info_data_dict['mom_mobile']=line[7]
				order_info_data_dict['total_price']=line[8]
				# order_info_data_dict['createdAt']=str(line[9])
				order_ist_time= (line[9]+ timedelta(hours=5, minutes=30))
				order_info_data_dict['createdAt']=str(order_ist_time)
				order_info_data_dict['firstName']=line[10]
				order_info_data_dict['middleName']=line[11]
				order_info_data_dict['lastName']=line[12]
				order_info_data_dict['image_name']=line[13]
				order_info_data_dict['note']=line[14]
				order_info_data_dict['mom_firstName']=line[15]
				order_info_data_dict['mom_latitude']=line[16]
				order_info_data_dict['mom_longitude']=line[17]
				order_info_data_dict['mom_code']=line[18]
				order_info_data_dict['mom_address']=line[19]

				checkStringLst= dbhelper.GetData().orderItemInfo(line[1])

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

		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/delivery/get/complete/order/list/',methods=['GET','POST'])
def ApiGetNewComOrderdelivery():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile=user_data['mobile']
		order_info_data = dbhelper.GetData().ComOrderListDelivery(mobile)
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

				try:
					image_name= dbhelper.GetData().MomProfile(line[7])[0][0]
				except:
					image_name=""
				order_info_data_dict['image_name']=image_name
				order_info_data_dict['orderStatus']=line[9]

				order_info_data_dict['deliver_number']= line[10]
				order_info_data_dict['delivery_latitute']= line[11]
				order_info_data_dict['delivery_longitude']= line[12]
				order_info_data_dict['customerRating']= line[14]
				order_info_data_dict['deliveryRating']= line[15]
				order_info_data_dict['note']= line[17]
				order_info_data_dict['ratingStatus']= line[19]

				# order_info_data_dict['createdAt']=str(line[20])
				order_ist_time= (line[20]+ timedelta(hours=5, minutes=30))
				order_info_data_dict['createdAt']=str(order_ist_time)
				checkStringLst= dbhelper.GetData().orderItemInfo(line[1])

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

		resp = Response(json.dumps({"success": True, "order_data": order_info_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)
