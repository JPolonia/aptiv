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
                for page in range(len(dictFile[mount])):
                    for table in range(len(dictFile[mount][page])):
                        if checkDataframe(dictFile[mount][page][table], len(verticalAssemblyDict[mount])):
                            dataframe = dictFile[mount][page][table]
                            partnumbers, optional_partnumbers, error = get_partnumbers(dataframe, positions[mount][revAssembliesList[mount][assembly]], len(verticalAssemblyDict[mount]))
                            for value in partnumbers:
                                if not value in dict[mount][revAssembliesList[mount][assembly]]:
                                    dict[mount][revAssembliesList[mount][assembly]][value] = partnumbers[value]
                                else:
                                    dict[mount][revAssembliesList[mount][assembly]][value]["qty"] += partnumbers[value]["qty"]
                            for value in optional_partnumbers:
                                if not value in optional_dict[mount][revAssembliesList[mount][assembly]]:
                                    optional_dict[mount][revAssembliesList[mount][assembly]][value] = partnumbers[value]
                                else:
                                    optional_dict[mount][revAssembliesList[mount][assembly]][value]["qty"] += partnumbers[value]["qty"]
    return dict, optional_dict


def checkDataframe(dataframe, start_column):
    temp = False
    x = len(dataframe.columns)
    y = start_column
    if len(dataframe.columns) - start_column == 4:
        temp = True
    return temp



def get_start_row(dataframe):
    for x in range(len(dataframe[0])):
        if type(dataframe[0][x]) == float:
            if type(dataframe[0][x+1]) != float:
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


def get_partnumbers(dataframe, col, nColumns_toCheck):
    partnumbers = {}
    optional_partnumbers = {}
    error = "nothing"
    start_row = get_start_row(dataframe)
    for row in range(start_row, len(dataframe[0])):
        if dataframe[col][row]=="1":
            partnumber = dataframe[nColumns_toCheck + 1][row]
            description = dataframe[nColumns_toCheck + 2][row]
            add_error = add_PartnumberToDictionary(partnumber, description, partnumbers)
            if not add_error:
                error = [partnumber, col]
        elif dataframe[col][row] == "001":
            partnumber = nColumns_toCheck + 1
            description = nColumns_toCheck + 2
            add_error = add_PartnumberToDictionary(optional_partnumbers, description, partnumbers)
            if not add_error:
                error = [partnumber, col]
    return partnumbers, optional_partnumbers, error
