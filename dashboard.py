# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json, urllib2, logging
import dashboardCloudDbHandler as dbhelper
import datetime
import json
import StringIO

import mailhandler
import random
from math import radians, cos, sin, asin, sqrt
import math
import ast
from time import gmtime, strftime

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

@app.route('/dashboard/get/order/iteminfo/',methods=['GET','POST'])
def ApiItemInfoDashboard():
	if request.method=='POST':
		orderInfo =json.loads(request.data)
		orderId = orderInfo['orderId']
		# order_info_data = dbhelper.GetData().getOrderItemInfo(orderId)
		checkStringLst= dbhelper.GetData().orderItemInfo(orderId)

		checkList=[]
		for check in checkStringLst:
			check_dict={}
			check_dict['orderId'] = check[1]
			check_dict['food_item'] = check[2]
			check_dict['quantity'] = check[3]
			check_dict['itemId'] = check[4]
			check_dict['pType'] = check[5]
			check_dict['itemActualPrice'] = check[6]
			check_dict['image']= check[9]
			checkList.append(check_dict)
		resp = Response(json.dumps({"success": True, "orderItem_list": checkList }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/dashboard/get/new/order/',methods=['GET','POST'])
def ApiGetNewListWebDashboard():
	if request.method=='POST':
		order_info_data = dbhelper.GetData().OrderListWebDash()
		order_info_data_db = []
		if(len(order_info_data))>0:
			for line in order_info_data:
				order_info_data_dict = {}

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

				order_info_data_dict['firstName']=str(line[10])
				order_info_data_dict['middleName']=str(line[11])
				order_info_data_dict['lastName']=str(line[12])
				order_info_data_dict['image_name']=str(line[13])
				order_info_data_dict['note']=line[14]
				order_info_data_dict['orderStatus']=line[15]

				try:
					mom_name = dbhelper.GetData().getVendorLoginStatus(line[7])
					vendor_name=str(mom_name[0][0])+str(mom_name[0][2])
				except:
					vendor_name=''
				order_info_data_dict['vendor_name']=vendor_name
				# order_info_data_dict['promoCode']=line[17]
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

@app.route('/dashboard/get/complete/order/list/total/',methods=['GET','POST'])
def ApiGetNewComOrderTotal():
	if request.method=='POST':
		order_info_data = dbhelper.GetData().getCompleteOrderInfo()
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


				image_nam= dbhelper.GetData().MomProfile(line[7])
				if len(image_nam)>0:
					image_name= image_nam[0][0]
					mom_name= image_nam[0][1]+" "+ image_nam[0][2]
					order_info_data_dict['image_name']=image_name
					order_info_data_dict['mom_name']=mom_name
				else:
					order_info_data_dict['image_name']=""
					order_info_data_dict['mom_name']=""
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


@app.route('/dashboard/delivery/edit/', methods=['GET','POST'])
def apiDeliveryEdit():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		name = user_data['name']
		address = user_data['address']
		driveringLicense = user_data['driveringLicense']
		aadharNo = user_data['aadharNo']
		vehicleNo = user_data['vehicleNo']
		companyName = user_data['companyName']
		image = user_data['image']

		updateDelivery = dbhelper.UpdateData().updateDeliveryBoy(mobile, name, address, driveringLicense, aadharNo, vehicleNo, companyName, image)

		db={'message': 'User updated Successfully', "confirmation": 1}
		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)
