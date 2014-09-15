
import urllib
#import mysql.connector
import MySQLdb
import os


def CRAWLER2(urlstring1,urlstring2,cursor,tblname):
	connection=urllib.urlopen(urlstring1)
	result=connection.read()

	result_A=result.find('<div class="content">')
	result_B=result.find('<div id="noresult_overlay"></div>',result_A+1)
	totalcontent=result[result_A:result_B]

	result_cut_A=totalcontent.find('<p class="row"')
	result_cut_B=totalcontent.find('</p>',result_cut_A+1)
	content=totalcontent[result_cut_A:result_cut_B]
	print content
	print '\n'

	while (result_cut_A!=-1):
		result_cut_A=totalcontent.find('<p class="row"',result_cut_B+1)
		result_cut_B=totalcontent.find('</p>',result_cut_A+1)
		content=totalcontent[result_cut_A:result_cut_B]
		#print content
		print '\n'
		##Name
		name_a=content.find('class="hdrlnk">',1)
		name_b=content.find('</a>',name_a+1)
		name=content[name_a+15:name_b]
		print name
		#Price
		price_a=content.find('&#x0024;',name_b+1)
		price_b=content.find('</span>',price_a+1)
		price=content[price_a+8:price_b]
		if price_a != -1:
			print price
		else:
			price = 'NA'
			print price
		##Date
		date_a=content.find('<span class="date">',0)
		date_b=content.find('</span>',date_a+1)
		date=content[date_a+19:date_b]
		print date
		##URL
		url_a=content.find('<a href="',0)
		url_b=content.find('"',url_a+10)
		url=content[url_a+9:url_b]
		print urlstring2+url
		print '\n\n'
		url_final= urlstring2+url
		SQLPREPARE="insert into %s (TITLE,PRICE,DATE,URL) values ('%s','%s','%s','%s')"%(tblname,name.replace("'","*"),price,date,url_final)
		#print SQLPREPARE
		cursor.execute(SQLPREPARE)
	return 'FINISH!'
	




def CRAWLER(urlstring1,urlstring2,cursor,tblname):
	connection=urllib.urlopen(urlstring1)
	result=connection.read()

	result_A=result.find('<div class="content">')
	result_B=result.find('<div id="noresult_overlay"></div>',result_A+1)
	totalcontent=result[result_A:result_B]

	result_cut_A=totalcontent.find('<p class="row"')
	result_cut_B=totalcontent.find('</p>',result_cut_A+1)
	content=totalcontent[result_cut_A:result_cut_B]
	#print content
	#print '\n'

	while (result_cut_A!=-1):
		result_cut_A=totalcontent.find('<p class="row"',result_cut_B+1)
		result_cut_B=totalcontent.find('</p>',result_cut_A+1)
		content=totalcontent[result_cut_A:result_cut_B]
		#print content
		#print '\n'
		##Name
		name_a=content.find('class="hdrlnk">',1)
		name_b=content.find('</a>',name_a+1)
		name=content[name_a+15:name_b]
		#print name
		#Price
		price_a=content.find('&#x0024;',name_b+1)
		price_b=content.find('</span>',price_a+1)
		price=content[price_a+8:price_b]
		if price_a != -1:
			price = price
			#print price
		else:
			price = 'NA'
			#print price
		##Date
		date_a=content.find('<span class="date">',0)
		date_b=content.find('</span>',date_a+1)
		date=content[date_a+19:date_b]
		#print date
		##URL
		url_a=content.find('<a href="',0)
		url_b=content.find('"',url_a+10)
		url=content[url_a+9:url_b]
		#print urlstring2+url
		#print '\n\n'
		url_final= urlstring2+url
		try:
			SQLPREPARE="insert into %s (TITLE,PRICE,DATE,URL) values ('%s','%s','%s','%s')"%(tblname,name.replace("'","*"),price,date,url_final)
		    #print SQLPREPARE
			cursor.execute(SQLPREPARE)
		except:
			pass
	return 'FINISH!'



###BEGIN
print 'Executing...'


##Connecting to Google sql service
if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
	cnx = MySQLdb.connect(unix_socket='/cloudsql/kepler-186f-11:yinic-crawler', db='CRAWLER', user='root')
else:
	cnx = MySQLdb.connect(host='173.194.87.70', port=3306, db='CRAWLER', user='root',passwd='password')
cursor = cnx.cursor()
#cnx = mysql.connector.connect(user='root', password='admin',host='localhost',database='CRAWLER',port=8889)
#cnx = mysql.connector.connect(user='root', password='password',host='173.194.87.70',database='CRAWLER',port=3306)
#cursor = cnx.cursor()

print 'Connected...'
search_string='*'
table_string='CRAWLER.YINIC_CRAWLER_CACHE'
#Purge the data
cursor.execute('delete from %s'%table_string)
cnx.commit()
for i in range(0,20):
	print i
	urlstring1="http://kansascity.craigslist.org/search/sss?s=%d&query=%s"%((i*100),search_string)
	urlstring2="http://kansascity.craigslist.org"
	tblname=table_string
	log=CRAWLER(urlstring1,urlstring2,cursor,tblname)
	#print urlstring1



cnx.commit()
cursor.close()
cnx.close()
