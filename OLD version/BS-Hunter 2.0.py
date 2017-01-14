# -*- coding: utf-8 -*-
import os
from datetime import datetime
from subprocess import PIPE, Popen
import xlwt
import getpass

# def sanitizeList(list):
#     for item in list:
#         if item == "" || item == " ":
#

mcc=[]
mncs=[]
lacs={}
cids={}

pathToJsFile = r"C:"+os.sep+"Program Files"+os.sep+"nodejs"+os.sep+"test.js"
pathToResultFiles = r"C:"+os.sep+"users"+os.sep+getpass.getuser()+os.sep+"Documents"+os.sep

style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on',num_format_str='####')
wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

mcc = raw_input("Enter a 'MCC' value: ")
mncs = raw_input("Enter a 'MNC' values divided by spaces: ").split()
# for mnc in mncs:
#     if mnc == "":
#         mncs.remove(mnc)

for mnc in mncs:
    lacs[mnc] = raw_input("Enter a 'LAC' values for a MNC = "+mnc+", divided by space: ").split()
    cids[mnc] = raw_input("Enter a cid intervals for a MNC = "+mnc+", X-XX Y-YY format: ").split()

currentDate = str(datetime.now()).split(" ")[0]+"_"+str(datetime.now()).split(" ")[1].split(".")[0].replace(":","")
fileNameToSaveResults = pathToResultFiles+currentDate+".xls"

columnCount = 0
responseCount = 1
strCount = 1
for mnc in mncs:
    ws.write(0, columnCount, "mnc", style0)
    ws.write(0, columnCount+1, "cid", style0)
    ws.write(0, columnCount+2, "lac", style0)
    ws.write(0, columnCount+3, "lat", style0)
    ws.write(0, columnCount+4, "lon", style0)
    for lac in lacs[mnc]:
        for cidInterval in cids[mnc]:
            startCid = int(cidInterval.split("-")[0])
            endCid = int(cidInterval.split("-")[1])
            for cid in range(startCid,endCid+1):
                cmd = ["node",pathToJsFile, mcc, mnc,lac,str(cid)]
                p = Popen(cmd,stdout=PIPE,stderr=PIPE, shell=True)
                p.wait()
                response = str(p.communicate())
                response = response.split("\\n")
                print response[0].split("'")[1]+"; "+response[1]
                if response[1] != "No response!":
                    lat = response[1].split(" ")[3]
                    lon = response[1].split(" ")[5]
                    ws.write(strCount, columnCount, mnc, style0)
                    ws.write(strCount, columnCount+1, cid, style0)
                    ws.write(strCount, columnCount+2, lac, style0)
                    ws.write(strCount, columnCount+3, lat, style0)
                    ws.write(strCount, columnCount+4, lon, style0)
                #else:
                    # lat = "-"
                    # lon = "-"
                    # ws.write(strCount, columnCount, mnc, style0)
                    # ws.write(strCount, columnCount+1, cid, style0)
                    # ws.write(strCount, columnCount+2, lac, style0)
                    # ws.write(strCount, columnCount+3, lat, style0)
                    # ws.write(strCount, columnCount+4, lon, style0)
                    strCount += 1
                responseCount += 1
                if responseCount > 500:
                    wb.save(fileNameToSaveResults)
                    responseCount = 1
        #ws.write(strCount, columnCount, "", style0)
        #strCount += 1
    columnCount += 7
    strCount = 1
wb.save(fileNameToSaveResults)
print "Job Done!"
print "File with results: "+fileNameToSaveResults
raw_input("Press ENTER key to exit...")