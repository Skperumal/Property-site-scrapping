import threading
import urllib.request
import time
import re
import json
import pyodbc
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as dt
import uuid
import os
import sys
import atexit
import getpass, poplib
import smtplib
import email
import logging

null="NULL"
urls = ['http://www.breg.net/commercial-properties.cfm']
array_image =[]

path_work=r"D:\Project\Sites\Breg\Automated_Scrap_Data\\"

#CURRENT_DATE&TIME
d_t=str(datetime.now())
date_now=dt.datetime.today().strftime("%d-%m-%Y")
#print(date_now)
            
cnxn1 = pyodbc.connect('DRIVER={SQL Server};SERVER=PFBASQL;DATABASE=WebScraping;UID=scraper;PWD=scraper')
cursor1 = cnxn1.cursor()

k =[]
cursor1.execute("SELECT * from dbo.CRAWL_INPUT")
for row in cursor1.fetchall():
 #print (row)
 k=row

cursor1.close()

def mail(value):
   SERVER = "mail.hawkisolutions.com"
   FROM = "ramprasadb@hawkisolutions.com"
   TO  = ["perumals@hawkisolutions.com"] # must be a list

   SUBJECT = "Error Log...!"

   #value = "This message was sent with Python's smtplib."

# Prepare actual message

   message = """\
From: %s
To: %s
Subject: %s

%s
   """ % (FROM, ", ".join(TO), SUBJECT, value)

# Send the mail
   try:
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()
   except:
     raise"unable to send mail, a secured connection cannot be established between program and the mailbox [issue-001]" 
   return message



####Log file creation and error handling
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
os.makedirs("%s%s" % (path_work,date_now) )
os.chmod("%s%s" % (path_work,date_now) ,0o777)
try:
 handler = logging.FileHandler("%s%s\%sBreg_log.log" % (path_work,date_now,k[0]))
 handler.setLevel(logging.DEBUG)
except IOError:
 print("no such log file in path, or file is write protected [issue-0]")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

class MyLogger(object):
                def __init__(self, logger, level):
                                """Needs a logger and a logger level."""
                                self.logger = logger
                                self.level = level

                def write(self, message):
                                # Only log if there is a message (not just a new line)
                                if message.rstrip() != "":
                                                
                                                self.i=message
                                                self.logger.log(self.level, message.rstrip())
                                                
                                                

#sys.stdout = MyLogger(logger, logging.INFO) 
sys.stderr = MyLogger(logger, logging.ERROR)


crawlval=0
def autoIncrement():  
 global crawlval  
 pStart = 1 #adjust start value, if req'd   
 #pInterval = 1 #adjust interval value, if req'd  
 if (crawlval == 0):   
  crawlval = pStart   
 else:   
  crawlval += 1
 return crawlval 

def getStreetNum(ele):
    newVal = re.split("((^[\s]*?[0-9].*? )(([A-Za-z0-9]*(\s?[\-&:/]\s?)[A-Za-z0-9]* )|[A-Za-z0-9]\s)?)",ele)
    if(len(newVal)>1):
        resultArr = [newVal[1],newVal[len(newVal)-1]]
    else:
        resultArr = ["",newVal[0]]
    return resultArr


def fetch_url(url):
   null="NULL"
   f = open(r"D:\foo.txt","w")
   
   f.write('crawlval,\tsitename,\ttxroll_name,\ttxroll_image,\ttxroll_StreetNumber,\ttxroll_StreetName,\ttxroll_OwnerCity,\ttxroll_OwnerState,\tTotal_SF,\tAvailable_SF,\tBroker_Name,\ttxroll_GBA,\ttxroll_description,\tproperty_type,\tGrossSalePrice\n');
   
   image_f =open(r"%s%s\%s.txt" % (path_work,date_now,k[0]),"w")
   dum_string_write= "WRITING HTML CONTENT OF PROPERTY TO FILES"
   image_f.write(' %s\n \n\n \n\n\n\n\n\n\n\n\n\n\n\n\n' % (dum_string_write))

   os.makedirs("%s%s\images" % (path_work,date_now) )
   os.chmod("%s%s\images\\" % (path_work,date_now),0o777)
            
           
   wd = webdriver.Firefox()
   wd.get(url)

   
   for i in range(1):
   
     html_page = wd.page_source
     soup = BeautifulSoup(html_page)
     htmlstring=soup.decode()
     
     #print(htmlstring)

     url_header="http://www.breg.net/"
     dissect=re.compile(r'%s'%k[2],re.M | re.I | re.DOTALL)
     dissect_url=re.compile(r'%s'%k[3],re.M | re.I | re.DOTALL)
     dissect_image=re.compile(r'id=\"slider\">(.*?)</div>',re.M | re.I | re.DOTALL)
     single_images=re.compile(r'src=\"\.\./(.*?)\"',re.M | re.I | re.DOTALL)
     for dis1 in re.findall(dissect,htmlstring):

        for dis2 in re.findall(dissect_url,dis1):
            
            url_property = url_header + dis2
            #time.sleep(5)
            #prop=webdriver.Firefox()
            #prop.get(url_property)
            wd.get(url_property)
            html_page_property = wd.page_source
            soup1 = BeautifulSoup(html_page_property)
            htmlstring_prop=soup1.decode()
            html_content=soup1.encode("utf-8")
            
            image_f =open(r"%s%s\%s.txt" % (path_work,date_now,k[0]),"a")
            image_f.write('%s\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n' % (html_content))
             
            # POPULATE
            

            StreetNumber=re.search('%s'%k[10],htmlstring_prop,re.DOTALL)
            
            if StreetNumber:
             StreetNumber=StreetNumber.group(1)
             #street=" ".join(StreetNumber.split())
             #StreetNumber=street
             Street_re1=re.compile(r'(&amp;)',re.M | re.I | re.DOTALL)
             StreetNumber=Street_re1.sub('&',StreetNumber)
             SampleNumber=getStreetNum(StreetNumber)
             StreetNumber = SampleNumber[0]
             StreetName = SampleNumber[1]

             #print(StreetNumber)
            else:
             StreetNumber=null;
             StreetName=null;
             
            #StreetName=re.search('%s'%k[11],htmlstring_prop,re.DOTALL)
            
            #if StreetName:
             #StreetName=StreetName.group(1)
             #Streename_re1=re.compile(r'(&amp;)',re.M | re.I | re.DOTALL)
             #StreetName=Streename_re1.sub('&',StreetName)
             #SampleNumber=getStreetNum(StreetName)
             #StreetNumber = SampleNumber['sNum']

             #print(txroll_image)
            #else:
            # StreetName=null;
             

            GBA=re.search('%s'%k[18],htmlstring_prop,re.DOTALL)
            
            if GBA:
             GBA=GBA.group(1)
             #print(property_type)
             sk=" ".join(GBA.split())
             GBA=sk
             GBA_re1=re.compile(r'(<.*?>)',re.M | re.I | re.DOTALL)
             GBA=GBA_re1.sub('#',GBA)
            else:
             GBA=null;
             
            PropCity=re.search('%s'%k[33],htmlstring_prop,re.DOTALL)
            if PropCity:
             PropCity=PropCity.group(1)
            else:
             PropCity=null;
             #print(txroll_StreetNumber.group(1))

            PropState=re.search('%s'%k[34],htmlstring_prop,re.DOTALL)
            if PropState:
             PropState=PropState.group(1)
            else:
             PropState=null;
             #print(txroll_StreetName.group(1))

            Broker_Name=re.search('%s'%k[39],htmlstring_prop,re.DOTALL)
            
            if Broker_Name:
             Broker_Name=Broker_Name.group(1)
             broker_desc=" ".join(Broker_Name.split())
             Broker_Name=broker_desc
             broker_re1=re.compile(r'(<.*?>)',re.M | re.I | re.DOTALL)
             Broker_Name=broker_re1.sub('#',Broker_Name)
            else:
             
             Broker_Name=null;
             #print(txroll_OwnerCity.group(1))

            Total_SF=re.search('%s'%k[40],htmlstring_prop,re.DOTALL)
            
            if  Total_SF:
             Total_SF=Total_SF.group(1)
            else:
             
             Total_SF=null;
             #print(txroll_OwnerState.group(1))

            Available_SF=re.search('%s'%k[41],htmlstring_prop,re.DOTALL)
            
            if  Available_SF:
             Available_SF=Available_SF.group(1)
            else:
             
             Available_SF=null;
             #print(Total_SF.group(1))

            Property_Remarks=re.search('%s'%k[42],htmlstring_prop,re.DOTALL)
            
            if  Property_Remarks:
             Property_Remarks=Property_Remarks.group(1)
             sk_desc=" ".join(Property_Remarks.split())
             Property_Remarks=sk_desc
             desc_re1=re.compile(r'(<.*?>)',re.M | re.I | re.DOTALL)
             Property_Remarks=desc_re1.sub('#',Property_Remarks)
             
             
            else:
             
             Property_Remarks=null;
             #print(Available_SF.group(1))

            Property_Image=re.search('%s'%k[43],htmlstring_prop,re.DOTALL)
            
            if Property_Image:
             Property_Image=Property_Image.group(1)
            else:
             
             Property_Image=null;
             #print(Broker_Name.group(1))

            BuildingName=re.search('%s'%k[44],htmlstring_prop,re.DOTALL)
            
            if BuildingName:
             BuildingName=BuildingName.group(1)
             #txroll_GBA.strip()
            else:
             BuildingName=null;
             #print(txroll_GBA.group(1))

            CAM=re.search('%s'%k[47],htmlstring_prop,re.DOTALL)
            
            if  CAM:
             CAM=CAM.group(1)
             
            else:
             
             CAM=null;
             #print(txroll_description.group(1))

            GrossSalePrice=re.search('%s'%k[50],htmlstring_prop,re.DOTALL)
            
            if  GrossSalePrice:
             GrossSalePrice=GrossSalePrice.group(1)
             GrossSalePrice_re1=re.compile(r'(<.*?>)',re.M | re.I | re.DOTALL)
             GrossSalePrice=GrossSalePrice_re1.sub('#',GrossSalePrice)
             
            else:
             
             GrossSalePrice=null;

             
            PropertyUse=re.search('%s'%k[90],htmlstring_prop,re.DOTALL)
            if  PropertyUse:
              PropertyUse=PropertyUse.group(1)
             
            else:
             
              PropertyUse=null;
             
            Rent=re.search('%s'%k[111],htmlstring_prop,re.DOTALL)
            if  Rent:
              Rent=Rent.group(1)
             
            else:
             
              Rent=null;
             
            Price=re.search('%s'%k[112],htmlstring_prop,re.DOTALL)
            if  Price:
              Price=Price.group(1)
             
            else:
             
              Price=null;


            
            #print(prop_image_dissect)
            
            

            #UNIQUE ID
            unique_id=uuid.uuid1()
            unique_id1=k[0] + '_' + str(unique_id)
            print(unique_id1)
              
            #f =open(r"D:\foo.txt","a")
            #f.write('%s \t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s \t %s\t %s\t %s\t %s\t%s\t %s\t %s\t %s\t %s\n' % (crawlval,k[0],StreetNumber,StreetName,GBA,PropCity,PropState,Broker_Name,Total_SF,Available_SF,Property_Remarks,Property_Image,BuildingName,CAM,GrossSalePrice,PropertyUse,Rent,Price))

            cursor2 = cnxn1.cursor()


            ###Saving images in the local and DB
              
            prop_image_dissect=re.findall(dissect_image,htmlstring_prop)
            image_main_value=re.findall(single_images,str(prop_image_dissect))
            for count,img_rows in enumerate(image_main_value):
           
              join_url = url_header + img_rows
                 
              #path_local_image='D:\Project\Sites\Breg\Automated_Scrap_Data\IMAGES_%s_%d.jpg'% (unique_id,count)
              path_local_image="%s%s\images\IMAGES_%s_%d.jpg" % (path_work,date_now,unique_id,count)
              if join_url not in array_image:
                 array_image.append(join_url)
                 urllib.request.urlretrieve(join_url, "%s" % (path_local_image))
                 #print(array_image)
                 path_image =open(r"%s" % (path_local_image),'rb').read()
                 cursor2.execute("if not exists (select * from dbo.picture where sitename = ? and Property_Image = ?) insert into dbo.picture(sitename,img,Property_Image,date_time,unique_id) values (?,?,?,?,?)",k[0],join_url,k[0],path_image,join_url,d_t,unique_id1)              
              
              #array_image=join_url
              #inserting into Table
              
            #cursor2.execute("insert into dbo.property_output(sitename,StreetNumber,StreetName,GBA,PropCity,PropState,Broker_Name,Total_SF,Available_SF,Property_Remarks,Property_Image,BuildingName,CAM,date_time) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",k[0],StreetNumber,StreetName,GBA,PropCity,PropState,Broker_Name,Total_SF,Available_SF,Property_Remarks,Property_Image,BuildingName,CAM,d_t)
            #cursor2.execute("insert into dbo.sales_output(sitename,GrossSalePrice,PropertyUse,Rent,Price,date_time) values (?,?,?,?,?,?)",k[0],GrossSalePrice,PropertyUse,Rent,Price,d_t)

            #Check for if row and if not present then update row
                 
            cursor2.execute("if not exists (select * from dbo.property_output where sitename = ? and StreetNumber = ? and StreetName = ? and GBA like ? and PropCity = ? and PropState = ? and Broker_Name = ? and Total_SF = ? and Available_SF = ?  and Property_Image = ? and BuildingName = ? and CAM = ? ) insert into dbo.property_output(sitename,StreetNumber,StreetName,GBA,PropCity,PropState,Broker_Name,Total_SF,Available_SF,Property_Remarks,Property_Image,BuildingName,CAM,date_time,unique_id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",k[0],StreetNumber,StreetName,GBA,PropCity,PropState,Broker_Name,Total_SF,Available_SF,Property_Image,BuildingName,CAM,k[0],StreetNumber,StreetName,GBA,PropCity,PropState,Broker_Name,Total_SF,Available_SF,Property_Remarks,Property_Image,BuildingName,CAM,d_t,unique_id1)
            cursor2.execute("if not exists (select * from dbo.sales_output where sitename = ? and GrossSalePrice = ? and PropertyUse = ? and Rent = ? and Price = ? and Property_Image = ?) insert into dbo.sales_output(sitename,GrossSalePrice,PropertyUse,Rent,Price,Property_Image,date_time,unique_id) values (?,?,?,?,?,?,?,?)",k[0],GrossSalePrice,PropertyUse,Rent,Price,Property_Image,k[0],GrossSalePrice,PropertyUse,Rent,Price,Property_Image,d_t,unique_id1)

            cursor2.commit()
            cursor2.close()
            
            #cursor1.execute("select * from dbo.sale_output")
            #for r in cursor1.fetchall():
            # print (r)
 
            #element=wd.find_element_by_link_text('IDX-pagination-footer-next')
            break
  

     
     
#looping   
threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
for thread in threads:
    thread.start();
for thread in threads:
    thread.join() 
    
 
atexit.register(mail(sys.stderr.i))
