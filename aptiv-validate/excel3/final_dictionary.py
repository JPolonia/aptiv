import re

def final_dict(dict_Tables):
    dict_Partnumbers = {}
    dict_AdditionalFeatures = {}
    for mount in dict_Tables:
        dict_Partnumbers[mount]={}
        dict_AdditionalFeatures[mount]={}
        for assembly in dict_Tables[mount]:
            dict_Partnumbers[mount][assembly] ={}
            dict_AdditionalFeatures[mount][assembly] = {}
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




def get_partnumbers(table):
    partnumbers = {}
    additional_features = {}
    for item in range(len(table)):
        IsNumber=re.match('\d{1,}', table[item][0]) #check if there are digits in de F/N column
        if IsNumber:
            number = table[item][1]
            description = table[item][3]
            if not table[item][5]=="PC":
                additional_features[number] = {"qty" : 1, "description" : description}
            else:
                qty = table[item][4]
                partnumbers[number] = {"qty": qty, "description": description}
    return partnumbers, additional_features