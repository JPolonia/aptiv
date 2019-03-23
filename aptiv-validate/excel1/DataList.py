
def get_DataList(sheet_EBOMData):
    list_Assemblies = Get_Assemblies(sheet_EBOMData)
    dict_DataList = {"SM1" : {}, "SM2" : {}, "HP1" : {}, "CMP" : {}}
    nRows = sheet_EBOMData.nrows
    for list_index in range(len(list_Assemblies)-1): # nao verifica a última tabela
        Assembly= list_Assemblies[list_index][1] #assembly number
        list_dataList=[]

        assemblyRow = list_Assemblies[list_index][0] #position 0 of array in list is the row number
        start_row = get_StartRow(sheet_EBOMData, assemblyRow, nRows)
        end_row = list_Assemblies[list_index+1][0]-2  #table ends 3 rows above partnumber
        for row in range(start_row, end_row):
            lineData = sheet_EBOMData.row_values(row, 1, 7)
            list_dataList.append(lineData)

        description = list_Assemblies[list_index][2]
        mount = ""
        if "SM1" in description:
            mount = "SM1"
        elif "SM2" in description:
            mount = "SM2"
        elif "HP1" in description:
            mount = "HP1"
        elif "CMP" in description:
            mount = "CMP"
        dict_DataList[mount][Assembly] = list_dataList


    #last table
    assemblyRow = list_Assemblies[len(list_Assemblies) - 1][0]
    start_row = get_StartRow(sheet_EBOMData, assemblyRow, nRows)
    end_row = sheet_EBOMData.nrows
    Assembly = list_Assemblies[len(list_Assemblies)-1][1]
    list_dataList = []
    for row in range(start_row, end_row):
        lineData = sheet_EBOMData.row_values(row, 1, 7)
        list_dataList.append(lineData)

    description = list_Assemblies[len(list_Assemblies)-1][2]
    mount = ""
    if "SM1" in description:
        mount = "SM1"
    elif "SM2" in description:
        mount = "SM2"
    elif "HP1" in description:
        mount = "HP1"
    elif "CMP" in description:
        mount = "CMP"
    dict_DataList[mount][Assembly] = list_dataList

    return dict_DataList



def get_StartRow(sheet, AssemblyRow, lenth_sheet):
    for row in range(AssemblyRow, lenth_sheet):
        x = sheet.cell(row, 0)
        if sheet.cell(row, 0).value == "Ll":
            startRow = row+1
            break
    return startRow




def Get_Assemblies(sheet_EBOM_data):
    list_Assemblies=[]
    nrows = sheet_EBOM_data.nrows
    for row in range(nrows):
        if sheet_EBOM_data.cell(row, 0).value=="Part Number":
            list_Assemblies.append([row, sheet_EBOM_data.cell(row, 1).value, sheet_EBOM_data.cell(row+3, 1).value])
    return list_Assemblies #contains star row, assembly number and assembly description








