def final_dictionary(dictFile, revAssembliesList, positions, verticalAssemblyDict):
    dict = {}
    optional_dict = {}
    additional_features_dict ={}
    optional_features_dict = {}
    for mount in revAssembliesList:
        if revAssembliesList[mount] != []:
            dict[mount] = {}
            optional_dict[mount] = {}
            additional_features_dict[mount] = {}
            optional_features_dict[mount] = {}
            for assembly in range(len(revAssembliesList[mount])):
                dict[mount][revAssembliesList[mount][assembly]] = {}
                optional_dict[mount][revAssembliesList[mount][assembly]] = {}
                additional_features_dict[mount][revAssembliesList[mount][assembly]] ={}
                optional_features_dict[mount][revAssembliesList[mount][assembly]]= {}
                for page in range(len(dictFile[mount])):
                    for table in range(len(dictFile[mount][page])):
                        if checkDataframe(dictFile[mount][page][table], len(verticalAssemblyDict[mount])):
                            dataframe = dictFile[mount][page][table]
                            partnumbers, optional_partnumbers, additional_features, optional_features, error = get_partnumbers(dataframe, positions[mount][revAssembliesList[mount][assembly]], len(verticalAssemblyDict[mount]))
                            add_error(error)
                            for value in partnumbers:
                                if not value in dict[mount][revAssembliesList[mount][assembly]]:
                                    dict[mount][revAssembliesList[mount][assembly]][value] = partnumbers[value]
                                else:
                                    dict[mount][revAssembliesList[mount][assembly]][value]["qty"] += partnumbers[value]["qty"]
                            for value in optional_partnumbers:
                                if not value in optional_dict[mount][revAssembliesList[mount][assembly]]:
                                    optional_dict[mount][revAssembliesList[mount][assembly]][value] = optional_partnumbers[value]
                                else:
                                    optional_dict[mount][revAssembliesList[mount][assembly]][value]["qty"] += optional_partnumbers[value]["qty"]
                            for value in additional_features:
                                if not value in additional_features_dict[mount][revAssembliesList[mount][assembly]]:
                                    additional_features_dict[mount][revAssembliesList[mount][assembly]][value] = additional_features[value]
                                else:
                                    additional_features_dict[mount][revAssembliesList[mount][assembly]][value]["qty"] += additional_features[value]["qty"]

                            for value in optional_features:
                                if not value in optional_features_dict[mount][revAssembliesList[mount][assembly]]:
                                    optional_features_dict[mount][revAssembliesList[mount][assembly]][value] = optional_features[value]
                                else:
                                    optional_features_dict[mount][revAssembliesList[mount][assembly]][value]["qty"] += optional_features[value]["qty"]
    return dict, optional_dict, additional_features_dict, optional_features_dict


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
    additionalFeatures = {}
    optional_addtionalFeatures = {}
    error = "nothing"
    start_row = get_start_row(dataframe)

    for row in range(start_row, len(dataframe[0])):
        added = True
        if dataframe[col][row]=="1":
            partnumber = dataframe[nColumns_toCheck + 1][row]
            description = dataframe[nColumns_toCheck + 2][row]
            if "MA" in partnumber: #checks if is an additional feauture
                added = add_PartnumberToDictionary(partnumber, description, additionalFeatures)
            elif not "LOCAL_FID" in partnumber and not "GLOBAL_FID"  in partnumber:
                added = add_PartnumberToDictionary(partnumber, description, partnumbers)
            if not added:
                error = "Warning: Component: ", partnumber, "has different descriptions"
                add_error(error)
        elif dataframe[col][row] == "O01":
            partnumber = dataframe[nColumns_toCheck + 1][row]
            description = dataframe[nColumns_toCheck + 2][row]
            if "MA" in partnumber: #checks if is an additional feauture
                added = add_PartnumberToDictionary(partnumber, description, optional_addtionalFeatures)
            elif not "LOCAL_FID" in partnumber and not "GLOBAL_FID" in partnumber:
                added = add_PartnumberToDictionary(partnumber, description, optional_partnumbers)
            if not added:
                error = "Warning: Component: ", partnumber, "has different descriptions"
                add_error(error)
    return partnumbers, optional_partnumbers, additionalFeatures, optional_addtionalFeatures, error


def add_error(error):
    if error != "nothing":
        from errors.error_list import add_error_item

        add_error_item(error)
