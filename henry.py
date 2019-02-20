__author__ = 'perumal'
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request, Response, HtmlResponse, XmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
import os
import re
import time
import datetime
import sys
import csv
import HTMLParser
import math
# import erie
import random
from bs4 import BeautifulSoup as Bs
# import erie
import TableParser as tp

request_headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'en-US,en;q=0.8','Connection':'keep-alive','Cookie':'PHPSESSID=660bbebbab97174ee8ad832beded507b; __cfduid=d87afc050ab3e4e9bae44495899df8fa41443689634; QPMAP_REPORTS_WIDTH=300; QPMAP_CONTROLS_WIDTH=200; __utma=106997826.6988934.1443164197.1444652209.1444711249.37; __utmb=106997826.9.10.1444711249; __utmc=106997826; __utmz=106997826.1443164197.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','Host':'qpublic7.qpublic.net','Referer':'http\':\'//www.qpublic.net/ga/henry/search.html','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}


def write_excel_file(arr, sheet_name):
    fp = open(sheet_name + ".txt", 'a')
    for i in arr:
        fp.write(str(i) + "\t")
    fp.write("\n")
    fp.close()


def multi_delete(list_, *args):
    indexes = sorted(list(args), reverse=True)
    # print indexes
    for index in indexes:
        del list_[index]
    return list_


class henry(BaseSpider):
    name = 'henry'
    start_urls = ['http://www.qpublic.net/ga/henry/search.html']
    # start_urls = ['http://www.ipchicken.com']



    def __init__(self, name=None, **kwargs):

        self.now = datetime.datetime.now()
        Primary_header = ['Sitename', 'Owner Name','Today Date', 'Mailing Address', 'Parcel Number', 'Millage Group', 'Total Millage ', 'Location Address', 'Property Usage ', 'Total Acres ', 'Landlot / District', 'Subdivision Name', 'Subdivision Lot/Block', 'Plat Book ', 'Plat Page']
        write_excel_file(Primary_header, 'Primary')
        value_information_header = ['ParcelNumber','Owner', 'LandValue', 'BuildingValue',
                                    'Misc Value ', 'Total Value ', 'Exemptions ']
        write_excel_file(value_information_header, 'value_information')
        Land_Information_header = ['ParcelNumber','Owner',  'LandUse', 'NumberUnits', 'UnitType']
        write_excel_file(Land_Information_header, 'Land_Information')
        Sale_Information_header = ['ParcelNumber', 'owner', 'Sale Date',  'Deed Book ', 'Price', 'Instrument',
                                   'Reason', 'Grantor', 'Grantee']
        write_excel_file(Sale_Information_header, 'Sale Information')
        Miscellaneous_Information_header = ['ParcelNumber','Owner',  'Description', 'Length', 'Width', 'Units', 'Year Built']
        write_excel_file(Miscellaneous_Information_header, 'Miscellaneous Information')
        Building_Information_header = ['ParcelNumber', 'Owner',  'Building ', 'Type', 'Effective Area ', 'HeatedArea ', 'BedRooms', 'Baths', 'Wall Height ', 'Actual Year Built ']
        write_excel_file(Building_Information_header, 'Building Information')


        self.link = "http://qpublic7.qpublic.net/"
        self.nxt_link = "http://qpublic7.qpublic.net/ga_henry_alsearch.php"
        self.init_reqs = []
        self.all_links = []
        self.reqs = []
        self.search = 50
        # self.crawl_no = 1
        self.sitename = "henry"

    def parse(self, response):

        # f=open("dump/mainpage.html","w")
        # f.write(response.body)
        # f.close()

        try:

            url = "http://qpublic7.qpublic.net/ga_henry_search.php"

            req = Request(url=url, headers=request_headers, dont_filter=True, callback=self.next_page1)

            return req

        except:
            print "error1"
            pass

    def next_page1(self, response):

        # f=open("dump/mainpage.html","w")
        # f.write(response.body)
        # f.close()

        try:

            url = "http://qpublic7.qpublic.net/ga_henry_search.php?county=ga_henry&type=name"

            req = Request(url=url, headers=request_headers, dont_filter=True, callback=self.next_page3)

            return req

        except:
            print "error2"
            pass


    def next_page3(self, response):

        # f=open("dump/search.html","w")
        # f.write(response.body)
        # f.close()

        inputs = ['T']

        random.shuffle(inputs)

        for val in inputs:
            search_url = "http://qpublic7.qpublic.net/ga_henry_alsearch.php"

            req = FormRequest(url=search_url,
                              formdata={'BEGIN':'0', 'INPUT':val, 'searchType':'owner_name','county':'ga_henry','Owner_Search':'Search By Owner Name'}, headers=request_headers,
                              dont_filter=True, callback=self.next4)

            req.meta['search_word'] = val

            self.init_reqs.append(req)

        return self.init_reqs

    def next4(self, response):

        # f=open("dump/results_"+response.meta['search_word']+"_page_num_"+str(response.meta['page_num'])+".html","w")
        # f.write(response.body)
        # f.close()

        data = response.body
        soup = Bs(data, "lxml")
        htmlstring = soup.decode()
        #print htmlstring

        dissect_url = re.compile(r'<td.class="cell_value".nowrap="">.<a.href="(.*?)"', re.M | re.I | re.DOTALL)
        print "hi"
        # self.all_links = []
        for dis1 in re.findall(dissect_url, htmlstring):
            print dis1
            dis2 = dis1.replace("&amp;", "&")
            # dissect_letter = re.search(r'=.*?=(..)', dis1, re.DOTALL)
            # if dissect_letter.group(1) != "PB":
            self.all_links.append(dis2)
            #print self.all_links

        if 'Search Next 50 Parcels' in data:
            print "going to next page......"

            req = FormRequest(url=self.nxt_link, formdata={'BEGIN':str(self.search),'INPUT':response.meta['search_word'],'searchType':'owner_name','owner_name':'Search Next 50 Parcels'},headers=request_headers, dont_filter=True, callback=self.next4)

            # req.meta['page_num'] = int(response.meta['page_num']) + 1
            #
            req.meta['search_word'] = response.meta['search_word']
            self.search += 50

            return req

        else:

            req_links = []

            while self.all_links != []:
                # for link_page in self.all_links:
                # print self.all_links[0]
                req = Request(url=self.link+self.all_links[0], dont_filter=True, callback=self.links)
                # yield Request(url=self.all_links[0], dont_filter=True, callback=self.links)
                # req.meta['cnt'] = cnt
                req.meta['search_word'] = response.meta['search_word']
                # req.meta['page_num'] = int(response.meta['page_num'])

                # cnt += 1
                self.all_links.remove(self.all_links[0])
                # print self.all_links
                req_links.append(req)

            return req_links

    def links(self, response):

        # f=open("dump/link_"+str(response.meta['cnt'])+".html","w")
        # f.write(response.body)
        # f.close()

        data = response.body
        soup1 = Bs(data, "lxml")
        html = soup1.decode()
        # data=response.body.replace('\n','').replace('\t','').replace('\r','').strip()




        Parcel_Information = re.search('Owner and Parcel Information.*?</tr>(.*?)</table>', html, re.DOTALL)
        Location_Address = re.search('Location Address.*?">(.*?)</td>', html, re.DOTALL)
        Millage_Rate = re.search('Millage Rate.*?">(.*?)</td>', html, re.DOTALL)
        Owner = re.search('Owner Name .*?">(.*?)</td>', html, re.DOTALL)
        Owner = Owner.group(1).replace("&amp;", '&')
        sk5=" ".join(Owner.split())
        Owner=sk5
        Owner_re2=re.compile(r'<.*?>',re.M | re.I | re.DOTALL)
        Owner=Owner_re2.sub('',Owner)
        #Parcel_number = re.search('Parcel Number .*?">(.*?)</td>', html, re.DOTALL)
        #Parcel_number = Parcel_number.group(1).strip()
        # print Parcel_Information.group(1)
        Parcel_Information_val = tp.process_html_table(Parcel_Information.group(1))
        Parcel_number = Parcel_Information_val[1][3]
        #print Parcel_Information_val
        #print Parcel_number
        Parcel_Information_arr = [self.sitename]
        # while (i < len(val)):
        for i in range(0, len(Parcel_Information_val)):
            Parcel_Information_arr.extend((Parcel_Information_val[i][1], Parcel_Information_val[i][3]))
        #print Parcel_Information_arr
        Parcel_Information_arr[3:4] = [','.join(Parcel_Information_arr[3:6:2])]
        #print Parcel_Information_arr
        Parcel_Information_arr = multi_delete(Parcel_Information_arr, 5, 7, 11, 14)
        #print Parcel_Information_arr
        # Parcel_Information_arr.extend([Location_Address.group(1).strip(), Millage_Rate.group(1).strip()])
        # print Parcel_Information_arr
        write_excel_file(Parcel_Information_arr, "Primary")
        print Owner.strip()

        try:

            value_information = re.search('January 1, 2015 Value Information .*?</tr>(.*?)</table>', html, re.DOTALL)
            # print value_information.group(1)
            value_information_val = tp.process_html_table(value_information.group(1))
            # print value_information_val
            # value_information_arr = [site_name,Parcel_number,Owner.strip()]
            for i in range(1, len(value_information_val)):
                value_information_arr = [Parcel_number, Owner.strip()]
                value_information_arr.extend((value_information_val[i][0], value_information_val[i][1],
                                              value_information_val[i][2], value_information_val[i][3],
                                              value_information_val[i][4]))
                # print value_information_arr
                write_excel_file(value_information_arr, "value_information")

        except:
            print "Value table not found"

        try:

            Land_Information = re.search('Land Information.*?</tr>(.*?)</table>', html, re.DOTALL)
            #print Land_Information.group(1)
            Land_Information_val = tp.process_html_table(Land_Information.group(1).strip())
            # print Land_Information_val
            # Land_Information_arr = [crawl_no,site_name,Parcel_number]
            for i in range(1, len(Land_Information_val)):
                Land_Information_arr = [Parcel_number, Owner.strip()]
                #print Land_Information_arr
                Land_Information_arr.extend((Land_Information_val[i][0], Land_Information_val[i][1],
                                             Land_Information_val[i][2]))
                #print Land_Information_arr
                write_excel_file(Land_Information_arr, "Land_Information")
        except:
            print "Land table not found"

        try:

            Sale_Information = re.search('Sale Information.*?</tr>(.*?)</table>', html, re.DOTALL)
            # print Accessory Information.group(1)
            Sale_Information_val = tp.process_html_table(Sale_Information.group(1))
            # print Sale_Information_val
            # Accessory Information_arr = [crawl_no,site_name,Parcel_number]
            if (Sale_Information_val[1][6].strip() == " No sales information associated with this parcel. "):
                print "Sale table not found"
            else:

                for i in range(1, len(Sale_Information_val)):
                    Sale_Information_arr = [Parcel_number, Owner.strip()]
                    Sale_Information_arr.extend((Sale_Information_val[i][0], Sale_Information_val[i][1],
                                                 Sale_Information_val[i][2], Sale_Information_val[i][3],
                                                 Sale_Information_val[i][4], Sale_Information_val[i][5],
                                                 Sale_Information_val[i][6]))
                    # print Sale_Information_arr
                    write_excel_file(Sale_Information_arr, "Sale Information")

        except:
            print "Sale table not found"
        #
        try:

            Miscellaneous_Information = re.search('Miscellaneous Data.*?</tr>(.*?)</table>', html, re.DOTALL)
            # print Accessory Information.group(1)
            Miscellaneous_Information_val = tp.process_html_table(Miscellaneous_Information.group(1))
            #print Miscellaneous_Information_val
            # Accessory Information_arr = [crawl_no,site_name,Parcel_number]
            if (Miscellaneous_Information_val[1][
                    4].strip() == "No records associated with this parcel."):
                print "Miscellaneous table not found"
            else:
                for i in range(1, len(Miscellaneous_Information_val)):
                    Miscellaneous_Information_arr = [Parcel_number, Owner.strip()]
                    #print Miscellaneous_Information_arr
                    Miscellaneous_Information_arr.extend(
                        (Miscellaneous_Information_val[i][0], Miscellaneous_Information_val[i][1],
                         Miscellaneous_Information_val[i][2], Miscellaneous_Information_val[i][3], Miscellaneous_Information_val[i][4]))
                    # print Miscellaneous_Information_arr
                    write_excel_file(Miscellaneous_Information_arr, "Miscellaneous Information")
        except:
            print "Miscellaneous table not found"

        try:

            Building_Information = re.search('Building Data.*?</tr>(.*?)</table>', html, re.DOTALL)
            # print Accessory Information.group(1)
            Building_Information_val = tp.process_html_table(Building_Information.group(1))
            #print Building_Information_val[1][7]
            # Accessory Information_arr = [crawl_no,site_name,Parcel_number]
            if (Building_Information_val[1][
                    7].strip() == "No buildings associated with this parcel."):
                print "Building table not found"
            else:
                for i in range(1, len(Building_Information_val)):
                    Building_Information_arr = [Parcel_number, Owner.strip()]
                    #print Building_Information_arr
                    Building_Information_arr.extend(
                        (Building_Information_val[i][0], Building_Information_val[i][1],
                         Building_Information_val[i][2], Building_Information_val[i][3], Building_Information_val[i][4], Building_Information_val[i][5], Building_Information_val[i][6], Building_Information_val[i][7]))
                    # print Building_Information_arr
                    write_excel_file(Building_Information_arr, "Building Information")
        except:
            print "Building table not found"

