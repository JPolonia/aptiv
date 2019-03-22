def numPages(path):
    from PyPDF2 import PdfFileReader
    pdf_file = open(path, 'rb')
    pdf_reader = PdfFileReader(pdf_file)
    n_pages = PdfFileReader.getNumPages(pdf_reader)
    return n_pages


