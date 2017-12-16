
#-*- coding: utf-8 -*-


import sys
import pandas as pd
import requests
import urllib.request
from bs4 import BeautifulSoup
import pymysql
import time
import os

os.environ['http_proxy']=''






def getaptdata(address, yearmonth, key, target ):
	if target == "apt":
		url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD=" + str(address) + "&DEAL_YMD=" + str(yearmonth) +"&serviceKey="+key 
	elif target == "land": 
		url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcLandTrade?LAWD_CD=" +str(address) +"&DEAL_YMD="+str(yearmonth) +"&serviceKey="+key
	elif target == "rent":
		url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent?LAWD_CD=" +str(address) +"&DEAL_YMD="+str(yearmonth) +"&serviceKey="+key
	elif target == "villa":
		url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade?LAWD_CD=" + str(address) +"&DEAL_YMD="+str(yearmonth) +"&serviceKey="+key
	elif target == "villarent":
		url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHRent?LAWD_CD=" + str(address) +"&DEAL_YMD="+str(yearmonth) +"&serviceKey="+key
	elif target == "studio":
		url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiTrade?LAWD_CD=" + str(address) +"&DEAL_YMD="+str(yearmonth) +"&serviceKey="+key
	elif target =="studiorent":
		url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiRent?LAWD_CD=" + str(address) +"&DEAL_YMD="+str(yearmonth) +"&serviceKey="+key

	elif target == "single":
		url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcSHTrade?LAWD_CD=" + str(address) +"&DEAL_YMD="+str(yearmonth) +"&serviceKey="+key
	else:
		startmonth=yearmonth+"01"
		endmonth=yearmonth+"12"
		if target == "landindex":
			url ="http://openapi.kab.co.kr/OpenAPI_ToolInstallPackage/service/rest/LfrPrcIndexSvc/getLfrPrcIndex?startmonth=" + str(startmonth) +"&endmonth="+str(endmonth) + "&region=" + str(address) + "&serviceKey=" + key
		elif target == "aptindex":
			url ="http://openapi.kab.co.kr/OpenAPI_ToolInstallPackage/service/rest/AptRealPrcIndexSvc/getAptRealPrcIndex?startmonth=" + str(startmonth) +"&endmonth="+str(endmonth) + "&region=" + str(address) + "&serviceKey=" + key
		elif target == "rentindex":
			url ="http://openapi.kab.co.kr/OpenAPI_ToolInstallPackage/service/rest/RentPrcIndexSvc/getRentPrcIndex?startmonth=" + str(startmonth) +"&endmonth="+str(endmonth) + "&region=" + str(address) + "&serviceKey=" + key
	print(url)
	try:
		f = urllib.request.urlopen(url)
	except Exception as e:
		print('Fail ' + str(e))
		time.sleep(100)
		f = urllib.request.urlopen(url)

	aptdata2 = f.read().decode("utf8")
	f.close()
	soup = BeautifulSoup(aptdata2, "lxml")

	aptdata = list(aptdata.get_text().replace('\n','').split(">") for aptdata in soup.find_all("item"))
	return(aptdata)

def updateIndexTable(aptdata, conn, target, code):
	try:
		with conn.cursor() as curs:
			for i in aptdata:
				if "index" in target:
					print(i)

					rows = str(i[0]).split('|')
					for i,r in enumerate(rows):
						units = r.split(',') 
						ym=units[0]
						print(ym)
						if i==0:
							code = ym[:5]
							# 수도권
							if code == "A2000":
								area = ym[5:8]
								year = ym[8:12]
								month = ym[12:14]
							# 강북지역, 강남지역
							elif code == "11A01" or code == "11A02":
								area = ym[5:9]
								year = ym[9:13]
								month = ym[13:15]
							else:
								area = ym[5:7]
								year = ym[7:11]
								month = ym[11:13]
						else:
							year = ym[:4]
							month = ym[4:6]
						index = r.split(',')[1]
						date = str(year) + "-" + str(month) + "-01"
						curs.execute("""insert into priceIndex (`year`, `month`, `date`, `areacode`, `areacity`, `indexvalue`, `type`) VALUES ( %s, %s, %s, %s, %s, %s, %s)""", (str(year), str(month), str(date), code, area, str(index), target ))
						print("""insert into priceIndex (`year`, `month`, `date`, `areacode`, `areacity`, `indexvalue`, `type`) VALUES ( %s, %s, %s, %s, %s, %s, %s)""", (str(year), str(month), str(date), code, area, str(index), target ))

			conn.commit()
	except pymysql.InternalError as error:
		code, message = error.args
		print(code)
		print( message)

def updateBasicTable(aptdata, conn):
	try:
		with conn.cursor(pymysql.cursors.DictCursor) as curs:
			for i in aptdata:
				print(i)
				print(len(i))
			conn.commit()
	except pymysql.InternalError as error:
		code, message = error.args
		print(code)
		print( message)

def checkfield(field, landtype):
	try:
		if len(field) == 0:
			return

		if "거래금액" in field:
			value = field[:-4].strip().replace(',', '')
			return ( "price", value)
		elif "보증금" in field:
			value = field[:-3].strip().replace(',', '')
			return ("deposit", value)
		elif "보증금액" in field:
			value = field[:-4].strip().replace(',', '')
			return ("deposit", value)
		elif "월세금액" in field:
			value = field[:-4].strip().replace(',', '')
			return ("rentprice", value)
		elif "월세" in field:
			value = field[:-2].strip().replace(',', '')
			return ("rentprice", value)
		elif "건축년도" in field:
			return ( "constructionyear" , field[:-4] )
		elif len(field) == 5 and "년" in field:
			return ( "year", field[:-1])
		elif "단지" in field and (landtype == "studio" or landtype=="studiorent"):
			return ( "name", field[:-2].strip())
		elif "아파트" in field and (landtype == "apt" or landtype =="rent"):
			return ( "name", field[:-3].strip()) 
		elif "연립다세대" in field:
			return ( "name", field[:-5].strip())
		elif "법정동" in field:
			area = field[:-3].strip()
			if landtype == "apt":
				return ( "area" , area)
			else:
				return ("areadong", area)
		elif "시군구" in field:
			return ( "areagu", field[:-3])
		elif ( len(field) == 2 or len(field) == 3) and "월" in field:
			return ("month", field[:-1])
		elif "1~10일" in field or "11~20일" in field or "21~30일" in field or "21~28일" in field or "21~29일" in field or "21~31일" in field:
			return ("day", field[:-1])
		elif "거래면적" in field:
			return ("landarea", field[:-4].strip().replace(',', ''))
		elif "대지권면적" in field:
			return ("landrightarea", field[:-5])
		elif "대지면적" in field:
			return ("landarea", field[:-4])
		elif "연면적" in field:
			return ("totalgroundarea", field[:-3])
		elif "주택유형" in field:
			return ("housetype", field[:-4])
		elif "전용면적" in field:
			return ("exclusiveusearea", field[:-4])
		elif "지역코드" in field:
			return ("areacode", field[:-4])
		elif ( len(field) == 2 or len(field) == 3 ) and "층" in field:
			return ("floor", field[:-1])	
		elif "지번" in field:
			return ("lotnumber", field[:-2])
		elif "구분" in field:
			return ("shares", field[:-2])
		elif "지목" in field:
			return ("category", field[:-2])
		elif "용도지역" in field:
			return ("subcategory", field[:-4])
		elif "건축유형" in field:
			return ("housetype", field[:-4])
		else:
			print("out of scope:%s", field)  
			return("error", "error")
	except Exception as e:
		print('Fail ' + str(e))
		return ("check field error", "check field error")


def getDate(year, month, day, interval):
	day = day.split('~', 1)[0]
	if interval == "365":
		year = str(int(year) + 1)
	date = year + "-" + month + "-" + day
	return date





def updateTable(aptdata, conn, target):
	try:
		with conn.cursor() as curs:
			for i in aptdata:
				print("\n")
				print(i)
				entry = {}
				for field in i:
					if len(field) == 0:
						continue
					(fieldname, value) = checkfield(field, target)
					entry[fieldname] = value
				if 'error' in entry:
					print("Data error:%s", i)
					continue

				# 데이타 Fetch
				print(curs.rowcount)
				print(curs._last_executed)
				rows = curs.fetchall()
				if curs.rowcount == 0: 
					# insert query here 
					print(curs._last_executed)
					conn.commit()
	except pymysql.InternalError as error:
		code, message = error.args
		print(code)
		print( message)
	except Exception as e:
		print('Update Table Data Error:' + str(e))
 

def getQuery(entry, target):
	insert = "insert into " + "tablename" + "("
	value =  " VALUES ("
	datavalue = []
	for i,unit in enumerate(entry):
		if i == 0:
			insert += "`" + unit +"`"
			value += "%s"
		else:
			insert += ",`" + unit +"`"
			value += ",%s"
		datavalue.append(str(entry[unit]))
	insertvalue = insert + ")" + value + ")"
	datavalues=tuple(datavalue)
	print(insertvalue)
	print(datavalues)
	return(insertvalue, datavalues) 
	

def getDataFrame(aptdata):
	blist1 = []
	blist2 = []
	blist3 = []
	blist4 = []
	blist5 = []
	blist6 = []
	blist7 = []
	blist8 = []
	blist9 = []
	blist10 = []
	blist11 = []

	for i in aptdata:
		blist1.append(i[0][:-4])
		blist2.append(i[1][:-4])
		blist3.append(i[2][:-1])
		blist4.append(i[3][:-3])
		blist5.append(i[4][:-3])
		blist6.append(i[5][:-1])
		blist7.append(i[6][:-1])
		blist8.append(i[7][:-4])
		blist9.append(i[8][:-2])
		blist10.append(i[9][:-4])
		blist11.append(i[10][:-1])

	apt = pd.DataFrame({'건축년도':blist1, '월' : blist2, '법정동':blist3, '년':blist4, '전용면적':blist5, '아파트':blist6, '거래금액':blist7, '일':blist8, '>지번':blist9, '층':blist10, '지역코드':blist11})
	apt.columns = ['일', '거래금액','법정동','년','월','건축년도','전용면적','아파트','지번','층', '지역코드']
	return(apt)


ilocCodes = ["11000", "26000", "27000", "28000", "29000", "30000", "31000", "41000", "42000", "43000", "44000", "45000", "46000" , "47000", "48000", "49000"]

# 전체 코드
clocCodes = [ "11110","11140","11170","11200","11215","11230","11260","11290","11305","11320","11350","11380","11410","11440","11470","11500","11530","11545","11560","11590","11620","11650","11680","11710","11740", "26110", "26140", "26170", "26200", "26230", "26260", "26290", "26320", "26350", "26380", "26410", "26440", "26470", "26500", "26530", "26710", "27110", "27140", "27170", "27200", "27230", "27260", "27290", "27710", "28110", "28140", "28170", "28185", "28200", "28237", "28245", "28260", "28710", "28720", "29110", "29140", "29155", "29170", "29200", "30110", "30140", "30170", "30200", "30230", "31110", "31140", "31170", "31200", "31710", "36110",  "41111", "41113", "41115", "41117", "41131", "41133", "41135", "41150", "41171", "41173", "41190", "41210", "41220", "41250", "41271" , "41273", "41281", "41285", "41287", "41290", "41310","41360","41370","41390","41410","41430","41450","41461", "41463","41465","41480","41500","41550","41570","41590","41610","41630","41650","41670","41800","41820","41830", "42110","42130","42150","42170","42190","42210","42230","42720","42730","42750","42760","42770","42780","42790","42800","42810","42820","42830","43111","43112","43113","43114","43130","43150","43720","43730","43740","43745","43750","43760","43770","43800","44131","44133","44150","44180","44200","44210","44230","44250","44270","44710","44760","44770","44790","44800","44810","44825" , "45111","45113","45130","45140","45180","45190","45210","45710","45720","45730","45740","45750","45770","45790","45800","46110","46130","46150","46170","46230","46710","46720","46730","46770","46780","46790","46800","46810","46820","46830","46840","46860","46870","46880","46890","46900","46910", "47111","47113","47130","47150","47170","47190","47210","47230","47250","47280","47290","47720","47730","47750","47760","47770","47820","47830","47840","47850","47900","47920","47930","47940","48121","48123","48125","48127","48129","48170","48220","48240","48250","48270","48310","48330","48720","48730","48740","48820","48840","48850","48860","48870","48880","48890", "50110", "50130"]

years = [    "2006",  "2007", "2008", "2009", "2010","2011", "2012", "2013", "2014",  "2015", "2016", "2017" ]
months = [ "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
conn = pymysql.connect(host='localhost', user='userid', password='userpwd',
                       db='dbname', charset='utf8')
print(len(sys.argv))
key = "add key here"


if len(sys.argv) == 4:
	target=sys.argv[1]
	code=sys.argv[2]
	period=sys.argv[3]

	if len(period) == 6:
		print("get data by yearmn")
		aptdata=getaptdata(code,period, key, target)
		updateTable(aptdata, conn, target)
	elif len(period) == 4:
		print("get data by year")
		for m in months:
			ym = str(period)+m
			aptdata=getaptdata(code,ym, key, target)
			updateTable(aptdata, conn, target)
	else:
		print("usage: code period")
elif len(sys.argv) ==3:
	target = sys.argv[1]
	code=sys.argv[2]
	for y in years:
		for m in months:
			ym = str(y)+m
			aptdata=getaptdata(code,ym, key, target)
			updateTable(aptdata, conn, target)
elif len(sys.argv) ==2:
	target = sys.argv[1]
	print(target)
	years = [  "2017" ]
	months = [  "10", "11", "12"]
	locCodes = clocCodes
	if "index" in target:  
		if target == "rentindex":
			ilocCodes = [ "A2000", "11000", "11A01", "11A02", "41000", "28000", "26000", "27000", "29000", "30000", "31000"]

		for code in ilocCodes:
			for y in years:
				key = "H**D"
				aptdata=getaptdata(code, y, key, target)
				updateIndexTable(aptdata, conn, target, code) 
				time.sleep(5)


	else:
		for code in locCodes:
			for y in years:
				for m in months:
					ym = str(y)+m
					aptdata=getaptdata(code,ym, key, target)
					updateTable(aptdata, conn, target)
				time.sleep(1)
			time.sleep(1)
else:
	print("usage: target code period(Ym or Y) / target code / target ")
conn.close()
