

pathPDF = "files/24090330_H.pdf"
pathExcel = "files/Impact_Report_for_CN1080582853.xls"

from errors.error_list import create_file
create_file()


from PDFMain import PDF
list_PDF = PDF(pathPDF)


from ExcelMain import EXCEL
list_Excel = EXCEL(pathExcel)

from Comparison import compare
compare(list_PDF, list_Excel)


#verificar se error_list está vazia