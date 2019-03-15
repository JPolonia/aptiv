import PyPDF2

pdfFileObj = open('files/24090330_H.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)
df=pageObj.extractText()
print(df)

