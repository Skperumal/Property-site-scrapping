'''
Title: Lake , IN
Author: Perumal
Date: 21-09-2015
File version:1.0
status: development
website url: http://in-lake-assessor.governmaxa.com/propertymax/rover30.asp?sid=895B06F87785464A8074D602F72BF4CA
County,ST: MO
Description: all Page scrapper
python version: 3.3
libraries used: selnium. request, beautifulsoup, sys,os,stexit,logging,email,smtplib,poplib,re,threading
'''
import threading
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as dt

import os
import sys
import atexit
import getpass, poplib
import smtplib
import email
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains




start = datetime.now()
print(start)

#owner_array=['F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
owner_array=['A','B','C']
def mail(value):
   SERVER = "mail.hawkisolutions.com"
   FROM = "perumals@hawkisolutions.com"
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
try:
 handler = logging.FileHandler('Log.log')
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

def write_excel_file(arr, sheet_name, row_no):
    # wb = load_workbook('Dedham_MA.xlsx')
    # worksheet = wb.get_sheet_by_name(sheet_name)
    # for i in range(len(arr)):
    #     worksheet.cell(row=(row_no + 1), column=(i+1)).value = arr[i]
    # wb.save("Dedham_MA.xlsx")
    fp = open(sheet_name+".txt", 'a')
    for i in arr:
        fp.write(str(i) + "\t")
    fp.write("\n")
    fp.close()

null="NULL"
urls = ['http://in-lake-assessor.governmaxa.com/propertymax/ACAMA_Indiana/homepage.asp?sid=895B06F87785464A8074D602F72BF4CA']
#loop_url_link=['http://propertydata.orangecountygov.com/imate/viewlist.aspx?sort=printkey&swis=all&ownernamef=A&advanced=true&page=84']
array_image =[]

clickl_re="null"
path_work=r"D:\Project\Sites\Lake\Automated_Scrap_Data\\"

#CURRENT_DATE&TIME
d_t=str(datetime.now())
date_now=dt.datetime.today().strftime("%d-%m-%Y")

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

## Scraping Function
def fetch_url(url):
 null="NULL"
   ##IOException
 try:
  f = open(r"Lake.txt","w")
  f1 =open(r"Land_table.txt","w")
  f2 =open(r"Improvements_table.txt","w")
 
  
  f.write('crawl_id\tsite_name\tparcel_number\tparcel_address\tcurrent_total_value\tdate_as_of\tassess_year\tpay_year\towner\towner_address\ttransfer_date\ttaxing_unit\tparcel_address\ttownship\tDeeded_Acreage\tSection_and_Plat\tRouting_No\tLegal_Desc\tProperty_Class_Code\tNeighborhood_Code \tNeighborhood_Factor \tStreet_or_Road_Code \tLevel_Ground \tassess_year\tHigh \tLow\tRolling\tSwampy\tWater\tSewer\tNatural_Gas\tElectricity \tSidewalk\tAlley\tCurrent_Land_Value\tCurrent_Imp_Value\tCurrent_Total_Value\tNon_Res_Land \tNon_Res_Imp\tNon_Res_Total\tDwelling_Value\tFarmland_Value\tResidential_Land\tResidential_Imp\tResidential_Total\tReason_for_Change\tPrior_Land_Value\tPrior_Imp_Value\tClassified_Land_Value\tHomesite_Value\tAdjustment_Factor\tAverage_Value_Acre\n')
  f1.write('crawl_id\tparcel_number\tEffective_Frontage\tEffective_Depth\tAcreage\tSquare_Footage\tSoil_ID \tActual_Frontage\tDepth_Factor \tSoil_Productivity_Factor \tBase_Rate\tInfluence_Code_1\tInfluence_Code_2 \tInfluence_Code_3\tAssessed_Value \tInfluence_Factor_Code_1\tInfluence_Factor_Code_2 \tInfluence_Factor_Code_3\n')
  f2.write('crawl_id\tparcel_number\tImprovement Type Code \tBuilding # \tID # \tConstructed Yr. \tGrade \tTotal Area \tReplacement Cost \tAssessed Value')

 except IOError:
   logger.info("Insertion of header error..")
   print("Error in insertion of header to file or file is write protected..")
   ## Value Exception
 try:       
  wd = webdriver.Chrome()
  
  #wd.find_element_by_xpath('//*[@id="dept"]/div[3]/table/tbody/tr[2]/td/p[1]/b[1]/a')
 except ValueError:
  print("Url is improper or no url, ulr contains special characters")
     
  logger.info("The main page source code has been obtained successfully")   
 for val in owner_array:
     ###Pass values to the checkbox and click submit...
   time.sleep(4)
#   wd.switch_to_window(wd.window_handles[-1])
   
   wd.get(url)
   try:
    wd.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[5]/td/font/input').click()

   except:
    logger.info("No guest user ")
   time.sleep(6) 
   wd.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/font/b/a').click()
   time.sleep(3)
   element2=wd.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/font/input')
   element2.clear()
   element2.send_keys(val)
   wd.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/input').click()
   #prop.click(newlink)
   
   logger.info("Value entered successfully in text box... moving towards listing page")
   #test_case = wd.find_element_by_xpath("/html/body")
   #test_case.send_keys(Keys.CONTROL + Keys.TAB)
   time.sleep(4)
   #wd.switch_to_window(wd.window_handles[-1])
   list_page=wd.current_url
   #print(list_page)
   a=1
   '''
   new_value=1
   try:
    if new_value == 1:
         
      time.sleep(3)
      wd.get(loop_url_link)
      time.sleep(4)     
   except:
      print("Going from page loop=1")
   '''   
   ##MAIN LOOping Structure...
   while a == 1:
   #for i in range(count_loop):
     ## For directly going to the desired loop:
    
          
     
     html_search_listing = wd.page_source
     soup2 = BeautifulSoup(html_search_listing)
     htmlstring_page_listing=soup2.decode()
     
     url_header="http://in-lake-assessor.governmaxa.com/propertymax"
     dissect=re.compile(r'<b><a class="listlink"(.*?)>',re.M | re.I | re.DOTALL)
     dissect_url=re.compile(r'"\.\.(.*?)"',re.M | re.I | re.DOTALL)
     
     #dissect_image=re.compile(r'id=\"slider\">(.*?)</div>',re.M | re.I | re.DOTALL)
     #single_images=re.compile(r'src=\"\.\./(.*?)\"',re.M | re.I | re.DOTALL)

     for dis1 in re.findall(dissect,htmlstring_page_listing):

        for dis2 in re.findall(dissect_url,dis1):
          
          logger.info("proceeding to first listing page")
          url_property_inner = url_header + dis2
          url_property_inner_re1=re.compile(r'(&amp;)',re.M | re.I | re.DOTALL)
          url_property_inner=url_property_inner_re1.sub('&',url_property_inner)
          wd.get(url_property_inner)
          #new_value += 1
          time.sleep(4)
          html_search_listing_inner = wd.page_source
          soup_inner = BeautifulSoup(html_search_listing_inner)
          html_search_listing_inner=soup_inner.decode()
          
          
          #PROPERTY INFO ...............................
          autoIncrement()  

          
          parcel_number=re.search('<b>Parcel Number.*?<tr>\s*<td>.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if parcel_number:
             parcel_number=parcel_number.group(1)
             #print(StreetNumber)
          else:
             parcel_number=null;
             
          parcel_address=re.search('<b>Parcel Address.*?<tr>\s*<td>.*?\">.*?">(.*?)<',html_search_listing_inner,re.DOTALL)
          if parcel_address:
             parcel_address=parcel_address.group(1)
             #print(StreetNumber)
          else:
             parcel_address=null;

          current_total_value=re.search('<b>Parcel Address.*?<tr>\s*<td>.*?\">.*?">.*?">(.*?)<',html_search_listing_inner,re.DOTALL)
          if current_total_value:
             current_total_value=current_total_value.group(1)
             current_total_value_re2=re.compile(r'<.*?>',re.M | re.I | re.DOTALL)
             current_total_value=current_total_value_re2.sub('',current_total_value)
             #print(StreetNumber)
          else:
             current_total_value=null;

          
          date_as_of=re.search('<b>Parcel Address.*?<tr>\s*<td>.*?\">.*?">.*?">.*?">(.*?)<',html_search_listing_inner,re.DOTALL)
          if date_as_of:
             date_as_of=date_as_of.group(1)
             #print(StreetNumber)
          else:
             date_as_of=null;
             
          assess_year=re.search('<b>Parcel Address.*?<tr>\s*<td>.*?\">.*?">.*?">.*?">.*?">(.*?)<',html_search_listing_inner,re.DOTALL)
          if assess_year:
             assess_year=assess_year.group(1)
             #print(StreetNumber)
          else:
             assess_year=null;

          pay_year=re.search('<b>Parcel Address.*?<tr>\s*<td>.*?\">.*?">.*?">.*?">.*?">.*?">(.*?)<',html_search_listing_inner,re.DOTALL)
          if pay_year:
             pay_year=pay_year.group(1)
   
             #print(StreetNumber)
          else:
             pay_year=null;
          owner=re.search('<b>Owner\s*</b>.*?<font.*?">(.*?)<',html_search_listing_inner,re.DOTALL)
          if owner:
             owner=owner.group(1)
             #print(StreetNumber)
          else:
             owner=null;
             
          owner_address=re.search('<b>Owner Address\s*</b>.*?<font.*?">(.*?)</font>',html_search_listing_inner,re.DOTALL)
          if owner_address:
             owner_address=owner_address.group(1)
             sk131=" ".join(owner_address.split())
             owner_address=sk131
             owner_address_re2=re.compile(r'<.*?>',re.M | re.I | re.DOTALL)
             owner_address=owner_address_re2.sub(' ',owner_address)
             
             #print(StreetNumber)
          else:
             owner_address=null;

          transfer_date=re.search('<b>Transfer Date\s*</b>.*?<font.*?">(.*?)</font>',html_search_listing_inner,re.DOTALL)
          if transfer_date:
             transfer_date=transfer_date.group(1)
   
             #print(StreetNumber)
          else:
             transfer_date=null;

          taxing_unit=re.search('<b>Taxing Unit.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if taxing_unit:
             taxing_unit=taxing_unit.group(1)
             #print(StreetNumber)
          else:
             taxing_unit=null;
   
          township=re.search('<b>Township.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if township:
             township=township.group(1)
             #print(StreetNumber)
          else:
             township=null;

             
          Deeded_Acreage=re.search('<b>Deeded Acreage .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Deeded_Acreage:
             Deeded_Acreage=Deeded_Acreage.group(1)
             #print(StreetNumber)
          else:
             Deeded_Acreage=null;

          Section_and_Plat=re.search('<b>Section.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Section_and_Plat:
             Section_and_Plat=Section_and_Plat.group(1)
   
             #print(StreetNumber)
          else:
             Section_and_Plat=null;
             
          Routing_No=re.search('<b>Routing No.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Routing_No:
             Routing_No=Routing_No.group(1)
             #print(StreetNumber)
          else:
             Routing_No=null;
             
          Legal_Desc=re.search('<b>Legal Desc.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Legal_Desc:
             Legal_Desc=Legal_Desc.group(1)
             
             #print(StreetNumber)
          else:
             Legal_Desc=null;

          Property_Class_Code=re.search('<b>Property Class Code .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Property_Class_Code:
             Property_Class_Code=Property_Class_Code.group(1)
   
             #print(StreetNumber)
          else:
             Property_Class_Code=null;

          Neighborhood_Code =re.search('<b>Neighborhood Code.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Neighborhood_Code:
             Neighborhood_Code=Neighborhood_Code.group(1)
             #print(StreetNumber)
          else:
             Neighborhood_Code=null;
             
          Neighborhood_Factor =re.search('<b>Neighborhood Factor.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Neighborhood_Factor:
             Neighborhood_Factor=Neighborhood_Factor.group(1)
             #print(StreetNumber)
          else:
             Neighborhood_Factor=null;

          Street_or_Road_Code =re.search('<b>Street or Road Code.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Street_or_Road_Code:
             Street_or_Road_Code=Street_or_Road_Code.group(1)
             #print(StreetNumber)
          else:
             Street_or_Road_Code=null;

          
          Level_Ground =re.search('<b>Level Ground.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Level_Ground:
             Level_Ground=Level_Ground.group(1)
             #print(StreetNumber)
          else:
             Level_Ground=null;


          High =re.search('<b>High .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if High :
             High =High .group(1)
   
             #print(StreetNumber)
          else:
             High =null;
          Low=re.search('<b>Low .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Low:
             Low=Low.group(1)
             #print(StreetNumber)
          else:
             Low=null;
             
          Rolling=re.search('<b>Rolling.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Rolling:
             Rolling=Rolling.group(1)
             #print(StreetNumber)
          else:
             Rolling=null;

          Swampy=re.search('<b>Swampy .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Swampy:
             Swampy=Swampy.group(1)
   
             #print(StreetNumber)
          else:
             Swampy=null;

          Water=re.search('<b>Water .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Water:
             Water=Water.group(1)
             #print(StreetNumber)
          else:
             Water=null;
             
          Sewer=re.search('<b>Sewer .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Sewer:
             Sewer=Sewer.group(1)
             #print(StreetNumber)
          else:
             Sewer=null;

          Natural_Gas=re.search('<b>Natural Gas.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Natural_Gas:
             Natural_Gas=Natural_Gas.group(1)
             #print(StreetNumber)
          else:
             Natural_Gas=null;

          
          Electricity =re.search('<b>Electricity .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Electricity :
             Electricity =Electricity .group(1)
             #print(StreetNumber)
          else:
             Electricity =null;
             
          Sidewalk=re.search('<b>Sidewalk .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Sidewalk :
             Sidewalk=Sidewalk.group(1)
             #print(StreetNumber)
          else:
             Sidewalk=null;

          Alley=re.search('<b>Alley .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Alley:
             Alley=Alley.group(1)
   
             #print(StreetNumber)
          else:
             Alley=null;
             
          Current_Land_Value=re.search('<b>Current Land Value.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Current_Land_Value:
             Current_Land_Value=Current_Land_Value.group(1)
             #print(StreetNumber)
          else:
             Current_Land_Value=null;
             
          Current_Imp_Value=re.search('<b>Current Imp. Value .*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Current_Imp_Value:
             Current_Imp_Value=Current_Imp_Value.group(1)
             
             #print(StreetNumber)
          else:
             Current_Imp_Value=null;

          Current_Total_Value=re.search('<b>Current Total Value\s*</b></font>\s*</td>\s*<td align.*?>.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Current_Total_Value:
             Current_Total_Value=Current_Total_Value.group(1)
   
             #print(StreetNumber)
          else:
             Current_Total_Value=null;

          Non_Res_Land =re.search('<b>Non-Res. Land.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Non_Res_Land:
             Non_Res_Land=Non_Res_Land.group(1)
   
             #print(StreetNumber)
          else:
             Non_Res_Land=null;
             
          Non_Res_Imp=re.search('<b>Non-Res. Imp.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Non_Res_Imp:
             Non_Res_Imp=Non_Res_Imp.group(1)
             #print(StreetNumber)
          else:
             Non_Res_Imp=null;
             
          Non_Res_Total=re.search('<b>Non-Res. Total.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Non_Res_Total:
             Non_Res_Total=Non_Res_Total.group(1)
             
             #print(StreetNumber)
          else:
             Non_Res_Total=null;

          Dwelling_Value=re.search('<b>Dwelling Value.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Dwelling_Value:
             Dwelling_Value=Dwelling_Value.group(1)
   
             #print(StreetNumber)
          else:
             Dwelling_Value=null;

          Farmland_Value=re.search('<b>Farmland Value.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Farmland_Value:
             Farmland_Value=Farmland_Value.group(1)
             #print(StreetNumber)
          else:
             Farmland_Value=null;
             
          Residential_Land=re.search('<b>Residential Land.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Residential_Land:
             Residential_Land=Residential_Land.group(1)
             #print(StreetNumber)
          else:
             Residential_Land=null;

          Residential_Imp=re.search('<b>Residential Imp.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Residential_Imp:
             Residential_Imp=Residential_Imp.group(1)
             #print(StreetNumber)
          else:
             Residential_Imp=null;

          
          Residential_Total=re.search('<b>Residential Total.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Residential_Total:
             Residential_Total=Residential_Total.group(1)
             #print(StreetNumber)
          else:
             Residential_Total=null;
             
          Reason_for_Change=re.search('<b>Reason for Change.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Reason_for_Change:
             Reason_for_Change=Reason_for_Change.group(1)
             #print(StreetNumber)
          else:
             Reason_for_Change=null;

          Prior_Land_Value=re.search('<b>Parcel Address.*?<tr>\s*<td>.*?\">.*?">.*?">.*?">.*?">.*?">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Prior_Land_Value:
             Prior_Land_Value=Prior_Land_Value.group(1)
   
             #print(StreetNumber)
          else:
             Prior_Land_Value=null;
             
          Prior_Imp_Value=re.search('<b>Prior Land Value.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Prior_Imp_Value:
             Prior_Imp_Value=Prior_Imp_Value.group(1)
             #print(StreetNumber)
          else:
             Prior_Imp_Value=null;
             
          Classified_Land_Value=re.search('<b>Classified Land Value.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Classified_Land_Value:
             Classified_Land_Value=Classified_Land_Value.group(1)
             #print(StreetNumber)
          else:
             Classified_Land_Value=null;

          Homesite_Value=re.search('<b>Homesite Value.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Homesite_Value:
             Homesite_Value=Homesite_Value.group(1)
   
             #print(StreetNumber)
          else:
             Homesite_Value=null;

          Adjustment_Factor=re.search('<b>Adjustment Factor.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Adjustment_Factor:
             Adjustment_Factor=Adjustment_Factor.group(1)
             #print(StreetNumber)
          else:
             Adjustment_Factor=null;
             
          Average_Value_Acre=re.search('<b>Average Value.*?<font.*?\">(.*?)<',html_search_listing_inner,re.DOTALL)
          if Average_Value_Acre:
             Average_Value_Acre=Average_Value_Acre.group(1)
             #print(StreetNumber)
          else:
             Average_Value_Acre=null;

             
          try:
           wd.find_element_by_link_text('   Land').click()
          except:
           print("No land link")

          time.sleep(3)
          land_table= wd.page_source
          land_table_soup = BeautifulSoup(land_table)
          land_table_string=land_table_soup.decode()

          # Land Tab....................">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

          
           
          Effective_Frontage=re.search('<b>Effective Frontage.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Effective_Frontage:
             Effective_Frontage=Effective_Frontage.group(1)
             #print(StreetNumber)
          else:
             Effective_Frontage=null;

          
          Effective_Depth=re.search('<b>Effective Depth.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Effective_Depth :
             Effective_Depth =Effective_Depth.group(1)
             #print(StreetNumber)
          else:
             Effective_Depth =null;
             
          Acreage=re.search('<b>Acreage.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Acreage :
             Acreage=Acreage.group(1)
             #print(StreetNumber)
          else:
             Acreage=null;

          Square_Footage=re.search('<b>Square Footage.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Square_Footage:
             Square_Footage=Square_Footage.group(1)
   
             #print(StreetNumber)
          else:
             Square_Footage=null;
             
          Soil_ID =re.search('<b>Soil ID.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Soil_ID:
             Soil_ID=Soil_ID.group(1)
             #print(StreetNumber)
          else:
             Soil_ID=null;
             
          Actual_Frontage=re.search('<b>Actual Frontage.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Actual_Frontage:
             Actual_Frontage=Actual_Frontage.group(1)
             
             #print(StreetNumber)
          else:
             Actual_Frontage=null;

          Depth_Factor =re.search('<b>Depth Factor.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Depth_Factor:
             Depth_Factor=Depth_Factor.group(1)
   
             #print(StreetNumber)
          else:
             Depth_Factor=null

          Acreage_Factor=re.search('<b>Acreage Factor.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Acreage_Factor:
             Acreage_Factor=Acreage_Factor.group(1)
             #print(StreetNumber)
          else:
             Acreage_Factor=null;

          
          Soil_Productivity_Factor =re.search('<b>Soil Productivity Factor.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Soil_Productivity_Factor :
             Soil_Productivity_Factor =Soil_Productivity_Factor.group(1)
             #print(StreetNumber)
          else:
             Soil_Productivity_Factor =null;
             
          Base_Rate=re.search('<b>Base Rate.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Base_Rate :
             Base_Rate=Base_Rate.group(1)
             #print(StreetNumber)
          else:
             Base_Rate=null;

          Influence_Code_1=re.search('<b>Influence Code 1.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Influence_Code_1:
             Influence_Code_1=Influence_Code_1.group(1)
   
             #print(StreetNumber)
          else:
             Influence_Code_1=null;
             
          Influence_Code_2 =re.search('<b>Influence Code 2.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Influence_Code_2:
             Influence_Code_2=Influence_Code_2.group(1)
             #print(StreetNumber)
          else:
             Influence_Code_2=null;
             
          Influence_Code_3=re.search('<b>Influence Code 3.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Influence_Code_3:
             Influence_Code_3=Influence_Code_3.group(1)
             
             #print(StreetNumber)
          else:
             Influence_Code_3=null;

          Assessed_Value =re.search('<b>Assessed Value.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Assessed_Value:
             Assessed_Value=Assessed_Value.group(1)
   
             #print(StreetNumber)
          else:
             Assessed_Value=null


          Influence_Factor_Code_1=re.search('<b>Influence Factor Code 1.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Influence_Factor_Code_1:
             Influence_Factor_Code_1=Influence_Factor_Code_1.group(1)
   
             #print(StreetNumber)
          else:
             Influence_Factor_Code_1=null;
             
          Influence_Factor_Code_2 =re.search('<b>Influence Factor Code 2.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Influence_Factor_Code_2:
             Influence_Factor_Code_2=Influence_Factor_Code_2.group(1)
             #print(StreetNumber)
          else:
             Influence_Factor_Code_2=null;
             
          Influence_Factor_Code_3=re.search('<b>Influence Factor Code 3.*?<font.*?\">(.*?)<',land_table_string,re.DOTALL)
          if Influence_Factor_Code_3:
             Influence_Factor_Code_3=Influence_Factor_Code_3.group(1)
             
             #print(StreetNumber)
          else:
             Influence_Factor_Code_3=null;

          
             
          try:
           wd.find_element_by_link_text('   Improvements').click()
          except:
           print("No land link")

          time.sleep(3)
          improvements_table= wd.page_source
          improvements_table_soup = BeautifulSoup(improvements_table)
          improvements_table_string=improvements_table_soup.decode()

          # Improvements Tab....................">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
         

          improvement_table=re.search('<b>Improvements - Commercial.*?</tr>(.*?)</table>',improvements_table_string,re.DOTALL)
          if improvement_table:
             improvement_table=improvement_table.group(1)

             sk13=" ".join(improvement_table.split())
             improvement_table=sk13
             
             improvement_table_re2=re.compile(r'<td.*?>',re.M | re.I | re.DOTALL)
             improvement_table=improvement_table_re2.sub('\t',improvement_table)
             
             improvement_table_re1=re.compile(r'(<tr>)',re.M | re.I | re.DOTALL)
             improvement_table=improvement_table_re1.sub('\n%s\t%s' % (crawlval,parcel_number.strip()),improvement_table)
              
       
             improvement_table_re3=re.compile(r'(<.*?>)',re.M | re.I | re.DOTALL)
             improvement_table=improvement_table_re3.sub('',improvement_table)
             #print(StreetNumber)
          else:
             improvement_table='';

          
          
          
         
             
          #print(unique_id1)"""
          
          site="Lake"
              
          f = open(r"Lake.txt","a")
          f1 =open(r"Land_table.txt","a")
          f2 =open(r"Improvements_table.txt","a")
 
         
          f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(crawlval,site.strip(),parcel_number.strip(),current_total_value.strip(),date_as_of.strip(),assess_year.strip(),pay_year.strip(),owner.strip(),owner_address.strip(),transfer_date.strip(),taxing_unit.strip(),parcel_address.strip(),township.strip(),Deeded_Acreage.strip(),Section_and_Plat.strip(),Routing_No.strip(),Legal_Desc.strip(),Property_Class_Code.strip(),Neighborhood_Code .strip(),Neighborhood_Factor .strip(),Street_or_Road_Code .strip(),Level_Ground .strip(),assess_year.strip(),High .strip(),Low.strip(),Rolling.strip(),Swampy.strip(),Water.strip(),Sewer.strip(),Natural_Gas.strip(),Electricity .strip(),Sidewalk.strip(),Alley.strip(),Current_Land_Value.strip(),Current_Imp_Value.strip(),Current_Total_Value.strip(),Non_Res_Land .strip(),Non_Res_Imp.strip(),Non_Res_Total.strip(),Dwelling_Value.strip(),Farmland_Value.strip(),Residential_Land.strip(),Residential_Imp.strip(),Residential_Total.strip(),Reason_for_Change.strip(),Prior_Land_Value.strip(),Prior_Imp_Value.strip(),Classified_Land_Value.strip(),Homesite_Value.strip(),Adjustment_Factor.strip(),Average_Value_Acre.strip()))
          f1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (crawlval,parcel_number.strip(),Effective_Frontage.strip(),Effective_Depth.strip(),Acreage.strip(),Square_Footage.strip(),Soil_ID .strip(),Actual_Frontage.strip(),Depth_Factor .strip(),Soil_Productivity_Factor .strip(),Base_Rate.strip(),Influence_Code_1.strip(),Influence_Code_2.strip(),Influence_Code_3.strip(),Assessed_Value.strip(),Influence_Factor_Code_1.strip(),Influence_Factor_Code_2.strip(),Influence_Factor_Code_3.strip()))
          f2.write('%s'% improvement_table.strip())
          
          
     time.sleep(10)
     wd.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[2]/p/font/a/b').click()
     time.sleep(5)   
     try:
        wd.find_element_by_xpath('/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[4]/font/a').click()
        a=1
     except:
        a=2
        break
          
 
#looping   
threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
for thread in threads:
    thread.start();
for thread in threads:
    thread.join() 

stop = datetime.now()
timer = stop-start
time_arr = ["Start Time : " + str(start) + "End Time : " + str(stop)]
time_arr = ["Duration : %s" % str(timer)]
write_excel_file(time_arr, "Scrap Info", 0)

## Send the error log to the mailing function...
atexit.register(mail(sys.stderr.i))
