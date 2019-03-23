from errors.error_list import add_error_item

def compare(list_PDF, list_Excel):  # Pdf has 4 dict and excel has 2
    dictPDF_Partnumbers = list_PDF[0]
    dictPDF_OptPartnumbers = list_PDF[1]
    dictPDF_AdditionalFeatures = list_PDF[2]
    dictPDF_OptAdditionalFeatures = list_PDF[3]
    dictExcel_Partnumbers = list_Excel[0]
    dictExcel_AdditionalFeatures = list_Excel[1]
    check_Partnumbers(dictPDF_Partnumbers, dictPDF_OptPartnumbers, dictExcel_Partnumbers)
    #check_AdditionalFeatures(dictPDF_AdditionalFeatures, dictPDF_OptAdditionalFeatures, dictExcel_AdditionalFeatures)




def check_Partnumbers(dictPDF_Partnumbers, dictPDF_OptPartnumbers,  dictExcel_Partnumbers):
    for mount in dictPDF_Partnumbers:
        for assembly in dictPDF_Partnumbers[mount]:
            for partnumber in dictPDF_Partnumbers[mount][assembly]:
                if existsInDictionary(partnumber, assembly, mount, dictExcel_Partnumbers): #cheks if it exists in excel
                    checkDescription(partnumber, assembly, mount, dictPDF_Partnumbers, dictExcel_Partnumbers)
                    checkQty(partnumber, assembly, mount, dictPDF_Partnumbers, dictPDF_OptPartnumbers, dictExcel_Partnumbers)
                    del dictExcel_Partnumbers[mount][assembly][partnumber]
                else:
                    error = "ERROR: Partnumber " + partnumber + " does not exist in assembly " + assembly + " " + mount + " in Excel"
                    add_error_item(error)




def checkDescription(partnumber, assembly, mount, dictPDF_Partnumbers, dictExcel_Partnumbers):
    descriptionPDF = dictPDF_Partnumbers[mount][assembly][partnumber]["description"]
    descriptionExcel = dictExcel_Partnumbers[mount][assembly][partnumber]["description"]
    if descriptionPDF != descriptionExcel:
        error = "WARNING: Description of partnumber " + partnumber + " in assembly " + assembly + " " + mount + " does not match between PDF and Excel"
        add_error_item(error)

def checkQty(partnumber, assembly, mount, dictPDF_Partnumbers, dictPDF_OptPartnumbers, dictExcel_Partnumbers):
    qtyPDF = int(dictPDF_Partnumbers[mount][assembly][partnumber]["qty"])
    qtyExcel = int(dictExcel_Partnumbers[mount][assembly][partnumber]["qty"])
    if qtyPDF > qtyExcel:
        error = "ERROR: Quantity of partnumber " +  partnumber + " in assembly " + assembly + " " + mount + " in Excel: " + str(qtyExcel) + " is less than in PDF: " + str(qtyPDF)
        add_error_item(error)
    elif qtyPDF < qtyExcel:
        compareOPT(partnumber, assembly, mount, dictPDF_Partnumbers, dictPDF_OptPartnumbers,dictExcel_Partnumbers)



def compareOPT(partnumber, assembly, mount, dictPDF_Partnumbers, dictPDF_OptPartnumbers,dictExcel_Partnumbers):
    qtyPDF = (dictPDF_Partnumbers[mount][assembly][partnumber]["qty"])
    qtyExcel = (dictExcel_Partnumbers[mount][assembly][partnumber]["qty"])
    qtyOPT = (dictPDF_OptPartnumbers[mount][assembly][partnumber]["qty"])
    if not existsInDictionary(partnumber, assembly, mount, dictPDF_OptPartnumbers):
        error = "ERROR: Quantity of partnumber "+ partnumber + " in assembly "+ assembly + " " + mount + " in Excel: " + str(qtyExcel) + " is higher than in PDF: " + str(qtyPDF)
        add_error_item(error)
    else:
        qty_OPTplusInserted = qtyPDF + qtyOPT
        if qtyExcel > qty_OPTplusInserted: #checks if qty in excel is higher than the sum of mandatory partnumbers and optional
            error = "ERROR: Quantity of partnumber "+ partnumber+ " in assembly " + assembly + " " + mount + " in Excel: " + str(qtyExcel) + " is higher than in PDF: "+ str(qtyPDF)
            add_error_item(error)

def existsInDictionary(partnumber, assembly, mount, dictionary):
    aux = False
    if mount in dictionary:
        if assembly in dictionary[mount]:
            if partnumber in dictionary[mount][assembly]:
                aux = True
    return aux
