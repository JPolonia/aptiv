def check_assembly_count(assemblyList_PDF, assemblyList_Excel, key):
    aux = False
    if len(assemblyList_Excel[key]) == len(assemblyList_PDF[key]):
        aux = True
    return aux


def check_assemblies_PDF_Excel(assemblyList_PDF, assemblyList_Excel, error_path):
    error_file = open(error_path, "w")

    error_list = []
    aux = False

    for key in assemblyList_PDF:
        if check_assembly_count(assemblyList_PDF, assemblyList_Excel, key):
            for value in assemblyList_PDF[key]:
                if assemblyList_PDF[key][value] == assemblyList_Excel[key][value]:  #arrays in key must be sorted
                    aux = True
                else:
                    error_list.append("Assembly number " + value + " from " + key + "does not appear in Excel")
        else:
            error_list.append("Number of " + key + " assemblies revised in PDF does not correspond to Excel")
    line_list = []
    for i in range(len(error_list)):
        line_list.append(error_list[i] + "\n")
    error_file.writelines(line_list)
    error_file.close()


def add_error_item(error):
    error_file = open("files/Errors_List" "-a")
    line = error + "\n"
    error_file.writelines(line)
    error_file.close()
