from errors.error_list import create_file
from PDFMain import PDF
from ExcelMain import EXCEL
from Comparison import compare

pathPDF = "files/24090330_H.pdf"
pathExcel = "files/Impact_Report_for_CN1080582853.xls"

# def RetrieveData(pathPDF, pathExcel):

create_file()

list_PDF = PDF(pathPDF)

list_Excel = EXCEL(pathExcel)

compare(list_PDF, list_Excel)

#verificar se error_list está vazia

