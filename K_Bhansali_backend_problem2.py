#!/usr/bin/env python

#
# Web scraping
# ASNs (Autonomous System Numbers) are one of the building blocks of the
# Internet. This project is to create a mapping from each ASN in use to the
# company that owns it. For example, ASN 36375 is used by the University of
# Michigan - http://bgp.he.net/AS36375
# 
# The site http://bgp.he.net/ has lots of useful information about ASNs. 
# Starting at http://bgp.he.net/report/world crawl and scrape the linked country
# reports to make a structure mapping each ASN to info about that ASN.
# Sample structure:
#   {3320: {'Country': 'DE',
#     'Name': 'Deutsche Telekom AG',
#     'Routes v4': 13547,
#     'Routes v6': 268},
#    36375: {'Country': 'US',
#     'Name': 'University of Michigan',
#     'Routes v4': 14,
#     'Routes v6': 1}}
#
# When done, output the collected data to a json file.
#
# Use any python libraries. One suggestion, a good one for scraping is
# BeautifulSoup:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
# 

import urllib2
# Get beautifulsoup4 with: pip install beautifulsoup4
import bs4
import json


result = {}

# To help get you started, here is a function to fetch and parse a page.
# Given url, return soup.
def urls_from_main(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html,"html.parser")
    links = soup.select('td a')
    data_from_report(links)

def data_from_report(urls):
	for url in urls:
		link = url['href']
		country = link[link.rfind('/')+1:]
		generate_output(link,country)

def generate_output(url,country):
	global result
	baseurl = "http://bgp.he.net" + url
	print baseurl
	req = urllib2.Request(baseurl, headers={ 'User-Agent': 'Mozilla/5.0' })
	html = urllib2.urlopen(req).read()
	soup = bs4.BeautifulSoup(html,"html.parser")

	rows = soup.find_all("tr")
	
	for row in rows:
		datalist = row.find_all("td")
		count = 0
		asn = 0
		for d in datalist:
			if count == 0:
				asn_num = d.find("a").string[2:]
				#json doesnt allow integer keys
				asn = str(asn_num)
				result[asn] = {}
				result[asn]["Country"] = str(country)
				count += 1
			else:
				if count == 1:
					temp = d.string
					if temp:
						result[asn]["Name"] = temp.encode('utf-8')
				elif count == 3:
					result[asn]["Routes v4"] = int(d.string.replace(',',''))
				elif count == 5:
					result[asn]["Routes v6"] = int(d.string.replace(',',''))
				count += 1
	



urls_from_main("http://bgp.he.net/report/world")

with open("Results.json","w") as f:
    json.dump(result,f)