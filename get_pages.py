from get_n_pages import numPages
import pdf_to_tabula as ptt
from check_pages import check

def getPages(path):
    n_pages = numPages(path)
    pages=[]   #list that stores pages
    pages.append(ptt.pdf_to_tb(path,1))
    pages[0].append(ptt.pdf_to_tb_area(path, 1, 73.01,1743.3,1682.21,2363.14)) #retira info da tabela das datas
    for x in range(2, n_pages +1):
        page = ptt.pdf_to_tb_area(path,x, 34.27,32.78,1649.43,2360.16) #retira informação dentro dos limites da grelha
        page = check(page)
        pages.append(page)
    return pages


