#removing grid lines

from non_used import crop_page as cp
from PyPDF2 import PdfFileWriter, PdfFileReader

def trim(path):
    with open(path, "rb") as in_f:
        input = PdfFileReader(in_f)
        output = PdfFileWriter()
        numPages = input.getNumPages()

        for i in range(1, numPages):
            page = input.getPage(i)
            cp.crop(page, 0, 0, 1500, 1500)
            output.addPage(page)

        with open("files/out.pdf", "wb") as out_f:
            output.write(out_f)