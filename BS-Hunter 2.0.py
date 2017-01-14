# -*- coding: utf-8 -*-
import os
from datetime import datetime
from subprocess import PIPE, Popen
import xlwt
import getpass
import ConfigParser

#Constants
#pathToJsFile = r"C:"+os.sep+"Program Files"+os.sep+"nodejs"+os.sep+"test.js"
pathToJsFile = "test.js"
pathToResultFiles = r"C:"+os.sep+"users"+os.sep+getpass.getuser()+os.sep+"Documents"+os.sep
confFile = 'settings LTE.conf'

mcc = ""
mncs = []
lacs = {}
cids = {}
sectors = {}


def initConfigParser(pathToConfFile):
    configParser = ConfigParser.ConfigParser()
    configParser.readfp(open(pathToConfFile))
    return configParser


def initResultFileDescriptor():
    style = xlwt.easyxf('font: name Times New Roman, color-index black, bold on',num_format_str='####')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    currentDate = str(datetime.now()).split(" ")[0]+"_"+str(datetime.now()).split(" ")[1].split(".")[0].replace(":","")
    fileNameToSaveResults = pathToResultFiles+currentDate+".xls"
    return ws,wb,style,fileNameToSaveResults


def readConfigSettings(configParser):
    global mcc
    mcc = configParser.get("mcc","MCC")
    for section in configParser.sections():
        try:
            mnc = configParser.get(section,"MNC")
            mncs.append(mnc)
            lacs[mnc] = configParser.get(section,"LAC").split()
            cids[mnc] = configParser.get(section,"CID").split()
            sectors[mnc] = configParser.get(section, "SECTORS")
        except ConfigParser.NoOptionError, e:
            continue

    #return mcc, mncs, lacs, cids

configParser = initConfigParser(confFile)
ws, wb, style, fileNameToSaveResults = initResultFileDescriptor()

if configParser.get("commonSettings","optUseConfigSettings") == "TRUE":
    readConfigSettings(configParser)
else:
    mcc = raw_input("Enter a 'MCC' value: ")
    mncs = raw_input("Enter a 'MNC' values divided by spaces: ").split()
    for mnc in mncs:
        lacs[mnc] = raw_input("Enter an 'LAC' values for a MNC = "+mnc+", divided by space: ").split()
        cids[mnc] = raw_input("Enter a cid intervals for a MNC = "+mnc+", X-XX Y-YY format: ").split()

columnCount = 0
responseCount = 1
strCount = 1
for mnc in mncs:
    ws.write(0, columnCount, "mnc", style)
    ws.write(0, columnCount+1, "cid", style)
    ws.write(0, columnCount+2, "lac", style)
    ws.write(0, columnCount+3, "lat", style)
    ws.write(0, columnCount+4, "lon", style)
    for lac in lacs[mnc]:
        for cidInterval in cids[mnc]:
            startCid = int(cidInterval.split("-")[0])
            endCid = int(cidInterval.split("-")[1])
            for cid in range(startCid,endCid+1, 256):
                for i in range(0, int(sectors[mnc])):
                    cmd = ["node", pathToJsFile, mcc, mnc, lac, str(cid + i)]
                    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                    p.wait()
                    response = str(p.communicate())
                    response = response.split("\\n")
                    print response[0].split("'")[1]+"; "+response[1]
                    if response[1] != "No response!":
                        lat = response[1].split(" ")[3]
                        lon = response[1].split(" ")[5]
                        ws.write(strCount, columnCount, mnc, style)
                        ws.write(strCount, columnCount+1, cid, style)
                        ws.write(strCount, columnCount+2, lac, style)
                        ws.write(strCount, columnCount+3, lat, style)
                        ws.write(strCount, columnCount+4, lon, style)
                        strCount += 1
                    responseCount += 1
                    if responseCount > 500:
                        wb.save(fileNameToSaveResults)
                        responseCount = 1
    columnCount += 7
    strCount = 1
wb.save(fileNameToSaveResults)
print "Job Done!"
print "File with results: "+fileNameToSaveResults
raw_input("Press ENTER key to exit...")