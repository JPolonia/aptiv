#from utilities import *
import zipfile
import os

#pdf = "files/24090330_H.pdf"
#xls = "files/Impact_Report_for_CN1080582853.xls"
pathZip = "files/Arquivo.zip"
list_Files=[]

list_Files.append(pathZip)

pdf = False
xls = False
zip = False

for file in range(len(list_Files)):
    if list_Files[file].endswith(".pdf"):
        pdf = list_Files[file]
    if list_Files[file].endswith(".xls"):
        xls = list_Files[file]
    if list_Files[file].endswith(".zip"):
        zip = list_Files[file]

#create_ErrorFile()

if zip:
    zip_ref = zipfile.ZipFile(zip, 'r')
    zip_ref.extractall("files")
    zip_ref.close()
    for fname in os.listdir('files'):
        if fname.endswith('.pdf'):
            pdf = "files/" + fname
        elif fname.endswith('.xls'):
            xls = "files/" + fname
        if pdf and xls:
            break

from test import processPDF
#if pdf:
processPDF(pdf)
#if xls:
myExcel = classExcel(xls)
myExcel.writeJSON()
#if xls and pdf:
compare("files/InfoPDF.json", "files/InfoExcel.json")



#noErrors()


