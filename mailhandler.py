import webapp2
import jinja2
import cgi
import os
import smtplib
import json
import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

from google.appengine.api import mail


class sendMail():
    
    def sendLeadsDetails(self,to_id,name):
        message = mail.EmailMessage(sender = "Innobins Analytics <tech.gaplogix@gmail.com>",
                                        subject = "Birthday Wish")
        message.to = to_id
        message.html = 'Hi' + name + '. Happy birthday my employee, you make everything easier and I appreciate you very much, thank you for being part of this team.'
        message.send()
        print 'sendMail'

    def sendDetails(self,Email,reportInTime,reportOutTime,empCode,date):
        message = mail.EmailMessage(sender = "Innobins Analytics <tech.gaplogix@gmail.com>",
                                        subject = "Regularize Attendance ")
        message.to = Email
        message.html = leads_mail.mail_content%(empCode,date,reportInTime,reportOutTime)
        message.send()
        print 'sendMail'

    def sendLeaveDetails(self,email,empCode,leaveType,startDate,endDate,duration,reason):
        message = mail.EmailMessage(sender = "Innobins Analytics <tech.gaplogix@gmail.com>",
                                        subject = "Leave Request ")
        message.to = email
        message.html = leads_leavemail.mail_content%(empCode,leaveType,startDate,endDate,duration,reason)
        message.send()
        print 'sendMail'

    def sendReimbursementDetails(self,email,empCode,tripId,tDistance,tTime,tReimbursed,reason):
        message = mail.EmailMessage(sender = "Innobins Analytics <tech.gaplogix@gmail.com>",
                                        subject = "Reimbursement Request ")
        message.to = email
        message.html = leads_reimmail.mail_content%(empCode,tripId,tDistance,tTime,tReimbursed,reason)
        message.send()
        print 'sendMail'