# -*- coding: utf-8 -*-
from flask import Flask, request, Response, redirect
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
import cloudDbHandler as dbhelper
from sets import  Set
import unicodedata
import urllib
import urllib2
from datetime import date, timedelta, datetime


import googleapiclient.discovery
import googleapiclient.http
from google.appengine.api import urlfetch
from datetime import timedelta, date, datetime
from time import gmtime, strftime,time,localtime
import re
import CheckSumParser

app = Flask(__name__)

############################   Normal Function To calculate the Details   ###################################################

API_KEY = ['NkHb13BxRBiZ0JSyxLbAU','Hx1XU63ZThyFGsqfLeGu7']

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def sendActivationMsg(mobile):
    text ="Your+Profile+ has+ been+ approved+ by+ the+ Admin!+ Welcome+ to+ the+ Family."
    url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
    urlfetch.set_default_fetch_deadline(45)
    resp = urlfetch.fetch(url=url,
        method=urlfetch.GET,
        headers={'Content-Type': 'text/html'})

def sendDeActivationMsg(mobile):
    text ="Your+ Profile+ has+ been+ deactivated+ by+ the+ Admin!+ Please+ contact+ administration."
    url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
    urlfetch.set_default_fetch_deadline(45)
    resp = urlfetch.fetch(url=url,
        method=urlfetch.GET,
        headers={'Content-Type': 'text/html'})



def wordCleaner(words):
    second_name = words.replace('\u0130','')
    clean_w = re.sub('[^0-9a-zA-Z ]+', '', second_name)
    return clean_w

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


@app.route('/api/user/login/', methods=['GET','POST'])
def ApiUserLogin():
    if request.method  == 'POST':
        user_data =json.loads(request.data)
        mobile = user_data['mobile']
        otp  = user_data['otp']
        User= dbhelper.GetData().getUserLoginStatus(mobile)
        if len(User)>0:
            name = User[0][0]
            mobile=User[0][1]
            print otp
            text ="Your + verification+ code +is %s ."%(str(otp))
            url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
            urlfetch.set_default_fetch_deadline(45)
            resp = urlfetch.fetch(url=url,
                method=urlfetch.GET,
                headers={'Content-Type': 'text/html'})
            db={'message':'User Exist',"confirmation":1,"otp":otp}
        else:
            db={'message': 'User Not Exist', "confirmation":0}

        resp = Response(json.dumps({ "response": db}))
        return after_request(resp)


@app.route('/api/send/link/', methods=['GET','POST'])
def ApiSendLink():
    if request.method  == 'POST':
        user_data =json.loads(request.data)
        mobile = user_data['mobile']


        text ="Mother+on+Mission+Download+Our+App + https://play.google.com/store/apps/details?id=mom.com&hl=en."
        url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
        print url
        urlfetch.set_default_fetch_deadline(45)
        resp = urlfetch.fetch(url=url,
            method=urlfetch.GET,
            headers={'Content-Type': 'text/html'})
        db={'message':'Link Send',"confirmation":1}

        resp = Response(json.dumps({ "response": db}))
        return after_request(resp)

@app.route('/api/vendor/login/', methods=['GET','POST'])
def ApiVendorLogin():
    if request.method  == 'POST':
        user_data =json.loads(request.data)
        mobile = user_data['mobile']
        otp  = user_data['otp']
        login_info_data= dbhelper.GetData().getVendorLoginStatus(mobile)
        login_info_data_db = []
        if(len(login_info_data))>0:
            for line in login_info_data:
                login_info_data_dict = {}
                login_info_data_dict['firstName'] =line[0]
                login_info_data_dict['middleName'] =line[1]
                login_info_data_dict['lastName'] =line[2]
                login_info_data_dict['mobile']  =line[3]
                login_info_data_dict['profileStatus']=line[4]
                login_info_data_dict['email']=line[5]
                login_info_data_dict['image_name']=line[6]
                login_info_data_dict['status']=line[7]
                if line[7] ==1:
                    try:
                        text =" Welcome +to + Mother + on + Mission. Your + Login + OTP + is %s."%(str(otp))
                        url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
                        urlfetch.set_default_fetch_deadline(45)
                        resp = urlfetch.fetch(url=url,
                            method=urlfetch.GET,
                            headers={'Content-Type': 'text/html'})
                    except:
                        pass
                else:
                    pass

                login_info_data_db.append(login_info_data_dict)

                db={'message':'User Exist',"confirmation":1,"otp":otp,"user_data":login_info_data_db}
        else:
            db={'message': 'User Not Exist', "confirmation":0}
        resp = Response(json.dumps({ "response": db}))
        return after_request(resp)

@app.route('/api/add/user/',methods=['GET','POST'])
def APiadduser():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        name= userInfo['name']
        email = userInfo['email']
        mobile = userInfo['mobile']
        otp      = userInfo['otp']
        user_status =dbhelper.GetData().getUserStatus(mobile)
        if user_status==True:
            db={'message':'User Already Exist',"confirmation":0}
            resp = Response(json.dumps({"response": db}))
            return after_request(resp)
        else:
            AddUser = dbhelper.AddData().addUser(name,email,mobile)
            db={'message':'User Added',"confirmation":1,"mobile":mobile,"name":name,"email":email,"otp":otp}
            text =" Welcome+to+Mothers+On+Mission. Your+Login+OTP+is+ %s."%(str(otp))
            url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
            urlfetch.set_default_fetch_deadline(45)
            resp = urlfetch.fetch(url=url,
                method=urlfetch.GET,
                headers={'Content-Type': 'text/html'})
            resp = Response(json.dumps({"response":"success"}))
            return after_request(resp)

@app.route('/api/resend/otp/', methods=['GET','POST'])
def AddResendOtp():
    if request.method       == 'POST':
        user_data           =json.loads(request.data)
        mobile              = user_data['mobile']
        otp                = user_data['otp']


        text ='MOMApp+Your+verification+code+is +%s'%(str(otp))

        url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)

        urlfetch.set_default_fetch_deadline(45)
        resp = urlfetch.fetch(url=url,
            method=urlfetch.GET,
            headers={'Content-Type': 'text/html'})
        resp = Response(json.dumps({ "response": "success"}))
        return after_request(resp)

@app.route('/api/add/vendor/',methods=['GET','POST'])
def APiaddvendor():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        firstName= userInfo['firstName']
        middleName = userInfo['middleName']
        lastName = userInfo['lastName']
        email      = userInfo['email']
        mobile = userInfo['mobile']
        image_name = userInfo['image_name']
        about_mom = userInfo['about_mom']
        user_status =dbhelper.GetData().getUserStatus2(mobile)
        if user_status==True:
            db={'message':'User Already Exist',"confirmation":0}
            resp = Response(json.dumps({"response": db}))
            return after_request(resp)
        else:
            lastId           =dbhelper.GetData().getLastID()[0][0]
            if lastId:
                newid=str(1+lastId)
            else:
                newid=str(1)

            venor_code = 'MOMVNDR' + newid
            AddUser = dbhelper.AddData().addUser2(firstName,middleName,lastName,email,mobile,image_name,venor_code,about_mom)
            db={'message':'User Added',"confirmation":1,"mobile":mobile,"firstName":firstName,"email":email,"middleName":middleName,"lastName":lastName}
            # text =" Welcome to Mothers On Mission. Your Login OTP is %s."%(str(otp))

            # url ='http://bhashsms.com/api/sendmsg.php?user=mom123&pass=123456&sender=mother&phone=%s&text=%s&priority=ndnd&stype=normal'%(str(mobile),text)

            # urlfetch.set_default_fetch_deadline(45)
            # resp = urlfetch.fetch(url=url,
            # 	method=urlfetch.GET,
            # 	headers={'Content-Type': 'text/html'})
            db={'message':'User Added',"confirmation":1}
            resp = Response(json.dumps({"response":db}))
            return after_request(resp)


@app.route('/api/admin/post/login/',methods=['GET','POST'])
def ApiAdminLoginData():
    if request.method=='POST':
        configure_data = json.loads(request.data)
        username = configure_data['json_data']['username']
        password= configure_data['json_data']['password']
        login_info_data = dbhelper.GetData().PostAdmintLoginData(username)
        login_info_data_db = []
        if(len(login_info_data))>0:
            for line in login_info_data:
                login_info_data_dict = {}
                login_info_data_dict['id'] =line[0]
                login_info_data_dict['password'] =line[1]
                login_info_data_dict['username'] =line[2]
                login_info_data_dict['name']  =line[3]
                # login_info_data_dict['user_type']=line[4]
                login_info_data_dict['status']=1

                login_info_data_db.append(login_info_data_dict)
        else:
            resp = Response(json.dumps({"success": 0}))
        if(password==login_info_data[0][1]):
            resp = Response(json.dumps({"success": 1, "configure_data":login_info_data[0], "datasets":login_info_data_db}))
        else:
            resp = Response(json.dumps({"success": 0}))
        resp.headers['Content-type']='application/json'
        return after_request(resp)


# Add Menu
@app.route('/api/add/vendor/menu/',methods=['GET','POST'])
def APiVendorMenu():
    if request.method=='POST':
        menuInfo   = json.loads(request.data)
        mobile  = menuInfo['mobile']
        food_type= menuInfo['food_type']
        itemName  = menuInfo['itemName']
        itemDescription= menuInfo['itemDescription']
        itemGroup= menuInfo['itemGroup']
        half= menuInfo['half']
        quarter= menuInfo['quarter']
        full= menuInfo['full']
        halfPrice= menuInfo['halfPrice']
        quarterPrice= menuInfo['quarterPrice']
        fullPrice= menuInfo['fullPrice']
        item_image= menuInfo['item_image']
        itemPreparationTime = menuInfo['itemPreparationTime']
        AddUser = dbhelper.AddData().addVendorMenu(mobile,food_type,itemName,itemDescription,itemGroup,half,quarter,full,halfPrice,quarterPrice,fullPrice,item_image,itemPreparationTime)
        db={"success": True,'message':'Menu Added',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/add/offer/',methods=['GET','POST'])
def APiVendorOffer():
    if request.method=='POST':
        menuInfo   = json.loads(request.data)
        mobile  = menuInfo['mobile']
        offerName= menuInfo['offerName']
        offerType  = menuInfo['offerType']
        discount= menuInfo['discount']
        maxdiscount= menuInfo['maxdiscount']
        valid_to= menuInfo['valid_to']
        image= menuInfo['image']
        promocode= menuInfo['promocode']
        description = menuInfo['description']

        AddUser = dbhelper.AddData().addVendorOffer(mobile,offerName,offerType,discount,maxdiscount,valid_to,image,promocode,description)
        db={"success": True,'message':'Menu Added',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/edit/vendor/menu/',methods=['GET','POST'])
def APiEditMenu():
    if request.method=='POST':
        menuInfo   = json.loads(request.data)
        Id  = menuInfo['id']
        mobile  = menuInfo['mobile']
        food_type= menuInfo['food_type']
        itemName  = menuInfo['itemName']
        itemDescription= menuInfo['itemDescription']
        itemGroup= menuInfo['itemGroup']
        half= menuInfo['half']
        quarter= menuInfo['quarter']
        full= menuInfo['full']
        halfPrice= menuInfo['halfPrice']
        quarterPrice= menuInfo['quarterPrice']
        fullPrice= menuInfo['fullPrice']
        item_image= menuInfo['item_image']
        itemPreparationTime = menuInfo['itemPreparationTime']

        EditAccount = dbhelper.UpdateData().UpdateVendorMenu(Id,mobile,food_type,itemName,itemDescription,itemGroup,half,quarter,full,halfPrice,quarterPrice,fullPrice,item_image,itemPreparationTime)
        db={"success": True,'message':'MenuUpdate',"confirmation":1}

        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/delete/vendor/menu/',methods=['GET','POST'])
def APiMenuDelete():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        Id  = userInfo['id']
        EditAccount = dbhelper.DeleteData().DeleteVendorMenu(Id)
        db={"success": True,'message':'MenuDeleted',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)


@app.route('/api/get/offer/list/',methods=['GET','POST'])
def ApiGetOffer():
    if request.method=='POST':
        offer_info_data = dbhelper.GetData().GetOffer()
        offer_info_data_db = []
        if(len(offer_info_data))>0:
            for line in offer_info_data:
                offer_info_data_dict = {}
                offer_info_data_dict['id'] =line[0]
                offer_info_data_dict['offerName'] =line[1]
                offer_info_data_dict['offerType'] =line[2]
                offer_info_data_dict['discount']  =line[3]
                offer_info_data_dict['maxdiscount']=line[4]
                offer_info_data_dict['valid_to']=line[5]
                offer_info_data_dict['description']=line[6]
                offer_info_data_dict['image']='https://storage.googleapis.com/momvendor.appspot.com/offer/'+str(line[7])
                offer_info_data_dict['promocode']=line[8]
                offer_info_data_dict['mobile']=line[9]
                offer_info_data_dict['status']=line[10]


                offer_info_data_db.append(offer_info_data_dict)

        resp = Response(json.dumps({"success": True, "offer_data": offer_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)


@app.route('/api/get/menu/list/',methods=['GET','POST'])
def ApiGetMenu():
    if request.method=='POST':
        configure_data = json.loads(request.data)
        mobile  = configure_data['mobile']
        menu_info_data = dbhelper.GetData().VendorMenuList(mobile)
        print menu_info_data
        menu_info_data_db = []
        if(len(menu_info_data))>0:
            for line in menu_info_data:
                try:
                    menu_info_data_dict = {}
                    print "menu : "+line[3]
                    menu_info_data_dict['id'] =line[0]
                    menu_info_data_dict['mobile'] =line[1]
                    menu_info_data_dict['food_type'] =line[2]
                    menu_info_data_dict['itemName']  =line[3]
                    menu_info_data_dict['itemDescription']=line[4]
                    menu_info_data_dict['itemGroup']=line[5]
                    menu_info_data_dict['half']=line[6]
                    menu_info_data_dict['quarter']=line[7]
                    menu_info_data_dict['full']=line[8]
                    menu_info_data_dict['halfPrice']=line[9]
                    menu_info_data_dict['quarterPrice']=line[10]
                    menu_info_data_dict['item_image']=line[12]
                    menu_info_data_dict['fullPrice']=line[11]
                    menu_info_data_dict['itemPreparationTime']=line[16]
                    menu_info_data_dict['status']=line[17]

                    menu_info_data_db.append(menu_info_data_dict)
                except Exception as e:
                    print "error occoured while menuprocessing"
                    print e



        resp = Response(json.dumps({"success": True, "menu_data": menu_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)


@app.route('/api/get/menu/list/customer/',methods=['GET','POST'])
def ApiGetMenuCustomer():
    if request.method=='POST':
        configure_data = json.loads(request.data)
        mobile  = configure_data['mobile']
        menu_info_data = dbhelper.GetData().VendorMenuListCustomer(mobile)
        print menu_info_data
        menu_info_data_db = []
        if(len(menu_info_data))>0:
            for line in menu_info_data:
                try:
                    menu_info_data_dict = {}
                    print "menu : "+line[3]
                    menu_info_data_dict['id'] =line[0]
                    menu_info_data_dict['mobile'] =line[1]
                    menu_info_data_dict['food_type'] =line[2]
                    menu_info_data_dict['itemName']  =line[3]
                    menu_info_data_dict['itemDescription']=line[4]
                    menu_info_data_dict['itemGroup']=line[5]
                    menu_info_data_dict['half']=line[6]
                    menu_info_data_dict['quarter']=line[7]
                    menu_info_data_dict['full']=line[8]
                    menu_info_data_dict['halfPrice']=line[9]
                    menu_info_data_dict['quarterPrice']=line[10]

                    if float(line[11])>100:
                        fullPrice=float(line[11])+float(70)
                        print fullPrice
                    else:
                        fullPrice=float(line[11])*float(0.25)+float(10)+float(line[11])
                        print fullPrice
                    menu_info_data_dict['item_image']=line[12]
                    menu_info_data_dict['fullPrice']=fullPrice
                    menu_info_data_dict['itemPreparationTime']=line[16]

                    menu_info_data_db.append(menu_info_data_dict)
                except Exception as e:
                    print "error occoured while processing menu"
                    print e
        print "entire menu :"
        print menu_info_data_db
        try:
            resp = Response(json.dumps({"success": True, "menu_data": menu_info_data_db }))
            resp.headers['Content-type']='application/json'
            return after_request(resp)
        except Exception as e:
            print "exception occoured while parsing the response"
            print e
            resp = Response(json.dumps({"success": True, "menu_data": []}))
            resp.headers['Content-type'] = 'application/json'
            return after_request(resp)



@app.route('/api/get/menu/list/updated/',methods=['GET','POST'])
def ApiGetMenuUpdate():
    if request.method=='POST':
        configure_data = json.loads(request.data)
        mobile  = configure_data['mobile']
        menu_info_data = dbhelper.GetData().VendorMenuList(mobile)
        menu_info_data_dict_final = {}
        menu_info_data_db = []
        if(len(menu_info_data))>0:
            for line in menu_info_data:
                menu_info_data_dict = {}
                menu_info_data_dict['id'] =line[0]
                menu_info_data_dict['mobile'] =line[1]
                menu_info_data_dict['food_type'] =line[2]
                menu_info_data_dict['itemName']  =line[3]
                menu_info_data_dict['itemDescription']=line[4]
                menu_info_data_dict['itemGroup']=line[5]
                menu_info_data_dict['half']=line[6]
                menu_info_data_dict['quarter']=line[7]
                menu_info_data_dict['full']=line[8]
                menu_info_data_dict['halfPrice']=line[9]
                menu_info_data_dict['quarterPrice']=line[10]
                menu_info_data_dict['fullPrice']=line[11]
                menu_info_data_dict['qty']=1
                if float(line[11])>100:
                    fullPrice=float(line[11])+float(100)
                    print fullPrice
                else:
                    fullPrice=float(line[11])*float(0.25)+float(10)
                    print fullPrice
                menu_info_data_dict['item_image']=line[12]

                # menu_info_data_db.append(menu_info_data_dict)
                menu_info_data_dict_final[line[0]]=menu_info_data_dict

        resp = Response(json.dumps({"success": True, "menu_data": menu_info_data_dict_final }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)


@app.route('/api/get/menu/web/updated/',methods=['GET','POST'])
def ApiGetWebUpdate():
    if request.method=='POST':
        configure_data = json.loads(request.data)
        mobile  = configure_data['mobile']
        menu_info_data = dbhelper.GetData().VendorMenuList(mobile)

        menu_info_data_db = []
        if(len(menu_info_data))>0:
            for line in menu_info_data:
                menu_info_data_dict = {}
                menu_info_data_dict['id'] =line[0]
                menu_info_data_dict['mobile'] =line[1]
                menu_info_data_dict['food_type'] =line[2]
                menu_info_data_dict['itemName']  =line[3]
                menu_info_data_dict['itemDescription']=line[4]
                menu_info_data_dict['itemGroup']=line[5]
                menu_info_data_dict['half']=line[6]
                menu_info_data_dict['quarter']=line[7]
                menu_info_data_dict['full']=line[8]
                menu_info_data_dict['halfPrice']=line[9]
                menu_info_data_dict['quarterPrice']=line[10]
                # menu_info_data_dict['fullPrice']=line[11]
                menu_info_data_dict['qty']=1


                if float(line[11])>100:
                    fullPrice=float(line[11])+float(70)
                    print fullPrice
                else:
                    fullPrice=float(line[11])*float(0.25)+float(10)+float(line[11])
                    print fullPrice
                menu_info_data_dict['fullPrice']=fullPrice
                menu_info_data_dict['item_image']=line[12]

                menu_info_data_db.append(menu_info_data_dict)
                # menu_info_data_dict_final[line[0]]=menu_info_data_dict

        resp = Response(json.dumps({"success": True, "menu_data": menu_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)

@app.route('/api/menu/list/',methods=['GET','POST'])
def ApiGetMenuList2():
    if request.method=='POST':
        menu_info_data = dbhelper.GetData().VendorMenuList2()
        menu_info_data_db = []
        if(len(menu_info_data))>0:
            for line in menu_info_data:
                menu_info_data_dict = {}
                menu_info_data_dict['id'] =line[0]
                menu_info_data_dict['mobile'] =line[1]
                menu_info_data_dict['food_type'] =line[2]
                menu_info_data_dict['itemName']  =line[3]
                menu_info_data_dict['itemDescription']=line[4]
                menu_info_data_dict['itemGroup']=line[5]
                menu_info_data_dict['half']=line[6]
                menu_info_data_dict['quarter']=line[7]
                menu_info_data_dict['full']=line[8]
                menu_info_data_dict['halfPrice']=line[9]
                menu_info_data_dict['quarterPrice']=line[10]
                menu_info_data_dict['fullPrice']=line[11]

                menu_info_data_db.append(menu_info_data_dict)

        resp = Response(json.dumps({"success": True, "menu_data": menu_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)

@app.route('/api/fcm/confirm/order/',methods=['GET','POST'])
def Confirmorder():
    if request.method == 'POST':
        order_info=json.loads(request.data)
        orderId = order_info['orderId']
        mom_mobile = order_info['mom_mobile']
        print mom_mobile
        location_data = dbhelper.GetData().MomLocation(mom_mobile)
        if len(location_data) >0:
            Lat=location_data[0][0]
            Lan=location_data[0][1]
        else:
            response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Order has not been accepted Due to Location Error"}}))
            return after_request(response)

        EditAccount = dbhelper.UpdateData().UpdateDeliveryBoy(orderId)

        Partner_location = dbhelper.GetData().PartnerLocation(Lat,Lan)

        if(len(Partner_location))>0:
            delivery_mobile=Partner_location[0][0]
            delivery_latitute=Partner_location[0][1]
            delivery_longitude=Partner_location[0][2]
            EditAccount = dbhelper.UpdateData().UpdateDeliveryAssigned(orderId,delivery_mobile,delivery_latitute,delivery_longitude)


        response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"Order has been accepted" }}))
        return after_request(response)
    else:
        response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Order has not been accepted"}}))
        return after_request(response)


@app.route('/api/fcm/confirm/order/dashboard/',methods=['GET','POST'])
def ConfirmorderAdmin():
    if request.method == 'POST':
        order_info=json.loads(request.data)
        orderId = order_info['orderId']
        delivery_mobile = order_info['delivery_mobile']
        deliveryAssigned = dbhelper.UpdateData().updateDeliveryBoyAssign(orderId, delivery_mobile)

        response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"Order has been accepted" }}))
        return after_request(response)
    else:
        response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Order has not been accepted"}}))
        return after_request(response)



# @app.route('/api/fcm/order/assign/',methods=['GET','POST'])
# def AssignOrder():
# 	if request.method == 'GET':
# 		order_info=json.loads(request.data)
# 		order_data = dbhelper.GetData().getUnassignedOrder()
# 		for order in order_data:
#
# 		orderId = order_info['orderId']
# 		mom_mobile = order_info['mom_mobile']
# 		print mom_mobile
# 		location_data = dbhelper.GetData().MomLocation(mom_mobile)
# 		Lat=location_data[0][0]
# 		Lan=location_data[0][1]
#
# 		EditAccount = dbhelper.UpdateData().UpdateDeliveryBoy(orderId)
#
# 		Partner_location = dbhelper.GetData().PartnerLocation(Lat,Lan)
#
# 		if(len(Partner_location))>0:
# 			delivery_mobile=Partner_location[0][0]
# 			delivery_latitute=Partner_location[0][1]
# 			delivery_longitude=Partner_location[0][2]
# 			EditAccount = dbhelper.UpdateData().UpdateDeliveryAssigned(orderId,delivery_mobile,delivery_latitute,delivery_longitude)
#
#
# 		response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"Order has been accepted" }}))
# 		return after_request(response)
# 	else:
# 		response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Order has not been accepted"}}))
# 		return after_request(response)

@app.route('/api/deliver/order/',methods=['GET','POST'])
def Deliverorder():
    if request.method == 'POST':
        order_info=json.loads(request.data)
        orderId = order_info['orderId']
        mom_mobile = order_info['mom_mobile']
        location_data = dbhelper.GetData().MomLocation(mom_mobile)
        Lat=location_data[0][0]
        Lan=location_data[0][1]
        Partner_location = dbhelper.GetData().PartnerLocation(Lat,Lan)
        if(len(Partner_location))>0:
            delivery_mobile=Partner_location[0][0]
            delivery_latitute=Partner_location[0][1]
            delivery_longitude=Partner_location[0][2]
            EditAccount = dbhelper.UpdateData().UpdateDelivery2(orderId,delivery_mobile,delivery_latitute,delivery_longitude)

        response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"Order is Process to deliver" }}))
        return after_request(response)
    else:
        response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Order has not been accepted"}}))
        return after_request(response)

@app.route('/api/deliver/order/assign/',methods=['GET','POST'])
def DeliverorderAssign():
    if request.method == 'POST':
        order_info=json.loads(request.data)
        orderId = order_info['orderId']
        mobile= order_info['mobile']
        Partner_location = dbhelper.GetData().DeliveryLocation(mobile)
        delivery_mobile=Partner_location[0][0]
        delivery_latitute=Partner_location[0][1]
        delivery_longitude=Partner_location[0][2]
        EditAccount = dbhelper.UpdateData().UpdateDelivery2(orderId,delivery_mobile,delivery_latitute,delivery_longitude)

        response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"Order is Process to deliver" }}))
        return after_request(response)
    else:
        response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Order has not been accepted"}}))
        return after_request(response)


@app.route('/api/fcm/complete/order/',methods=['GET','POST'])
def Completeorder():
    if request.method == 'POST':
        order_info=json.loads(request.data)
        orderId = order_info['orderId']
        last=dbhelper.AddData().addCompleteBooking(orderId)
        EditAssign = dbhelper.DeleteData().DeleteRunorder(orderId)

        response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"Order has been completed" }}))
        return after_request(response)
    else:
        response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Order has not been completed"}}))
        return after_request(response)


@app.route('/api/customer/order/rating/',methods=['GET','POST'])
def RatingCompleteorder():
    if request.method == 'POST':
        order_info=json.loads(request.data)
        orderId = order_info['orderId']
        rating = order_info['rating']
        deliver_rating= order_info['deliver_rating']
        if deliver_rating=='0' and rating=='0':
            RatingCancel = dbhelper.UpdateData().UpdateCustomer2Rate(orderId,rating,deliver_rating)
        else:
            RatingStatus = dbhelper.UpdateData().UpdateCustomerRate(orderId,rating,deliver_rating)

        response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"Customer Rating Added" }}))
        return after_request(response)
    else:
        response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Customer Rating Not Added"}}))
        return after_request(response)

@app.route('/api/fcm/cancel/order/',methods=['GET','POST'])
def CompleteCancelorder():
    if request.method == 'POST':
        order_info=json.loads(request.data)
        orderId = order_info['orderId']
        last=dbhelper.AddData().addCancelBooking(orderId)
        EditAssign = dbhelper.DeleteData().deleteorder(orderId)
        EditAccount = dbhelper.UpdateData().UpdateCancelOrder(orderId)

        response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"This Order has been cancelled" }}))
        return after_request(response)
    else:
        response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"This Order has not been cancelled"}}))
        return after_request(response)


###Noted
@app.route('/api/get/new/order/list/',methods=['GET','POST'])
def ApiGetNewListOrder():
    if request.method=='POST':
        user_data =json.loads(request.data)
        mobile=user_data['mobile']
        order_info_data = dbhelper.GetData().OrderList(mobile)
        order_info_data_db = []
        if(len(order_info_data))>0:
            for line in order_info_data:
                order_info_data_dict = {}

                order_info_data_dict = {}
                order_info_data_dict['id']=line[0]
                order_info_data_dict['orderId']=line[1]
                order_info_data_dict['name']=line[2]
                order_info_data_dict['mobile']=line[3]

                if '\n' in line[4]:
                    add_part = ' '.join(line[4].split('\n')[:2])
                else:
                    add_part = line[4]

                order_info_data_dict['location']=add_part
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

                try:
                    # mom_name = dbhelper.GetData().getVendorLoginStatus(line[7])
                    vendor_name=str(line[10])+str(line[12])
                except:
                    vendor_name=''
                order_info_data_dict['vendor_name']=vendor_name
                order_info_data_dict['mom_name']=vendor_name
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

                # print order_info_data_db

        resp = Response(json.dumps({"success": True, "order_data": order_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)

##

# assign

@app.route('/api/get/new/order/web/',methods=['GET','POST'])
def ApiGetNewListWeb():
    if request.method=='POST':
        order_info_data = dbhelper.GetData().OrderListWeb()
        order_info_data_db = []
        if(len(order_info_data))>0:
            for line in order_info_data:
                order_info_data_dict = {}

                order_info_data_dict = {}
                order_info_data_dict['id']=line[0]
                order_info_data_dict['orderId']=line[1]
                order_info_data_dict['name']=line[2]
                order_info_data_dict['mobile']=line[3]

                if '\n' in line[4]:
                    str_add = ' '.join(line[4].split('\n')[:2])
                else:
                    str_add = line[4]
                order_info_data_dict['location']=str_add
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
                order_info_data_dict['orderStatus']=line[15]
                order_info_data_dict['deliver_number']=line[16]

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

@app.route('/api/get/assign/order/list/',methods=['GET','POST'])
def ApiGetAssignOrder():
    if request.method=='POST':
        order_info_data = dbhelper.GetData().AssignOderList()
        order_info_data_db = []
        if(len(order_info_data))>0:
            for line in order_info_data:
                order_info_data_dict = {}

                order_info_data_dict = {}
                order_info_data_dict['id']=line[0]
                order_info_data_dict['orderId']=line[1]
                order_info_data_dict['name']=line[2]
                order_info_data_dict['mobile']=line[3]
                if '\n' in line[4]:
                    str_add = ' '.join(line[4].split('\n')[:2])
                else:
                    str_add = line[4]

                order_info_data_dict['location']=str_add
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
                order_info_data_dict['orderStatus']=line[14]
                order_info_data_dict['deliver_number']=line[16]

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


@app.route('/api/get/complete/order/web/',methods=['GET','POST'])
def ApiGetNewComOrderWeb():
    if request.method=='POST':

        order_info_data = dbhelper.GetData().ComOrderweb()
        order_info_data_db = []
        if(len(order_info_data))>0:
            order_info_data_dict = {}
            order_info_data_dict['id']=line[0]
            order_info_data_dict['orderId']=line[1]
            order_info_data_dict['name']=line[2]
            order_info_data_dict['mobile']=line[3]

            if '\n' in line[4]:
                str_add = ' '.join(line[4].split('\n')[:2])
            else:
                str_add = line[4]
            order_info_data_dict['location']=str_add
            order_info_data_dict['latitude']=line[5]
            order_info_data_dict['longitude']=line[6]
            order_info_data_dict['mom_mobile']=line[7]
            order_info_data_dict['total_price']=line[8]


            image_name= dbhelper.GetData().MomProfile(line[7])[0][0]
            order_info_data_dict['image_name']=image_name
            order_info_data_dict['orderStatus']=line[9]

            order_info_data_dict['deliver_number']= line[10]
            order_info_data_dict['delivery_latitute']= line[11]
            order_info_data_dict['delivery_longitude']= line[12]
            order_info_data_dict['customerRating']= int(line[14])
            order_info_data_dict['deliveryRating']= int(line[15])
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






@app.route('/api/get/running/order/list/',methods=['GET','POST'])
def ApiGetNewRunOrder():
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


                if '\n' in line[4]:
                    str_add = ' '.join(line[4].split('\n')[:2])
                else:
                    str_add = line[4]
                order_info_data_dict['location']=str_add
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
                order_info_data_dict['deliver_number']=line[16]

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

@app.route('/api/get/complete/order/list/',methods=['GET','POST'])
def ApiGetNewComOrder():
    if request.method=='POST':
        user_data =json.loads(request.data)
        mobile=user_data['mobile']

        order_info_data = dbhelper.GetData().getCompleteOrderInfoMom(mobile)
        order_info_data_db = []
        if(len(order_info_data))>0:
            for line in order_info_data:
                order_info_data_dict = {}
                order_info_data_dict['id']=line[0]
                order_info_data_dict['orderId']=line[1]
                order_info_data_dict['name']=line[2]
                order_info_data_dict['mobile']=line[3]

                if '\n' in line[4]:
                    str_add =' '.join(line[4].split('\n')[:2])
                else:
                    str_add = line[4]
                order_info_data_dict['location']=str_add
                order_info_data_dict['latitude']=line[5]
                order_info_data_dict['longitude']=line[6]
                order_info_data_dict['mom_mobile']=line[7]
                order_info_data_dict['total_price']=line[8]


                image_name= dbhelper.GetData().MomProfile(line[7])[0][0]
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



@app.route('/api/active/vendor/account/',methods=['GET','POST'])
def APiVendorActive():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        EditAccount = dbhelper.UpdateData().UpdateActiveVendor(mobile)
        sendActivationMsg(mobile)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/deactive/vendor/account/',methods=['GET','POST'])
def APiVendorDeActive():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        EditAccount = dbhelper.UpdateData().UpdateDeActiveVendor(mobile)
        sendDeActivationMsg(mobile)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)


@app.route('/api/active/offer/list/',methods=['GET','POST'])
def APiVendorAcOffer():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        Id  = userInfo['id']
        EditAccount = dbhelper.UpdateData().UpdateActiveoffer(Id)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)


@app.route('/api/deactive/offer/list/',methods=['GET','POST'])
def APiVendorDeOffer():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        Id  = userInfo['id']
        EditAccount = dbhelper.UpdateData().UpdateActiveoffer(Id)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)


@app.route('/api/delete/vendor/account/',methods=['GET','POST'])
def APiVendorDelete():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        EditAccount = dbhelper.DeleteData().DeleteVendor(mobile)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/active/user/account/',methods=['GET','POST'])
def APiUserActive():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        EditAccount = dbhelper.UpdateData().UpdateActiveUser(mobile)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/deactive/user/account/',methods=['GET','POST'])
def APiUserDeActive():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        EditAccount = dbhelper.UpdateData().UpdateDeActiveUser(mobile)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)


@app.route('/api/delete/user/account/',methods=['GET','POST'])
def APiUserDelete():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        EditAccount = dbhelper.DeleteData().DeleteUser(mobile)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)
# selection report

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
        resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)


@app.route('/api/get/vendor/list/',methods=['GET','POST'])
def APiGetVendorList():
    if request.method=='POST':
        user_data = dbhelper.GetData().getVendorData()
        user_data_db=[]
        if(len(user_data))>0:
            for line in user_data:
                user_data_dict={}
                user_data_dict['id']  = line[0]
                user_data_dict['firstName']  = line[1]
                user_data_dict['lastName']  = line[2]
                user_data_dict['middleName']  = line[3]
                user_data_dict['email'] = line[4]
                user_data_dict['mobile'] = line[5]
                user_data_dict['address'] = line[6]
                user_data_dict['country'] = line[7]
                user_data_dict['state'] = line[8]
                user_data_dict['zipCode'] = line[9]
                user_data_dict['foodLicenseNo'] = line[10]
                user_data_dict['dob'] = line[11]
                user_data_dict['specialization'] = line[12]
                user_data_dict['comment'] = line[13]
                user_data_dict['openTime'] = line[14]
                user_data_dict['closeTime'] = line[15]
                user_data_dict['breakStart'] = line[16]
                user_data_dict['breakEnd'] = line[17]
                user_data_dict['profileStatus']=line[18]
                user_data_dict['image_name']=line[19]
                user_data_dict['latitude']=line[20]
                user_data_dict['longitude']=line[21]
                # user_data_dict['status']=line[22]
                user_data_dict['status']=line[22]
                user_data_dict['image']=line[23]

                user_data_db.append(user_data_dict)

        resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)

@app.route('/api/get/vendor/profile/',methods=['GET','POST'])
def APiGetVendorProfile():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        user_data = dbhelper.GetData().getVendorProfile(mobile)
        user_data_db=[]
        if(len(user_data))>0:
            for line in user_data:
                user_data_dict={}
                user_data_dict['id']  = line[0]
                user_data_dict['firstName']  = line[1]
                user_data_dict['lastName']  = line[2]
                user_data_dict['middleName']  = line[3]
                user_data_dict['email'] = line[4]
                user_data_dict['mobile'] = line[5]
                user_data_dict['address'] = line[6]
                user_data_dict['country'] = line[7]
                user_data_dict['state'] = line[8]
                user_data_dict['zipCode'] = line[9]
                user_data_dict['foodLicenseNo'] = line[10]
                user_data_dict['dob'] = line[11]
                user_data_dict['specialization'] = line[12]
                user_data_dict['comment'] = line[13]
                user_data_dict['openTime'] = line[14]
                user_data_dict['closeTime'] = line[15]
                user_data_dict['breakStart'] = line[16]
                user_data_dict['breakEnd'] = line[17]
                user_data_dict['profileStatus'] = line[18]
                user_data_dict['image_name'] = line[19]
                user_data_dict['latitude'] = line[20]
                user_data_dict['longitude'] = line[21]
                user_data_dict['image'] = line[23]
                user_data_dict['vendor_code'] = line[24]
                user_data_dict['about_mom'] = line[27]

                user_data_db.append(user_data_dict)

        resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)


#user auth

@app.route('/api/vendor/check/auth/', methods=['GET','POST'])
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
            AddCustomer= dbhelper.GetData().getVendorLogin(mobile)
            try:
                if len(AddCustomer)==0:
                    db={'message':'User Not Exist',"confirmation":0}
                    # text="Your+OTP+is+:+%s+Note+:+Please+ DO+NOT+SHARE+this+OTP+with+anyone."%(str(otp))
                    text ="Your + verification + code + is +%s ."%(str(otp))
                    mobile=str(mobile)
                    url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
                    print url
                    urlfetch.set_default_fetch_deadline(45)
                    resp = urlfetch.fetch(url=url,
                        method=urlfetch.GET,
                        headers={'Content-Type': 'text/html'})
                else:
                    db={'message': 'User Already Exist', "confirmation":1}
            except:
                pass
        else:
            db={'message': 'ReferalCode Not Exist', "confirmation":2}

        resp = Response(json.dumps({ "response": db}))
        return after_request(resp)

@app.route('/api/vendor/send/otp/', methods=['GET','POST'])
def CheckCustomerAuthOTP():
    if request.method == 'POST':
        user_data =json.loads(request.data)
        mobile = user_data['mobile']
        otp = user_data['otp']
        text =" Welcome to Mother on Mission. Your Login OTP is %s."%(str(otp))
        mobile=str(mobile)
        url ='http://alerts.variforrm.in/api?method=sms.normal&api_key=8d5b41565d64d9b7da4310877d45eb70&to=%s&sender=MOMION&message=%s&flash=0&unicode=0'%(str(mobile),text)
        urlfetch.set_default_fetch_deadline(45)
        resp = urlfetch.fetch(url=url,
            method=urlfetch.GET,
            headers={'Content-Type': 'text/html'})

        resp = Response(json.dumps({ "msg": "Sent Successfully"}))
        return after_request(resp)


@app.route('/api/update/vendor/profile/',methods=['GET','POST'])
def APiUpdateVendorProf():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        firstName= userInfo['firstName']
        middleName= userInfo['middleName']
        lastName= userInfo['lastName']
        email = userInfo['email']
        image_name = userInfo['image_name']
        address  = wordCleaner(userInfo['address'])
        country  = userInfo['country']
        state  = userInfo['state']
        zipCode  = userInfo['zipCode']
        foodLicenseNo  = userInfo['foodLicenseNo']
        dob  = userInfo['dob']
        specialization  = wordCleaner(userInfo['specialization'])
        comment  = wordCleaner(userInfo['comment'])
        openTime  = userInfo['openTime']
        endTime  = userInfo['endTime']
        breakStart  = userInfo['breakStart']
        breakEnd  = userInfo['breakEnd']
        latitude  = userInfo['latitude']
        longitude  = userInfo['longitude']
        image  = userInfo['image']
        about_mom= wordCleaner(userInfo['about_mom'])
        trackingStatus  = userInfo['trackingStatus']
        EditAccount = dbhelper.UpdateData().UpdateVendorProfile(mobile,firstName,middleName,lastName,email,image_name,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd,latitude,longitude,image,trackingStatus, about_mom)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/add/vendor/web/',methods=['GET','POST'])
def APiAddVendorWeb():
    if request.method=='POST':
        userInfo   = json.loads(request.data)
        mobile  = userInfo['mobile']
        firstName= userInfo['firstName']
        middleName = userInfo['middleName']
        lastName = userInfo['lastName']
        email      = userInfo['email']
        address  = userInfo['address']
        country  = userInfo['country']
        state  = userInfo['state']
        zipCode  = userInfo['zipCode']
        foodLicenseNo  = userInfo['foodLicenseNo']
        dob  = userInfo['dob']
        specialization  = userInfo['specialization']
        comment  = userInfo['comment']
        openTime  = userInfo['openTime']
        endTime  = userInfo['endTime']
        breakStart  = userInfo['breakStart']
        breakEnd  = userInfo['breakEnd']
        EditAccount = dbhelper.AddData().addVendorWeb(mobile,firstName,middleName,lastName,address,country,state,zipCode,foodLicenseNo,dob,specialization,comment,openTime,endTime,breakStart,breakEnd)
        db={"success": True,'message':'AccountUpdate',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)


# deliver boy

@app.route('/api/delivery/login/', methods=['GET','POST'])
def ApiDeliveryLogin2():
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


@app.route('/api/delivery/location/', methods=['GET','POST'])
def ApiDeliveryLocation():
    if request.method  == 'POST':
        user_data =json.loads(request.data)
        mobile = user_data['mobile']
        latitude  = user_data['latitude']
        longitude = user_data['longitude']
        orderId = user_data['orderId']
        deliver_status= dbhelper.GetData().getdeliverNumber(orderId)
        if len(deliver_status)!=0:
            deliver=deliver_status[0][0]
            orderStatus=deliver_status[0][1]
        else:
            deliver=''
            orderStatus=''
        deliver_location=dbhelper.GetData().getdeliverLocation(deliver)
        deliver_info_data_db = []
        if(len(deliver_location))>0:
            for line in deliver_location:
                deliver_info_data_dict = {}
                deliver_info_data_dict['deliver_lat']=line[0]
                deliver_info_data_dict['deliver_long']=line[1]
                deliver_info_data_dict['latitude']=latitude
                deliver_info_data_dict['longitude']=longitude
                deliver_info_data_dict['orderId']=orderId
                deliver_info_data_dict['orderStatus']=orderStatus

                EditAccount = dbhelper.UpdateData().UpdateDelivery(orderId,deliver,line[0],line[1])

                deliver_info_data_db.append(deliver_info_data_dict)
                db={'message':'Location Updated',"confirmation":1,"deliver_data":deliver_info_data_db}
        else:
            db={'message': 'User Not Exist', "confirmation":0}
        resp = Response(json.dumps({ "response": db}))
        return after_request(resp)

@app.route('/api/special/item/', methods=['GET','POST'])
def ApiSpecialItem():
    if request.method  == 'POST':
        user_data =json.loads(request.data)
        mobile = user_data['mobile']
        menuItem  = user_data['menuItem']
        date = user_data['date']


        EditAccount = dbhelper.UpdateData().UpdateSpecial(mobile,menuItem,date)

        db={'message':'Menu Updated',"confirmation":1}

        resp = Response(json.dumps({ "response": db}))
        return after_request(resp)


@app.route('/api/mom/customer/query/',methods=['GET','POST'])
def ApiAddMomQuery():
    if request.method=='POST':
        print 'data', request.data
        query_data = json.loads(request.data)
        name = query_data['name']
        customeremail= query_data['email']
        phone = query_data['phone']
        pincode= query_data['pincode']
        message =query_data['message']


        email = 'pratnaiksarthak63@gmail.com'

        mailhandler.sendMail().sendMomQueryDetails(name,customeremail,phone,pincode,message,email)
        AddUser = dbhelper.AddData().addQuery(name,email,phone,pincode,message)

        resp = Response(json.dumps({"success": True}))
        return after_request(resp)


@app.route('/api/mom/add/token/',methods=['GET','POST'])
def ApiAddMomToken():
    if request.method=='POST':
        query_data = json.loads(request.data)
        mobile = query_data['mobile']
        fcmToken= query_data['fcmToken']
        userType= query_data['userType']
        fcmTokenList= dbhelper.GetData.getToken("Vendor")

        print "fcmTokenLIst :"
        print fcmTokenList
        if (len(fcmTokenList) == 0):
            print " The fcm token list is empty"

        AddUser = dbhelper.AddData().addToken(mobile,fcmToken,userType)

        resp = Response(json.dumps({"success": True}))
        return after_request(resp)

@app.route('/api/customer/lead/', methods=['GET','POST'])
def ApiCustomerLead():
    if request.method  == 'POST':
        lead_location=dbhelper.GetData().getLead()
        lead_info_data_db = []
        if(len(lead_location))>0:
            for line in lead_location:
                lead_info_data_dict = {}
                lead_info_data_dict['name']=line[1]
                lead_info_data_dict['email']=line[2]
                lead_info_data_dict['phone']=line[3]
                lead_info_data_dict['pincode']=line[4]
                lead_info_data_dict['message']=line[5]

                lead_info_data_db.append(lead_info_data_dict)
        resp = Response(json.dumps({"success": True, "lead_data": lead_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)



# @app.route('/api/user/fcm/',methods=['GET','POST'])
# def broadcastorder():
# 	if request.method == 'POST':
# 		fcm_info=json.loads(request.data)
# 		to = fcm_info['to']
# 		senderType = fcm_info['senderType']
# 		message = fcm_info['message']
# 		title = fcm_info['title']

# 		fcmTokenList=dbhelper.GetData().getToken(senderType,to)
# 		print fcmTokenList
# 		if len(fcmTokenList)>0:
# 			for gcmT in fcmTokenList:
# 				message_data={ "data":  {"mobile":to,"title":title,"senderType":senderType,"message":message,"title":title},


# 				"to" : gcmT[0]
# 				}
# 				form_data = json.dumps(message_data)


# 				url='https://fcm.googleapis.com/fcm/send'
# 				urlfetch.set_default_fetch_deadline(45)

# 				resp = urlfetch.fetch(url=url,
# 					method=urlfetch.POST,
# 					payload=form_data,
# 					headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"}
# 					)




# 				print resp.content

# 			response = Response(json.dumps({"response":{"confirmation": 1}}))
# 			return after_request(response)


@app.route('/api/user/fcm/', methods=['GET','POST'])
def fcmMessageNotice():
    if request.method    == 'POST':
        fcm_info=json.loads(request.data)
        to = fcm_info['to']
        senderType = fcm_info['senderType']
        message = fcm_info['message']
        title = fcm_info['title']
        try:
            fcmTokenList=dbhelper.GetData().getToken(senderType,to)
            print fcmTokenList
            message_data={"notification":{"action":"Notification","body":message,"title":title,"imageUrl":"http://s33.postimg.org/slnc2rtwv/logo.png"},"to" : fcmTokenList[0][0]
                }
            form_data = json.dumps(message_data)
            url='https://fcm.googleapis.com/fcm/send'
            urlfetch.set_default_fetch_deadline(45)
            resp = urlfetch.fetch(url=url, method=urlfetch.POST, payload=form_data, headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"})
            print resp.content
        except:
            pass
        response = Response(json.dumps({"response":{"confirmation": 1}}))
        return after_request(response)

@app.route('/api/user/fcm/updated/', methods=['GET','POST'])
def fcmMessageNoticeOrderData():
    if request.method    == 'POST':
        fcm_info=json.loads(request.data)
        to = fcm_info['to']
        senderType = fcm_info['senderType']
        message = fcm_info['message']
        title = fcm_info['title']
        try:
            fcmTokenList=dbhelper.GetData().getToken(senderType,to)
            # print fcmTokenList

            message_data={ "data":  {"message":message, "cancallable":1 },
                "to" : fcmTokenList[0][0]
            }
            form_data = json.dumps(message_data)
            url='https://fcm.googleapis.com/fcm/send'
            urlfetch.set_default_fetch_deadline(45)
            resp = urlfetch.fetch(url=url,
                method=urlfetch.POST,
                payload=form_data,
                headers={"Authorization":"key=AIzaSyAAaAgERB7rzsgubWA0FuLoEOaA-iDQJ10", "Content-Type":"application/json"}
                )
            print resp.content
            response = Response(json.dumps({"response":{"confirmation": 1}}))
            return after_request(response)
        except:
            response = Response(json.dumps({"response":{"confirmation": 0}}))
            return after_request(response)



@app.route('/api/check/vendor/license/', methods=['GET','POST'])
def checkVendorLicense():
    if request.method=='POST':
        vendorInfo=json.loads(request.data)
        vendor_no = vendorInfo['mobile']
        checfoodStatus= dbhelper.GetData().getFoodLicenseStatus(vendor_no)
        if len(checfoodStatus)==0:
            response = Response(json.dumps({"response":{"confirmation": 0}}))
            return after_request(response)
        elif checfoodStatus[0][0]=="":
            response = Response(json.dumps({"response":{"confirmation": 0}}))
            return after_request(response)
        else:
            response = Response(json.dumps({"response":{"confirmation": 1}}))
            return after_request(response)

@app.route('/api/status/online/change/', methods=['GET','POST'])
def checkVendorLicenseChange():
    if request.method=='POST':
        vendorInfo=json.loads(request.data)
        vendor_no = vendorInfo['mobile']
        vendor_status = vendorInfo['status']
        checfoodStatus= dbhelper.UpdateData().updateOnlineStatus(vendor_no, vendor_status)

        response = Response(json.dumps({"response":{"confirmation": 1}}))
        return after_request(response)


@app.route('/api/get/online/status/', methods=['GET','POST'])
def getVendorStatus():
    if request.method=='POST':
        vendorInfo=json.loads(request.data)
        vendor_no = vendorInfo['mobile']
        getVendorStatus= dbhelper.GetData().getVendorOnlineStatus(vendor_no)
        if len(getVendorStatus)!=0:
            if int(getVendorStatus[0][0])==1:
                response = Response(json.dumps({"response":{"status": "Online",  "statusInt": 1 }}))
                return after_request(response)
            else:
                response = Response(json.dumps({"response":{"status": "Offline",  "statusInt": 0 }}))
                return after_request(response)

        else:
            response = Response(json.dumps({"response":{"status": "Not Exist", "statusInt": 0}}))
            return after_request(response)

@app.route('/api/food/status/change/', methods=['GET','POST'])
def checkFoodStatusChange():
    if request.method=='POST':
        vendorInfo=json.loads(request.data)
        item_id = vendorInfo['item_id']
        food_status = vendorInfo['status']
        checfoodStatus= dbhelper.UpdateData().updateFoodOnlineStatus(item_id, food_status)
        response = Response(json.dumps({"response":{"confirmation": 1}}))
        return after_request(response)


############Offer selection
@app.route('/api/add/contact/us/', methods=['GET','POST'])
def addContactUs():
    if request.method=='POST':
        contactUs=json.loads(request.data)
        name = contactUs['name']
        phone_no = contactUs['phone_no']
        email   = contactUs['email']
        pincode   = contactUs['pincode']
        note    = contactUs['note']

        AddContactUs = dbhelper.AddData().addContactUs(name,phone_no,email, pincode, note)

        resp = Response(json.dumps({"success": True}))
        return after_request(resp)

@app.route('/api/get/contact/us/', methods=['GET','POST'])
def getContactUS():
    if request.method=='POST':
        getContactUs = dbhelper.GetData().getContacUsT()
        getContactList =[]
        for row in getContactUs:
            contact_dict={}
            contact_dict['name'] = row[1]
            contact_dict['phone_no'] = row[2]
            contact_dict['email'] = row[3]
            contact_dict['pincode'] = row[4]
            contact_dict['note'] = row[5]
            getContactList.append(contact_dict)


        resp = Response(json.dumps({"success": True, 'contact_data': getContactList}))
        return after_request(resp)


@app.route('/api/add/offer/section/', methods=['GET','POST'])
def addOfferSectionnew():
    if request.method=='POST':
        offerInfo=json.loads(request.data)
        offer_name = offerInfo['offer_name']
        offer_type = offerInfo['offer_type']
        discount = offerInfo['discount']
        maxdiscount = offerInfo['maxdiscount']
        valid_to = offerInfo['valid_to']
        pvalues = offerInfo['pvalues']
        image = offerInfo['image']
        promoCode = offerInfo['promoCode']
        mobile = offerInfo['mobile']
        Status = 0
        chefPart = offerInfo['chefPart']
        momPart = offerInfo['momPart']
        minVal = offerInfo['minVal']
        maxVal = offerInfo['maxVal']
        minCartVal = offerInfo['minCartVal']

        addStatus= dbhelper.AddData().addFoodOnlineStatus(offer_name,offer_type,discount,maxdiscount,valid_to,pvalues,image,promoCode,mobile,Status,chefPart,momPart,minVal,maxVal, minCartVal)

        response = Response(json.dumps({"response":{"confirmation": 1}}))
        return after_request(response)

@app.route('/api/get/offer/section/', methods=['GET','POST'])
def ApiCustomeroffer():
    if request.method  == 'POST':
        offer_location=dbhelper.GetData().getoffernew()
        offer_info_data_db = []
        for line in offer_location:
            offer_info_data_dict = {}
            offer_info_data_dict['id']=line[0]
            offer_info_data_dict['offer_name']=line[1]
            offer_info_data_dict['offer_type']=line[2]
            offer_info_data_dict['discount']=line[3]
            offer_info_data_dict['maxdiscount']=line[4]
            offer_info_data_dict['valid_to']=line[5]
            offer_info_data_dict['pvalues']=line[6]
            offer_info_data_dict['image']='https://storage.googleapis.com/momvendor.appspot.com/offer/'+str(line[7])
            offer_info_data_dict['promocode']=line[8]
            offer_info_data_dict['mobile']=line[9]
            offer_info_data_dict['status']=line[10]
            offer_info_data_dict['chefPart']=line[11]
            offer_info_data_dict['momPart']=line[12]
            offer_info_data_dict['minVal']=line[13]
            offer_info_data_dict['maxVal']=line[14]
            offer_info_data_db.append(offer_info_data_dict)
        resp = Response(json.dumps({"success": True, "offer": offer_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)

@app.route('/api/get/offer/section/dashboard/', methods=['GET','POST'])
def ApiCustomerofferDashboard():
    if request.method  == 'POST':
        offer_location=dbhelper.GetData().getoffernewDashboard()
        offer_info_data_db = []
        for line in offer_location:
            offer_info_data_dict = {}
            offer_info_data_dict['id']=line[0]
            offer_info_data_dict['offer_name']=line[1]
            offer_info_data_dict['offer_type']=line[2]
            offer_info_data_dict['discount']=line[3]
            offer_info_data_dict['maxdiscount']=line[4]
            offer_info_data_dict['valid_to']=line[5]
            offer_info_data_dict['pvalues']=line[6]
            offer_info_data_dict['image']='https://storage.googleapis.com/momvendor.appspot.com/offer/'+str(line[7])
            offer_info_data_dict['promocode']=line[8]
            offer_info_data_dict['mobile']=line[9]
            offer_info_data_dict['status']=line[10]
            offer_info_data_dict['chefPart']=line[11]
            offer_info_data_dict['momPart']=line[12]
            offer_info_data_dict['minVal']=line[13]
            offer_info_data_dict['maxVal']=line[14]
            offer_info_data_db.append(offer_info_data_dict)
        resp = Response(json.dumps({"success": True, "offer": offer_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)

@app.route('/api/get/order/price/info/', methods=['GET','POST'])
def ApiorderpriceinfoUpdate():
    if request.method  == 'POST':
        order_location=dbhelper.GetData().getorderprice()
        order_info_data_db = []
        for line in order_location:
            order_info_data_dict = {}
            order_info_data_dict['id']=line[0]
            order_info_data_dict['orderId']=line[1]
            order_info_data_dict['totalPrice']=line[2]
            order_info_data_dict['chefPrice']=line[3]
            order_info_data_dict['momPrice']=line[4]
            order_info_data_dict['packagingCharge']=line[5]
            order_info_data_dict['discountAmount']=line[6]
            order_info_data_dict['taxAmount']=line[7]
            order_info_data_dict['subTotal']=line[8]


            order_info_data_dict['deleveryCharge']=line[9]

            order_info_data_dict['couponApplied']=line[10]
            order_info_data_dict['chefCouponApplied']=line[11]
            order_info_data_dict['momCouponAmount']=line[12]
            order_info_data_dict['Status']=line[13]

            order_info_data_db.append(order_info_data_dict)
        resp = Response(json.dumps({"success": True, "priceInfo": order_info_data_db }))
        resp.headers['Content-type']='application/json'
        return after_request(resp)

@app.route('/api/update/offer/section/',methods=['GET','POST'])
def APiupdatezoneoffer():
    if request.method=='POST':
        offerInfo   = json.loads(request.data)
        Id  = offerInfo['id']

        updateoffer = dbhelper.UpdateData().Updatezoneoffer(Id)
        db={"success": True,'message':'Update',"confirmation":1}

        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/update/offer/zone/section/',methods=['GET','POST'])
def APiupdatezoneoffernew():
    if request.method=='POST':
        offerInfo   = json.loads(request.data)
        Id  = offerInfo['id']

        updateoffer = dbhelper.UpdateData().Updatezoneoffernew(Id)
        db={"success": True,'message':'Update',"confirmation":1}

        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/delete/offer/menu/',methods=['GET','POST'])
def APiDeleteoffer():
    if request.method=='POST':
        offerInfo   = json.loads(request.data)
        Id  = offerInfo['id']
        Editoffer = dbhelper.DeleteData().Deleteoffer(Id)
        db={"success": True,'message':'offerDeleted',"confirmation":1}
        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/get/profile/pics/',methods=['GET','POST'])
def APIGETProfile():
    if request.method=='POST':
        offerInfo   = json.loads(request.data)
        mobile  = offerInfo['mobile']
        getProfilePics = dbhelper.GetData().getProfilePics(mobile)
        if len(getProfilePics)==0:
            db={"confirmation":1, "profile_image": ""}
        else:
            db={"confirmation":1, "profile_image": getProfilePics[0][0]}

        resp = Response(json.dumps({"response": db}))
        return after_request(resp)

@app.route('/api/fcm/confirm/order/assign/cron/',methods=['GET','POST'])
def ConfirmorderCronJob():
    if request.method == 'GET':
        try:
            orderDataLst = dbhelper.GetData().getOrderListData()
            orderId=""
            for order in orderDataLst:
                orderId = order[0]
                Lat = order[1]
                Lan = order[2]
                Partner_location = dbhelper.GetData().Partner(Lat,Lan)
                if(len(Partner_location))>0:
                    delivery_mobile=Partner_location[0][0]
                    delivery_latitute=Partner_location[0][1]
                    delivery_longitude=Partner_location[0][2]
                    EditAccount = dbhelper.UpdateData().UpdateDeliveryAssigned(orderId,delivery_mobile,delivery_latitute,delivery_longitude)

        except:
            orderId=""
        response = Response(json.dumps({"response":{"confirmation": 1,  "orderId":orderId,"message":"Order has been accepted" }}))
        return after_request(response)
    else:
        response = Response(json.dumps({"response":{"confirmation": 0 ,"message":"Order has not been accepted"}}))
        return after_request(response)

###########Payment GateWay Integeration
@app.route('/api/genrate/checksum/web/',methods=['GET','POST'])
def GenerateCheckSumWEB():
    if request.method=='POST':
        offerInfo   = json.loads(request.data)
        CUST_ID  = offerInfo['mobile']
        ORDER_ID  = offerInfo['orderId']
        TXN_AMOUNT  = offerInfo['TXN_AMOUNT']



        params = {
            "MID": "oAKmkJ83830562245354",
            "ORDER_ID": ORDER_ID,
            "CUST_ID": str(CUST_ID),
            "TXN_AMOUNT": str(TXN_AMOUNT).strip(),
            "WEBSITE":"oAKmkJWEB",
            "CHANNEL_ID": "WEB",
            "INDUSTRY_TYPE_ID": "Retail",
            "CALLBACK_URL": "https://mom-apicalls.appspot.com/api/verify/checksum/web/"
        }

        print params
        merchant_key ='OvHOjSL&up@PT2RB'



        mCheckSum= CheckSumParser.generate_checksum(params,merchant_key)

        params['CHECKSUMHASH'] =mCheckSum
        response = Response(json.dumps({"CHECKSUMHASH":mCheckSum, "params": params}))
        return after_request(response)

@app.route('/api/genrate/checksum/app/',methods=['GET','POST'])
def GenerateCheckSumAPP():
    if request.method=='POST':
        offerInfo   = json.loads(request.data)
        CUST_ID  = offerInfo['mobile']
        ORDER_ID  = offerInfo['orderId']
        TXN_AMOUNT  = offerInfo['TXN_AMOUNT']
        # params = {
        #     "MID": "TnhBck45795834165234",
        #     "ORDER_ID": ORDER_ID,
        #     "CUST_ID": str(CUST_ID),
        #     "TXN_AMOUNT": str(TXN_AMOUNT).strip(),
        #     "CHANNEL_ID": "WEB",
        #     "INDUSTRY_TYPE_ID": "Retail",
        #     "WEBSITE": "WEBSTAGING",
        #     "CALLBACK_URL": "https://mom-apicalls.appspot.com/api/verify/checksum/app/"
        # }
        # merchant_key ='UnuaRuD5AKV5XwBz'

        params = {
            "MID": "oAKmkJ83830562245354",
            "ORDER_ID": ORDER_ID,
            "CUST_ID": str(CUST_ID),
            "TXN_AMOUNT": str(TXN_AMOUNT).strip(),
            "CHANNEL_ID": "WAP",
            "WEBSITE":"oAKmkJWEB",
            "INDUSTRY_TYPE_ID": "Retail",
            "CALLBACK_URL": "https://mom-apicalls.appspot.com/api/verify/checksum/app/"
        }

        print params
        merchant_key ='OvHOjSL&up@PT2RB'


        mCheckSum= CheckSumParser.generate_checksum(params,merchant_key)
        params['CHECKSUMHASH'] =mCheckSum
        # params['WEBSITE'] ="https://motheronmission.com/"

        print '**', params
        response = Response(json.dumps({"CHECKSUMHASH":mCheckSum, "params": params}))
        return after_request(response)
@app.route('/api/genrate/checksum/',methods=['GET','POST'])
def GenerateCheckSum():
    if request.method=='GET':

        # name = dataInfo['name']
        CUST_ID= request.args.get('mobile')
        ORDER_ID= request.args.get('orderId')

        TXN_AMOUNT = request.args.get('TXN_AMOUNT')


        # params = {
        #     "MID": "TnhBck45795834165234",
        #     "ORDER_ID": ORDER_ID,
        #     "CUST_ID": str(CUST_ID),
        #     "TXN_AMOUNT": str(TXN_AMOUNT).strip(),
        #     "CHANNEL_ID": "WEB",
        #     "INDUSTRY_TYPE_ID": "Retail",
        #     "WEBSITE": "WEBSTAGING",
        #     "CALLBACK_URL": "https://mom-apicalls.appspot.com/api/verify/checksum/app/"
        # }
        #
        # print params
        # merchant_key ='UnuaRuD5AKV5XwBz'

        params = {
            "MID": "oAKmkJ83830562245354",
            "ORDER_ID": ORDER_ID,
            "CUST_ID": str(CUST_ID),
            "TXN_AMOUNT": str(TXN_AMOUNT).strip(),
            "CHANNEL_ID": "WEB",
            "WEBSITE":"oAKmkJWEB",
            "INDUSTRY_TYPE_ID": "Retail",
            "CALLBACK_URL": "https://mom-apicalls.appspot.com/api/verify/checksum/web/"
        }

        print params
        merchant_key ='OvHOjSL&up@PT2RB'

        param_dict = params


        mCheckSum= CheckSumParser.generate_checksum(params,merchant_key)

        param_dict['CHECKSUMHASH'] =mCheckSum
    response = Response(json.dumps({"CHECKSUMHASH":mCheckSum, "params": param_dict}))
    return after_request(response)



@app.route('/api/verify/checksum/app/',methods=['POST'])
def VerifyCheckSumApp():
    if request.method=='POST':
        respons_dict = {}
        checksum="0"

        for i in request.form.keys():
            respons_dict[i]=request.form[i]
            if i=='CHECKSUMHASH':
                checksum = request.form[i]  #Getting Checksum to verify its authenticity
            if 'GATEWAYNAME' in respons_dict:
                if respons_dict['GATEWAYNAME'] == 'WALLET':
                    respons_dict['BANKNAME'] = 'null';  #If Gateway is user's paytm wallet setting bankname to null
        MERCHANT_KEY ='OvHOjSL&up@PT2RB'


        # if verify:
        if checksum =="0":
            updateOrderStatus = dbhelper.UpdateData().updateOrderStatusInfoNeg(respons_dict['ORDERID'])
            str_msg= "order unsuccessful because of TXN Failure"
            response = Response(json.dumps({"msg":str_msg, "confirmation": 0}))
            return after_request(response)
        else:
            verify = CheckSumParser.verify_checksum(respons_dict, MERCHANT_KEY, checksum)

            if respons_dict['RESPCODE'] == '01':
                updateOrderStatus = dbhelper.UpdateData().updateOrderStatusInfo(respons_dict['ORDERID'])
                getOrderData = dbhelper.GetData().getOrderInfoData(respons_dict['ORDERID'])[0]
                try:
                    fcmTokenList=dbhelper.GetData().getTokenCustomer(getOrderData['mobile'])
                    print fcmTokenList

                    message_data={ "data":  {"orderId":getOrderData['orderId'],"customerName":getOrderData['name'], "customerMobile":getOrderData['mobile'], "totalAmount": getOrderData['totalPrice'], "address":getOrderData['location'], "note":getOrderData['note'], "promoCode": getOrderData['promoCode'],"dateTime":'', "cancallable":1 },"to" : fcmTokenList[0][0]
                    }
                    form_data = json.dumps(message_data)
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
                response = Response("Payment has been done. Redirectering to the MOM App....")
                return after_request(response)
            else:
                updateOrderStatus = dbhelper.UpdateData().updateOrderStatusInfoNeg(respons_dict['ORDERID'])
                str_msg= "order unsuccessful because"+respons_dict['RESPMSG']
                response = Response(json.dumps({"msg":str_msg, "confirmation": 0}))
                return after_request(response)

@app.route('/api/verify/checksum/web/',methods=['POST'])
def VerifyCheckSumweb():
    if request.method=='POST':
        respons_dict = {}
        checksum="0"
        for i in request.form.keys():
            respons_dict[i]=request.form[i]
            if i=='CHECKSUMHASH':
                checksum = request.form[i]  #Getting Checksum to verify its authenticity
            if 'GATEWAYNAME' in respons_dict:
                if respons_dict['GATEWAYNAME'] == 'WALLET':
                    respons_dict['BANKNAME'] = 'null';  #If Gateway is user's paytm wallet setting bankname to null
        MERCHANT_KEY ='OvHOjSL&up@PT2RB'


        # if verify:
        if checksum=="0":
            updateOrderStatus = dbhelper.UpdateData().updateOrderStatusInfoNeg(respons_dict['ORDERID'])

            str_msg= "order unsuccessful because of TXN Failure"
            return redirect("https://delhi-1018.appspot.com/#!/main/checkOut?confirmation=0&msg="+str_msg, code=302)
        else:
            verify = CheckSumParser.verify_checksum(respons_dict, MERCHANT_KEY, checksum)
            if respons_dict['RESPCODE'] == '01':
                updateOrderStatus = dbhelper.UpdateData().updateOrderStatusInfo(respons_dict['ORDERID'])
                getOrderData = dbhelper.GetData().getOrderInfoData(respons_dict['ORDERID'])[0]
                try:
                    fcmTokenList=dbhelper.GetData().getTokenCustomer(getOrderData['mobile'])
                    print fcmTokenList

                    message_data={ "data":  {"orderId":getOrderData['orderId'],"customerName":getOrderData['name'], "customerMobile":getOrderData['mobile'], "totalAmount": getOrderData['totalPrice'], "address":getOrderData['location'], "note":getOrderData['note'], "promoCode": getOrderData['promoCode'],"dateTime":'', "cancallable":1 },"to" : fcmTokenList[0][0]
                    }
                    form_data = json.dumps(message_data)
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

                response = Response(json.dumps({"msg":"order successful", "confirmation": 1}))
                return redirect("https://delhi-1018.appspot.com/#!/main/checkOut?confirmation=1", code=302)
            else:
                updateOrderStatus = dbhelper.UpdateData().updateOrderStatusInfoNeg(respons_dict['ORDERID'])

                str_msg= "order unsuccessful because"+respons_dict['RESPMSG']
                return redirect("https://delhi-1018.appspot.com/#!/main/checkOut?confirmation=0&msg="+str_msg, code=302)

@app.route('/api/mtrack/file/upload/',methods=['GET','POST'])
def apiMtrackFileUpload():
    if request.method=='POST':
        file_object = request.files['file']

        BUCKET_NAME = 'momvendor.appspot.com'
        storage = googleapiclient.discovery.build('storage', 'v1')
        GCS_UPLOAD_FOLDER = 'documents'

        filename = file_object.filename
        string_io_file = StringIO.StringIO(file_object.stream.read())

        filename_list= filename.split('.')
        filename_v=filename_list[0]+"_"+str(datetime.now()).replace(" ","_")+'.'+filename_list[1]
        fullName = GCS_UPLOAD_FOLDER + '/'+ filename_v
        print fullName, filename_v
        body = {
            'name': fullName,
        }
        req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'image/jpeg'))
        response = req.execute()


        image='https://storage.googleapis.com/momvendor.appspot.com/documents/'+ filename_v

        resp = Response(json.dumps({"success": True, "datasets": 'Yahoo', 'image': image }))
        return after_request(resp)
