from errors.error_list import add_error_item


def checkCMP(dict_DataList):
    if dict_DataList["CMP"] != {}:
        retrieveData(dict_DataList["CMP"])






def retrieveData(dict_CMPAssemblies):
    for assembly in dict_CMPAssemblies:
        edd, dwg, schematic = get_Features(dict_CMPAssemblies[assembly])
        if edd != "" or dwg != "" or schematic != "":
            error = "Assembly: " + assembly + " => CMP is missing " + edd + " " +  dwg + " " + schematic
            add_error_item(error)


def get_Features(list_assemblies):  # número part number

    edd = "EDD"
    dwg = "DWG"
    schematic = "SCHEMATIC"
    for part in list_assemblies:
        partnumber =list_assemblies[part][1]
        description = list_assemblies[part][3]
        if "EDD" in partnumber:
            edd = ""
        elif "DWG" in partnumber:
            dwg = ""
        elif "SCHEMATIC" in description:
            schematic = ""
    return edd, dwg, schematic

