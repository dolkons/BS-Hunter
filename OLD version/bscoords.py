# -*- coding: utf-8 -*-
import os
from datetime import datetime
from subprocess import PIPE, Popen
import csv
import xlwt
import getpass

pathToJsFile = r"C:"+os.sep+"Program Files"+os.sep+"nodejs"+os.sep+"test.js"
pathToResultFiles = r"C:"+os.sep+"users"+os.sep+getpass.getuser()+os.sep+"Documents"+os.sep

style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on',
    num_format_str='####')
wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')
# ws.write(0, 0, "cid", style0)
# ws.write(0, 1, "lac", style0)
# ws.write(0, 2, "Response", style0)
# ws.write(0, 3, "lat", style0)
# ws.write(0, 4, "lon", style0)

mcc = raw_input("Enter a 'MCC' value: ")
mnc = raw_input("Enter a 'MNC' value: ")
lacs = raw_input("Enter a 'LAC' values, divided by space: ").split(" ")
startCid = int(raw_input("Enter a Start of Cid interval: "))
endCid = int(raw_input("Enter a End of Cid interval: "))
strCount = 1

currentDate = str(datetime.now()).split(" ")[0]+"_"+str(datetime.now()).split(" ")[1].split(".")[0].replace(":","")
fileNameToSaveResults = pathToResultFiles+currentDate+".xls"

lacCount = 0
for lac in lacs:
    ws.write(0, lacCount, "cid", style0)
    ws.write(0, lacCount+1, "lac", style0)
    ws.write(0, lacCount+2, "Response", style0)
    ws.write(0, lacCount+3, "lat", style0)
    ws.write(0, lacCount+4, "lon", style0)
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
            responseResult = "+"
        else:
            lat = "-"
            lon = "-"
            responseResult = "-"
        ws.write(strCount, lacCount, cid, style0)
        ws.write(strCount, lacCount+1, lac, style0)
        ws.write(strCount, lacCount+2, responseResult, style0)
        ws.write(strCount, lacCount+3, lat, style0)
        ws.write(strCount, lacCount+4, lon, style0)
        wb.save(fileNameToSaveResults)
        strCount += 1
    lacCount += 6
    strCount = 1
print "Job Done!"
print "File with results: "+fileNameToSaveResults
raw_input("Press ENTER key to exit...")