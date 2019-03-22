from errors.error_list import add_error_item

def compare(list_PDF, list_Excel):  # Pdf has 4 dict and excel has 2
    dictPDF_Partnumbers = list_PDF[0]
    dictPDF_OptPartnumbers = list_PDF[1]
    dictPDF_AdditionalFeatures = list_PDF[2]
    dictPDF_OptAdditionalFeatures = list_PDF[3]
    dictExcel_Partnumbers = list_Excel[0]
    dictExcel_AdditionalFeatures = list_Excel[1]
    check_Partnumbers(dictPDF_Partnumbers, dictPDF_OptPartnumbers, dictExcel_Partnumbers)
    check_AdditionalFeatures(dictPDF_AdditionalFeatures, dictPDF_OptAdditionalFeatures, dictExcel_AdditionalFeatures)


def check_Partnumbers(dictPDF_Partnumbers, dictPDF_OptPartnumbers, dictExcel_Partnumbers):
    for mount in dictPDF_Partnumbers:
        for assembly in dictPDF_Partnumbers[mount]:
            if dictPDF_Partnumbers[mount][assembly] in dictExcel_Partnumbers:
                for partnumber in dictPDF_Partnumbers[mount][assembly]:
                    PN_PDF_QTY=dictPDF_Partnumbers[mount][assembly][partnumber]["qty"]
                    PN_OPT_PDF_QTY = dictPDF_OptPartnumbers[mount][assembly][partnumber]["qty"]
                    PN_EX_QTY=dictExcel_Partnumbers[mount][assembly][partnumber]["qty"]
                    PN_PDF_DSC = dictPDF_Partnumbers[mount][assembly][partnumber]["description"]
                    PN_OPT_PDF_DSC = dictPDF_OptPartnumbers[mount][assembly][partnumber]["description"]
                    PN_EX_DSC = dictExcel_Partnumbers[mount][assembly][partnumber]["description"]

                    if PN_PDF_QTY + PN_OPT_PDF_QTY < PN_EX_QTY:
                        error = "Components - Quantity Error. Mount: ", mount, "; Assembly: ", assembly, "; PartNumber: ", partnumber, ".", "\n", "Quantity should be: ", PN_PDF_QTY, " instead of ", PN_EX_QTY, "."
                        add_error_item(error)
                    elif PN_PDF_QTY + PN_OPT_PDF_QTY > PN_EX_QTY:
                        error = "Components - Quantity Warning. Mount: ", mount, "; Assembly: ", assembly, "; PartNumber: ", partnumber, ".", "\n", "Quantity should be: ", PN_PDF_QTY, " instead of ", PN_EX_QTY, "."
                        add_error_item(error)
                    if dictPDF_Partnumbers[mount][assembly][partnumber]["decription"] + \
                            PN_OPT_PDF_DSC < PN_EX_DSC:
                        error ="Components - Description Error. Mount: ", mount, "; Assembly: ", assembly, "; PartNumber: ", partnumber, ".", "\n", "Description should be: ", PN_PDF_DSC, " instead of ", PN_EX_DSC, "."
                        add_error_item(error)
                    elif PN_PDF_DSC + \
                            PN_OPT_PDF_DSC > PN_EX_DSC:
                        error = "Components - Description Warning. Mount: ", mount, "; Assembly: ", assembly, "; PartNumber: ", partnumber, ".", "\n", "Description should be: ", PN_PDF_DSC, " instead of ", PN_EX_DSC, "."
                        add_error_item(error)
            else:
                error= "Partnumbers: Assembly " + assembly + " is in PDF, but not in Excel."
                add_error_item(error)

def check_AdditionalFeatures(dictPDF_AdditionalFeatures, dictPDF_OptAdditionalFeatures, dictExcel_AdditionalFeatures):
    for mount in dictPDF_AdditionalFeatures:
        for assembly in dictPDF_AdditionalFeatures[mount]:
            if dictPDF_AdditionalFeatures[mount][assembly] in dictExcel_AdditionalFeatures:
                a=0
                for partnumbe in dictPDF_AdditionalFeatures[mount][assembly]:
                    if dictPDF_AdditionalFeatures[mount][assembly][partnumbe]["description"] == "MA-CONFORMAL COAT":
                        a=1
                    PN_PDF_QTY = dictPDF_AdditionalFeatures[mount][assembly][partnumbe]["qty"]
                    PN_OPT_PDF_QTY = dictPDF_OptAdditionalFeatures[mount][assembly][partnumbe]["qty"]
                    PN_EX_QTY = dictExcel_AdditionalFeatures[mount][assembly][partnumbe]["qty"]
                    PN_PDF_DSC = dictPDF_AdditionalFeatures[mount][assembly][partnumbe]["description"]
                    PN_OPT_PDF_DSC = dictPDF_OptAdditionalFeatures[mount][assembly][partnumbe]["description"]
                    PN_EX_DSC = dictExcel_AdditionalFeatures[mount][assembly][partnumbe]["description"]
                    if PN_PDF_QTY + \
                            PN_OPT_PDF_QTY < \
                            PN_EX_QTY:
                        error = "Additional Features - Quantity Error. Mount: ", mount, "; Assembly: ",assembly, "; PartNumber: ", partnumbe, ".", "\n", "Quantity should be: ", PN_PDF_QTY, " instead of ", PN_EX_QTY, "."
                        add_error_item(error)
                    elif PN_PDF_QTY + \
                            PN_OPT_PDF_QTY > \
                            PN_EX_QTY:
                        error ="Additional Features - Quantity Warning. Mount: ", mount, "; Assembly: ", assembly, "; PartNumber: ", partnumbe, ".", "\n", "Quantity should be: ", PN_PDF_QTY, " instead of ", PN_EX_QTY, "."
                        add_error_item(error)
                    if PN_PDF_DSC + \
                            PN_OPT_PDF_DSC < PN_EX_DSC:
                        error = "Additional Features - Description Error. Mount: ", mount, "; Assembly: ", assembly, "; PartNumber: ", partnumbe, ".", "\n", "Description should be: ", PN_PDF_DSC, " instead of ", PN_EX_DSC, "."
                        add_error_item(error)
                    elif PN_PDF_DSC + \
                            PN_OPT_PDF_DSC > PN_EX_DSC:
                        error = "Additional Features - Description Warning. Mount: ", mount, "; Assembly: ", assembly, "; PartNumber: ", partnumbe, ".", "\n", "Description should be: ", PN_PDF_DSC, " instead of ", PN_EX_DSC, "."
                        add_error_item(error)
                if a==0:
                    error="Missing MA-CONFORMAL COAT in Complete Assembly: " + assembly
                    add_error_item(error)
        else:
            error = "Additional Features: Assembly " + assembly + " is in PDF, but not in Excel."
            add_error_item(error)