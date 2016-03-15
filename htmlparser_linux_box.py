from lxml import html
import requests
from urllib2 import urlopen
import os

foldername = 'nsw_data_current'
filename = 'current_nsw_data.csv'

if os.path.exists("~/property/"+foldername):
    os.chdir("~/property/"+foldername)
else:
    os.chdir("~/property/")    
    os.system('mkdir '+foldername)
    os.chdir("~/property/"+foldername)

if os.path.isfile(filename):
    os.remove(filename)
    output = open(filename, 'w')
else:
    output = open(filename, 'wb')

pagelink = 'http://globe.six.nsw.gov.au/csv/current/'

def getcsv(pagelink):        
    csv_ind = 0   
    page = requests.get(pagelink)
    tree = html.fromstring(page.content)
    linknodes = tree.xpath('//a[@href]/text()')        
    
    for link in linknodes:
        if link[-3:] == "csv":
            csv_ind = 1
    
    if csv_ind == 1:
        for link in linknodes:
            if link[-3:] == "csv":
                csvname = link.strip()                
                url = pagelink + csvname        
                csvfile = urlopen(url)
                output.write(csvfile.read())

    else:
        for link in linknodes:
            if link.strip() != 'Parent Directory':
                pagelink2 = pagelink + link.strip()                
                getcsv(pagelink2)

getcsv(pagelink)
output.close()