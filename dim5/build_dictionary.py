def final_dictionary(dictFile, revAssembliesList, positions, verticalAssemblyDict):
    dict = {}
    optional_dict = {}
    for mount in revAssembliesList:
        if revAssembliesList[mount] != []:
            dict[mount] = {}
            optional_dict[mount] = {}
            for assembly in range(len(revAssembliesList[mount])):
                dict[mount][revAssembliesList[mount][assembly]] = {}
                optional_dict[mount][revAssembliesList[mount][assembly]] = {}
                for j in range(len(dictFile[mount])):
                    for k in range(len(dictFile[mount][j])):
                        if checkDataframe(dictFile[mount][j][k], len(verticalAssemblyDict[mount])):
                            dataframe = dictFile[mount][j][k]
                            dict[mount][revAssembliesList[mount][assembly]], dict[mount][revAssembliesList[mount][assembly]], error = partnumbers(dataframe, positions, len(verticalAssemblyDict[mount]))

    return dict


def checkDataframe(dataframe, start_column):
    temp = False
    if len(dataframe.columns) - start_column-1 == 4:
        temp = True
    return temp



def get_start_row(dataframe):
    for x in range(len(dataframe[0])):
        if type(dataframe[0][x]) == float:
            if type(dataframe[0][x]) != float:
                x = x +1
                break
    return x


def add_PartnumberToDictionary(partnumber, description, dictionary):
    added = True
    if partnumber in dictionary:
        dictionary[partnumber]["qty"] += 1
        if dictionary[partnumber]["description"] != description:
            added = False

    else:
        dictionary[partnumber] = {"qty": 1, "description": description}
    return added


def partnumbers(dataframe,positions, nColumns_toCheck):
    partnumbers = {}
    optional_partnumbers = {}
    error = "nothing"
    start_row = get_start_row(dataframe)
    for x in range(start_row, len(dataframe[0]) - start_row):
        for i in positions:
            if dataframe[i][x]==1:
                partnumber = nColumns_toCheck + 1
                description = nColumns_toCheck + 2
                add_error = add_PartnumberToDictionary(partnumber, description, partnumbers)
                if not add_error:
                    error = [partnumber, i]
            elif dataframe[i][x] == "001":
                partnumber = nColumns_toCheck + 1
                description = nColumns_toCheck + 2
                add_error = add_PartnumberToDictionary(optional_partnumbers, description, partnumbers)
                if not add_error:
                    error = [partnumber, i]
    return partnumbers, optional_partnumbers, error