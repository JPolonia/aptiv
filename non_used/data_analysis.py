



def check_position(assemblyList, checkAssemblyList, key, index):
    columns  = []
    for x in range(len(assemblyList[key])):
        for i in range(len(checkAssemblyList[index])):
            if assemblyList[key][x] == checkAssemblyList[index][i]:
                columns.append(i)

    return columns


from non_used.error_check import add_error_item
def all_partnumbers_oneTable(dataframe, columns, componentDictionary, n_assemblys, key):
    for i in columns[key]:
        y = dataframe.shape[0]
        for x in range(dataframe.shape[0]):

            y = dataframe[2][3]

            if dataframe[i][x] == 1:
                partnumber = dataframe[n_assemblys][x]
                if partnumber in componentDictionary:
                    componentDictionary[partnumber]['qty'] +=1
                    if not componentDictionary[partnumber]['description'] == dataframe[n_assemblys + 1][x]:
                        add_error_item("Description incongruence in partnumber = " + partnumber)
                else:
                    componentDictionary[partnumber] = {'qty' : 1, 'description' : dataframe[n_assemblys + 1][x]}
    return componentDictionary

def check_all_tables_1page(page, componentDictionary, columns, n_assemblys):
    for x in range(len(page)):
        if page[x].shape[0] > 2:
            componentDictionary  = all_partnumbers_oneTable(page[x], columns, componentDictionary, n_assemblys)

def check_all(pages, componentDictionary, columns, n_assemblys):
    for i in range(len(pages)):
        componentDictionary = check_all_tables_1page(pages[i], componentDictionary, columns, n_assemblys)
    return