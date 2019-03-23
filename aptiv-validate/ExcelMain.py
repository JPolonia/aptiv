
def EXCEL(path):
    #stage 1 - collect assemblies revised and collect independent tables
    from excel1.get_all import get_all
    dict_RevAssemblies, dict_DataList = get_all(path)
    pass


    #stage 2 - Checks coherence between ITEM MASTER Data and EBOM Data.
    from excel2.Check_Coherence import check
    check(dict_RevAssemblies, dict_DataList)


    #stage 3 - Checks if all the needed components in CMP are in place (DWG,EDD and SCHEMATIC), retrieves and filters Part Numbers, getting the final dictionary to compare with PDF File.
    from excel3.CMP_Needs import  checkCMP
    from excel3.final_dictionary import final_dict
    checkCMP(dict_DataList)
    dict_Partnumbers, dict_AdditionalFeatures = final_dict(dict_DataList)
    pass


    import json
    f = open("files/ExcelPartnumbers.json", "w+")
    f.write(json.dumps(dict_Partnumbers, indent=4, sort_keys=True))
    f = open("files/ExcelAdditionalFeatures.json", "w+")
    f.write(json.dumps(dict_AdditionalFeatures, indent=4, sort_keys=True))
    pass

    list_Excel = []
    list_Excel.append(dict_Partnumbers)
    list_Excel.append(dict_AdditionalFeatures)

    return list_Excel
