#######Ethan'sFavoriate PYTHON FILE READER >>>r.py'
import sys,os,csv
import urllib

iFile=open('./TPA_small.csv','rU')
jFile=open('Result.csv','w')


def HAN_GOOGLENLP_SERVICE(connection,PRELIST):
	result=connection.read()
	result_A=result.find('<location>')
	result_B=result.find('</location>',result_A+1)
	totalcontent=result[result_A:result_B]
	result_cut_A=totalcontent.find('<lat>')
	result_cut_B=totalcontent.find('</lat>',result_cut_A+1)
	latitude=totalcontent[result_cut_A+5:result_cut_B]
	#print latitude
	result_cut_A=totalcontent.find('<lng>')
	result_cut_B=totalcontent.find('</lng>',result_cut_A+1)
	longtitude=totalcontent[result_cut_A+5:result_cut_B]
	#print longtitude
	PRELIST.append(latitude)
	PRELIST.append(longtitude)
	return PRELIST

##sour=csv.reader(iFile,delimiter=',')
sour=iFile.readlines()
ResultList=[['Person_ID','Orig_Address','latitude','Longtitude']]
for line in sour:
	item=line.split('|')
	PRELIST=[item[0],item[1].replace(',\n','')]
	#print item[0]
	#print item[1]
	print 'Now processing... %s'%item[1]
	connection=urllib.urlopen('https://maps.googleapis.com/maps/api/geocode/xml?address=%s&key=AIzaSyDTHqRL9G_9RbQDD02d_xn2ihg4tB0DBZ8'%item[1])
	ResultList.append(HAN_GOOGLENLP_SERVICE(connection,PRELIST))
	
	
#print ResultList 
	
import csv
with open('SQL.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(ResultList)

iFile.close()
iFile.close()
