x = {"SM1" : { "assembly1" : { "partnumber1" : {"qty" : 1,
                                              "description" : "string"},
                            "partnumber2" : {"qty" : 1,
                                              "description" : "string"}},
               "assembly2" : { "partnumber1" : {"qty" : 1,
                                                              "description" : "string"},
                                            "partnumber2" : {"qty" : 1,
                                                              "description" : "string"}}
}}






#retrieve assembly_rev_list
from non_used.assembly_revised import get_assemblyLocals
assemblyList = get_assemblyLocals(rev_letter, pages[0][3])  #vai bucar as assemblies à tabela 3 da pagina 0



#first error check
from non_used.error_check import check_assemblies_PDF_Excel
check_assemblies_PDF_Excel(assemblyList,{"SM1" : [10293], "SM2" : [9384], "HP1" : [3043]}, path_error)


# get assembly list for each place index 0 = SM1... each list item is an array containing the partnumbers
from PDF2.vertical_assembly import retrieve_data
checkAssemblyList = retrieve_data(path, pages)

from non_used import data_analysis as da

#get collumns to check
columns = da.columns(pages[0][3], assemblyList, checkAssemblyList)

#retrive list with separeted data
from PDF2.data_list import select_data
data_list = select_data(pages)


#retrives dictionary for all pages
for i in range(len(data_list)):
    componentDictionary = {}
    componentDictionary  = da.check_all(data_list[i], componentDictionary, columns(key), n_assemblys= len(checkAssemblyList[i]))



pass