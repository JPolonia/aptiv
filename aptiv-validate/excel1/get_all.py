import xlrd
from excel1.AssembliesRevised import get_RevAssemblies
from excel1.DataList import get_DataList

def get_all(path):

    book = xlrd.open_workbook(path)
    sheet_EBOM_DATA = book.sheet_by_name("EBOM Data")
    sheet_IMD = book.sheet_by_name("ITEM MASTER Data")
    dict_RevAssemblies = get_RevAssemblies(sheet_IMD)
    dict_DataList=  get_DataList(sheet_EBOM_DATA)

    return dict_RevAssemblies, dict_DataList