def final_dictionary(dict_Tables):
    dict_Partnumbers = {}
    dict_CMP = {}
    dict_AdditionalFeatures = {}
    for mount in dict_Tables:
        if mount == "CMP":
            check_CMP()
        else:
            for assembly in dict_Tables:
                table = dict_Tables[mount][assembly]
                partnumbers, additional_features = get_partnumbers(table)
                for value in partnumbers:
                    if not value in dict_Partnumbers[mount][assembly]:
                        dict_Partnumbers[mount][assembly][value] = partnumbers[value]
                    else:
                        erro = "Partnumber repetida em: " + assembly + " em " + mount
                for value in additional_features:
                    if not value in dict_AdditionalFeatures[mount][assembly]:
                        dict_AdditionalFeatures[mount][assembly][value] = additional_features[value]
                    else:
                        erro = "Partnumber repetida em: " + assembly + " em " + mount

    return dict_Partnumbers, dict_AdditionalFeatures
