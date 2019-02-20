__author__ = 'perumal'
import sys
import os
import datetime
import time
from time import strftime
import shutil
import random
import time


start = time.time()

print start

now = datetime.datetime.now()
folder_date = now.strftime('%Y%m%d')
outfoldername = 'output'


proxy="31.220.10.23:1212"


os.putenv("http_proxy",proxy)
#os.putenv("https_proxy",proxy)

#time.sleep(10)

#os.system("rm -rf dump")


try:
	shutil.rmtree('dump')
except:
	pass
os.system('mkdir dump')

shutil.copy ('henry.py', 'henry/spiders/henry.py')

sys_call="scrapy crawl henry"
print sys_call

os.system(sys_call)

end = time.time()

print end

total_time = end - start

print total_time
#mv_cmd='mv erie*Output*.csv ../../output_data/erie/'+str(folder_date)+'/'
#print mv_cmd
#os.system(mv_cmd)






