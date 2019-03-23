def get_RevAssemblies(sheet):
    dict_RevAssembly = {"SM1" : {}, "SM2" : {}, "HP1" : {}, "CMP" : {}}
    n_rows = sheet.nrows
    for row in range(7, n_rows): #table starts at line 7
        name = sheet.cell(row, 0).value
        assembly = get_assembly(name)
        item_name = sheet.cell(row, 1).value
        if "SM1" in item_name:
            dict_RevAssembly["SM1"][assembly] = item_name
        elif "SM2" in item_name:
            dict_RevAssembly["SM2"][assembly] = item_name
        elif "HP1" in item_name:
            dict_RevAssembly["HP1"][assembly] = item_name
        elif "CMP" in item_name:
            dict_RevAssembly["CMP"][assembly] = item_name


    return dict_RevAssembly


def get_assembly(name):

    lenth_assembly=0
    for chr in range(len(name)):
        if name[lenth_assembly]==",":
            break
        else:
            lenth_assembly += 1

    assembly=name[:(lenth_assembly)]
    return assembly