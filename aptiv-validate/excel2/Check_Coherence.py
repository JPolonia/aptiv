from errors.error_list import add_error_item

def check(dict_RevAssemblies, dict_DataList):
    for mount in dict_RevAssemblies:
        for assembly in dict_RevAssemblies[mount]:
            if not assembly in dict_DataList[mount]:
                error = "Error: Assembly: " + str(assembly) + " , " + str(mount) + " from ITEM MASTER Data is not present in " + str(mount) + " in EBOM Data"
                add_error_item(error)




