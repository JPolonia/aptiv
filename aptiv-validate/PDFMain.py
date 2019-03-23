



def PDF(path):
#create error file


    #stage 1
    # with this command we get all pages in a lsit. Each page is a list of dataframes containing all useful info. The pages that have no useful info are a string "ignore"
    from PDF1_parse_pages.get_pages import getPages
    pages = getPages(path)

    pass



    #stage 2
    #retrieve last rev letter, retrive list with separeted data, retrive mount list(checking which mounts are in pdf file)
    from PDF2.retrieve_all import retrieve
    rev_letter, data_list, mount_list, verticalAssemblyList = retrieve(path, pages)

    pass


    #stage3
    #associates data_list with mounts, returning the dictionary which will be analised
    from PDF3.associate import assoc
    dictFile = assoc(data_list, mount_list)
    verticalAssemblyDict = assoc(verticalAssemblyList, mount_list)

    from PDF3.check_rev_assemblies import revAssembliesList
    revAssembliesList = revAssembliesList(pages, rev_letter)

    pass


    #stage4
    #getting the columns positions to check in each mount
    from PDF4.column_numbers import columns_to_analyze
    positions = columns_to_analyze(revAssembliesList, verticalAssemblyDict)




    #stage5
    #buliding the full dictionary
    from PDF5.build_dictionary import final_dictionary
    dict_FinalDataFile, dict_OptionalFinalDataFile, dict_AdditionalFeatures, dict_OptionalAdditionalFeatures = final_dictionary(dictFile,revAssembliesList, positions, verticalAssemblyDict)

    import json
    f = open("files/InsertedComponents.json", "w+")
    f.write("Last Revision = " + rev_letter)
    f.write(json.dumps(dict_FinalDataFile, indent=4, sort_keys=True))
    f = open("files/OptionalComponents.json", "w+")
    f.write(json.dumps(dict_OptionalFinalDataFile, indent=4, sort_keys=True))
    f = open("files/InsertedAdditionalFeatures.json", "w+")
    f.write(json.dumps(dict_AdditionalFeatures, indent=4, sort_keys=True))
    f = open("files/OptionalAdditionalFeatures.json", "w+")
    f.write(json.dumps(dict_OptionalAdditionalFeatures, indent=4, sort_keys=True))
    pass


    list_PDF = []
    list_PDF.append(dict_FinalDataFile)
    list_PDF.append(dict_OptionalFinalDataFile)
    list_PDF.append(dict_AdditionalFeatures)
    list_PDF.append(dict_OptionalAdditionalFeatures)

    return list_PDF