import re
import PyPDF2
from dim1_parse_pages import pdf_to_tabula as parse


#rotates all pdf pages
def rotate(path, path_out, degrees):
    pdf_in = open(path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        page.rotateClockwise(degrees)
        pdf_writer.addPage(page)

    pdf_out = open(path_out, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()



#gets an array of assemblies that will correspond to a mount
def getList(path,pagenum):
    page = parse.pdf_to_tb_area(path, pagenum, 28.418,1444.03,2352.338,1652.425) #retrieves by area

    assemblyArray = []
    aux = True
    i = 0
    while aux:
        assemblyArray.append(page[0][0][i])
        number = page[0][0][i+1]
        if not type(number) == float:  # drop all float values… … but only if they are nan
            if not re.match('\d{5,}', number): #checks if string has 5 digits or more, if not it ends the cycle
                aux = False
        else:
            aux = False
        i +=1

    return assemblyArray



#agreggates the assemblies arrays in a list
def retrieve_data(path, pages):
    path_out = 'files/rotated.pdf'
    rotate(path,path_out, 90)


    checkAssembly_list = []
    for pagenum in range(len(pages)-1, 1, -1):
        if pages[pagenum] == "ignore":
            if not pages[pagenum - 1] == "ignore":
                checkAssembly_list.append(getList(path_out, pagenum))

    checkAssembly_list.reverse()
    return checkAssembly_list

