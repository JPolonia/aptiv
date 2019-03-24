import tabula
import PyPDF2
import re
import os
import xlrd
import json


# Error functions
path_error = "files/Errors_List.txt"
def create_ErrorFile():         # creates a text file for error output
    error_file = open(path_error,"w+")
    error_file.close()


def add_error_item(error):          # adds error line to error text file
    error_file = open(path_error, "a")
    error_file.write(error + "\n")
    error_file.close()

def noErrors():         # checks if there were no added errors to
    if os.stat(path_error).st_size == 0:
        add_error_item("No errors/ warnings")
# End of error functions



# Utility fucntions
# checks at which column starts the partnumbers
def check_start_column(dataframe):
    aux = False
    col = -1
    while not aux:
        col += 1
        if not type(dataframe[col][0]) == float:
            if not re.match('\d{5,}', dataframe[col][0]):  # cell has to have 5 or more digits
                aux = True
    return col

def add_PartnumberToDictionary(partnumber, description, dictionary):
    added = True
    if partnumber in dictionary:
        dictionary[partnumber]["qty"] += 1
        if dictionary[partnumber]["description"] != description:
            added = False

    else:
        dictionary[partnumber] = {"qty": 1, "description": description}
    return added

#Turning into "Error" into bold
def bold(error):
    if error[0:5]=="ERROR" or error[0:5]=="Error":
        bold1 = "\033[1m"
        reset = "\033[0;0m"
        a = bold1 + error + reset
    return error

# End of utility fucntions



# Class Errors
class Errors:

    def __init__(self, path):  # path="files/Errors_List.txt"
        self.list=[]
        #self.path=path
        self.file=""

    def create_ErrorFile(self):  # creates a text file for error output
        self.file = open(self.path, "w+")
        self.file.close()

    def add_error_item(self, error):  # adds error line to error text file
        self.file = open(self.path, "a")
        error1=bold(error)
        self.file.write(error1 + "\n")
        self.file.close()

    def noErrors(self):  # checks if there were no added errors to
        if os.stat(self.path).st_size == 0:
            self.add_error_item("No errors/ warnings")

# End of Class Errors



# Class PDF
class classPDF:

    errorList = []

    def __init__(self, path):
        self.path = path
        self.Npages = self.NumPages(path)
        self.Pages = self.validatedPages(path)   # returns a list of validated pages
        self.RevLetter = self.revLetter(self.Pages)   # returns the letter of last revision
        self.ID = self.IDnumber(self.Pages)   # returns de number to compare with excel (CN)
        self.listMounts = self.MountList(self.Pages)   # returns an orgaized list of the mounts that are in the first page
        self.dictPagesPerMount = self.dictComponentTables(self.Pages)   # returns a dictionary of mounts that have respective tables
        self.dictVerticalAssembly = self.VerticalAssemblyDict(self.Pages) # returns a dictionary of a list of vertcal asseblies in each mount
        self.dictComponents, self.dictOptionalComponents, self.dictAdditionalFeatures, self.dictOptionalAdditionalFeatures = self.final_dictionary()
        self.listPDF = self.PDFlist()

    #Properties of PDF
    def NumPages(self, path):  # gets number of pages id the PDF file

        pdf_file = open(path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        n_pages = PyPDF2.PdfFileReader.getNumPages(pdf_reader)

        return n_pages


    def validatedPages(self, path): # Parses PDF to python and returns list of pages that exclude ignorable ones (marked has "ignore"

        n_pages = self.NumPages(path)
        pages = []  # list that stores pages
        pages.append(self.pdf_to_tb(path, 1))
        pages[0].append(self.pdf_to_tb_area(path, 1, 73.01, 1743.3, 1682.21, 2363.14))  # retrieves date table info
        for pageNumber in range(2, n_pages + 1):
            page = self.pdf_to_tb_area(path, pageNumber, 34.27, 32.78, 1649.43,
                                  2360.16)  # only retrieve info thats inside the outer grid
            # Page Validation
            aux = False
            for pageNumb in range(0, len(page) - 1):
                if page[pageNumb][0][
                    0] == "If Package name is not available, then up to 15 characters of the geometry name\rwill appear in parentheses":
                    aux = True
                    break
            if not aux:  # unuseful pages are marked as ignore
                    page = "ignore"
            # End of page validation
            pages.append(page)
        # Ignore CMP
        pageNumber = n_pages
        aux = False
        while not aux and pageNumber > -1:  # assuming that CMP page is either last page or is only before ignorable pages
            if pages[pageNumber - 1] == "ignore":
                pageNumber = pageNumber - 1
            else:
                pages[pageNumber - 1] = "ignore"
                aux = True
        # End of ignoring CMP

        return pages

    def revLetter(self, pages):
        page = pages[0]
        rev = ""
        row = 0
        while row <= len(page[5][0][2]):
            rev = page[5][0][2][row]
            aux = True
            for i in range(row + 1, row + 6):
                if not type(page[5][0][2][i]) == float:
                    aux = False
            if aux:
                if not type(rev) == float:
                    row = len(page[5][0][2])
            row += 1
        return rev

    def IDnumber(self, pages):  # return number of pdf to check if excel corresponds
        page = pages[0]
        row = 0
        while True:
            if page[5][0][2][row] == self.revLetter(pages):
                break
            else:
                row += 1

        id = page[5][0][7][row]
        id.replace(" ", "")

        return id

    # Getting a list of mounts that appear in 1st page
    def MountList(self, pages):
        MountList = []
        # Checking which Mounts appear in 1st page table
        dataframe = pages[0][3]  # page 0 is the first one, and the info is in dataframe number 3, always
        start_column = check_start_column(dataframe)
        existsSM1 = False
        existsSM2 = False
        existsHP1 = False
        for col in range(len(dataframe[0])):
            if not type(dataframe[start_column + 1][col]) == float:
                if "SM1" in dataframe[start_column + 1][col]:
                    existsSM1 = True
                elif "SM2" in dataframe[start_column + 1][col]:
                    existsSM2 = True
                elif "HP1" in dataframe[start_column + 1][col]:
                    existsHP1 = True
        # End of Checking which Mounts appear in 1st page table
        # Adding Mounts to list:
        if existsSM1:
            MountList.append("SM1")
        if existsSM2:
            MountList.append("SM2")
        if existsHP1:
            MountList.append("HP1")
        return MountList
        # End of Getting a list of mounts that appear in 1st page

    def dictComponentTables(self, pages):

        MountList = self.listMounts
        # Getting Data List with blocks of pages that will correspond to a mount from MountList
        DataList = []
        nPage = len(pages)
        pageIndex = nPage - 1
        aux = False
        # while starts at end of pdf file
        while pageIndex >1:  # the identfying element that tels us wchic pages separate mounts is "ignore"
            if pages[pageIndex] == "ignore":
                if not pageIndex == nPage - 1:  # if page is not last one
                    # checks if previous page was ignore, because there's only 1 ignore between mounts
                    if not pages[pageIndex + 1] == "ignore" :
                        array = []
                        x = pageIndex + 1
                        while pages[x] != "ignore":  # gets all pages until it finds an "ignore"
                            array.append(pages[x])
                            x += 1
                        DataList.append(array)
            pageIndex = pageIndex - 1
        DataList.reverse()
        # End of Getting Data List with blocks of pages that will correspond to a mount from MountList

        # Associating both lists
        dictPagesPerMount = {}
        for i in range(len(DataList)):
            dictPagesPerMount[MountList[i]] = DataList[i]
        if not len(DataList) == len(MountList):
            error="ERROR: Not every mount from 1st page is defined through out PDF or otherwise, rest of analysis might be corrupted"
            self.errorList.append(error)
        # End of Associating both lists
        return dictPagesPerMount

    # Aggreggate the vertical assemblies arrays in a dictionary
    def VerticalAssemblyDict(self, pages):
        path = self.path
        path_out = 'files/rotated.pdf'

        # Rotate PDF 90º
        pdf_in = open(path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_in)
        pdf_writer = PyPDF2.PdfFileWriter()

        for pageNumb in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pageNumb)
            page.rotateClockwise(90)
            pdf_writer.addPage(page)

        pdf_out = open(path_out, 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()
        pdf_in.close()
        # End of Rotate PDF 90º

        listCheckedAssembly = []
        for pagenum in range(len(pages) - 1, 1, -1):
            if pages[pagenum] == "ignore":
                if not pages[pagenum - 1] == "ignore":

                    # Retrive Data from rotated file
                    page = self.pdf_to_tb_area(path_out, pagenum, 28.418, 1444.03, 2352.338,
                                               1652.425)  # retrieves by area
                    assemblyArray = []  # gets an array of assemblies that will correspond to a mount
                    aux = True
                    i = 0
                    while aux:
                        assemblyArray.append(page[0][0][i])
                        number = page[0][0][i + 1]
                        if not type(number) == float:  # drop all float values… … but only if they are nan
                            if not re.match('\d{5,}',
                                            number):  # checks if string has 5 digits or more, if not it ends the cycle
                                aux = False
                        else:
                            aux = False
                        i += 1
                    # End of Retrieving Data from rotated file

                    listCheckedAssembly.append(assemblyArray)

        listCheckedAssembly.reverse()
        os.remove(path_out)

        dictVerticalAssembly = {}
        for mount in range(len(self.listMounts)):
            dictVerticalAssembly[self.listMounts[mount]] = {}
        for i in range(len(listCheckedAssembly)):
            dictVerticalAssembly[self.listMounts[i]] = listCheckedAssembly[i]
        if not len(listCheckedAssembly) == len(self.listMounts):
            error = "Not every mount from 1st page is defined through out PDF or otherwise, rest of analysis might be corrupted"
            self.errorList.append(error)

        return dictVerticalAssembly
    # End of Aggreggate the assemblies arrays in a dictionary

    #End of Properties PDF





    # Parsing Methods
    def pdf_to_tb(self, path, page):
        dt = tabula.read_pdf(path, output_format="dataframe", encoding="utf-8", java_options=None, pandas_options=None,
                             multiple_tables=True, pages=page)
        return dt  # returns list of the multiple dataframes inside a page

    def pdf_to_tb_area(self, path, page, xl, yl, xr, yr):  # returns list of dataframes for a specific area
        df = tabula.read_pdf(path, output_format="dataframe", encoding="utf-8", java_options=None, pandas_options=None, multiple_tables=True, pages=page, spreadsheet=True, area=(xl, yl, xr, yr))
        return df

    def pdf_to_tb_noPage(self, path):
        dt = tabula.read_pdf(path, output_format="dataframe", encoding="utf-8", java_options=None, pandas_options=None,
                             multiple_tables=True)
        return dt  # returns list of the multiple dataframes inside a page
    # End Parsing Methods



    # Method for Checking Revision for Errors
    def check_RevisionError(self, pages):
        page = pages[0]
        dataframe = page[3]
        startColumn = check_start_column(dataframe)
        list_Finders = []
        list_Revisions = []

        for row in range(len(dataframe[0]) - 1, -1, -1):
            if type(dataframe[startColumn][row]) != float:
                if "." in dataframe[startColumn][row]:
                    revLetter = dataframe[startColumn + 3][row]
                    list_Revisions.append(revLetter)
                    list_Finders.append(list_Revisions)
                    list_Revisions.reverse()
                    list_Revisions = []
                else:
                    revLetter = dataframe[startColumn + 3][row]
                    list_Revisions.append(revLetter)

        list_Finders.reverse()

        for finder in range(len(list_Finders)):
            counter = 0
            last_Rev = list_Finders[finder][0]
            for revision in range(1, len(list_Finders[finder])):
                revLetter = list_Finders[finder][revision]
                if revLetter == last_Rev:
                    counter += 1
                elif revLetter >= last_Rev:
                    error = "Error: Assembly in position " + str(
                        revision + 1) + " has later revision than CMP in finder " + str(finder + 1)
                    self.errorList.append(error)
            if counter == 0:
                warning = "Warning: CMP has later revision than all assemblies in finder " + str(finder + 1)
                self.errorList.append(warning)
    # End of Method for Checking Revision for Errors


    # Method for building the final dictionary
    def final_dictionary(self):
        dictFile = self.dictPagesPerMount
        verticalAssemblyDict = self.dictVerticalAssembly

        dictComponents = {}
        dictOptionalComponents = {}
        dictAdditionalFeatures = {}
        dictOptionalAdditionalFeatures = {}

        # Adding to respective mounts, the assemblies that are signelized as being last revised.
        dataframe = self.Pages[0][3]
        revAssemblyList = {"SM1": [], "SM2": [], "HP1": []}
        start_column = check_start_column(dataframe)
        # Get row of revised assemblies
        column = start_column + 3
        positionsList = []
        for row in range(len(dataframe[column])):
            if dataframe[column][row] == self.RevLetter:
                positionsList.append(row)
        # End of Get postions of revised assemblies

        # Build list of assemblies that are revised
        for value in positionsList:
            if "SM1" in dataframe[start_column + 1][value]:
                revAssemblyList["SM1"].append(dataframe[start_column][value])
                sorted(revAssemblyList["SM1"])
            elif "SM2" in dataframe[start_column + 1][value]:
                revAssemblyList["SM2"].append(dataframe[start_column][value])
                sorted(revAssemblyList["SM2"])
            elif "HP1" in dataframe[start_column + 1][value]:
                revAssemblyList["HP1"].append(dataframe[start_column][value])
                sorted(revAssemblyList["HP1"])
        # Enf of Adding to respective mounts, the assemblies that are signelized as being last revised.

        pass

        positionsDict = {}
        for mount in self.listMounts:
            positionsDict[mount] = {}

        pass

        total_columns = {}
        for mount in self.dictVerticalAssembly:
            total_columns[mount] = len(self.dictVerticalAssembly[mount])

        pass

        for mount in revAssemblyList:
            if revAssemblyList[mount] is not None:
                if mount in verticalAssemblyDict:
                    for i in range(total_columns[mount]):
                        if verticalAssemblyDict[mount][i] in revAssemblyList[mount]:
                            positionsDict[mount][verticalAssemblyDict[mount][i]] = i

        pass

        for mount in revAssemblyList:
            if revAssemblyList[mount] != []:
                dictComponents[mount] = {}
                dictOptionalComponents[mount] = {}
                dictAdditionalFeatures[mount] = {}
                dictOptionalAdditionalFeatures[mount] = {}
                for assembly in range(len(revAssemblyList[mount])):
                    dictComponents[mount][revAssemblyList[mount][assembly]] = {}
                    dictOptionalComponents[mount][revAssemblyList[mount][assembly]] = {}
                    dictAdditionalFeatures[mount][revAssemblyList[mount][assembly]] = {}
                    dictOptionalAdditionalFeatures[mount][revAssemblyList[mount][assembly]] = {}
                    for page in range(len(dictFile[mount])):
                        for table in range(len(dictFile[mount][page])):

                            # Checking if dataframe is the one we are looking for
                            dataframe = dictFile[mount][page][table]
                            checkDataframe = False
                            x = len(dataframe.columns)
                            y = start_column
                            if len(dataframe.columns) -  len(self.dictVerticalAssembly[mount]) == 4: # no of non assembly columns  is 4
                                checkDataframe = True
                            # End of Checking if dataframe is the one we are looking for

                            if checkDataframe:
                                dataframe = dictFile[mount][page][table]

                                col = positionsDict[mount][revAssemblyList[mount][assembly]]
                                nColumns_toCheck = len(verticalAssemblyDict[mount])
                                partnumbers = {}
                                optional_partnumbers = {}
                                additionalFeatures = {}
                                optional_additionalFeatures = {}
                                error = "nothing"

                                for row in range(len(dataframe[0])):
                                    if type(dataframe[0][row]) == float:
                                        if type(dataframe[0][row + 1]) != float:
                                            row = row + 1
                                            break
                                start_row = row

                                for row in range(start_row, len(dataframe[0])):
                                    added = True
                                    if dataframe[col][row] == "1":
                                        partnumber = dataframe[nColumns_toCheck + 1][row]
                                        description = dataframe[nColumns_toCheck + 2][row]
                                        if "MA" in partnumber:  # checks if is an additional feauture
                                            added = add_PartnumberToDictionary(partnumber, description,
                                                                                            additionalFeatures)
                                        elif not "LOCAL_FID" in partnumber and not "GLOBAL_FID" in partnumber:
                                            added = add_PartnumberToDictionary(partnumber, description,
                                                                                            partnumbers)
                                        if not added:
                                            error = "Warning: Component: ", partnumber, "has different descriptions"
                                            self.errorList.append(error)
                                    elif dataframe[col][row] == "O01":
                                        partnumber = dataframe[nColumns_toCheck + 1][row]
                                        description = dataframe[nColumns_toCheck + 2][row]
                                        if "MA" in partnumber:  # checks if is an additional feauture
                                            added = add_PartnumberToDictionary(partnumber, description,
                                                                                            optional_additionalFeatures)
                                        elif not "LOCAL_FID" in partnumber and not "GLOBAL_FID" in partnumber:
                                            added = add_PartnumberToDictionary(partnumber, description,
                                                                                            optional_partnumbers)
                                        if not added:
                                            error = "Warning: Component: ", partnumber, "has different descriptions"
                                            self.errorList.append(error)

                                for value in partnumbers:
                                    if not value in dictComponents[mount][revAssemblyList[mount][assembly]]:
                                        dictComponents[mount][revAssemblyList[mount][assembly]][value] = partnumbers[
                                            value]
                                    else:
                                        dictComponents[mount][revAssemblyList[mount][assembly]][value]["qty"] += \
                                            partnumbers[value]["qty"]
                                for value in optional_partnumbers:
                                    if not value in dictOptionalComponents[mount][revAssemblyList[mount][assembly]]:
                                        dictOptionalComponents[mount][revAssemblyList[mount][assembly]][value] = \
                                            optional_partnumbers[value]
                                    else:
                                        dictOptionalComponents[mount][revAssemblyList[mount][assembly]][value]["qty"] += \
                                            optional_partnumbers[value]["qty"]
                                for value in additionalFeatures:
                                    if not value in dictAdditionalFeatures[mount][revAssemblyList[mount][assembly]]:
                                        dictAdditionalFeatures[mount][revAssemblyList[mount][assembly]][value] = \
                                            additionalFeatures[value]
                                    else:
                                        dictAdditionalFeatures[mount][revAssemblyList[mount][assembly]][value][
                                            "qty"] += additionalFeatures[value]["qty"]

                                for value in optional_additionalFeatures:
                                    if not value in dictOptionalAdditionalFeatures[mount][
                                        revAssemblyList[mount][assembly]]:
                                        dictOptionalAdditionalFeatures[mount][revAssemblyList[mount][assembly]][value] = \
                                            optional_additionalFeatures[value]
                                    else:
                                        dictOptionalAdditionalFeatures[mount][revAssemblyList[mount][assembly]][value][
                                            "qty"] += optional_additionalFeatures[value]["qty"]
        return dictComponents, dictOptionalComponents, dictAdditionalFeatures, dictOptionalAdditionalFeatures

    # End Method for building the final dictionary

    # Method for Writing dictionaries to json
    def writeJSON(self):
        f = open("files/InfoPDF.json", "w+")
        f.write(json.dumps(self.listPDF, indent=4, sort_keys=True))
        # f = open("files/OptionalComponents.json", "w+")
        # f.write("Last Revision = " + self.RevLetter + "}" + "\n")
        # f.write(json.dumps(self.dictOptionalComponents, indent=4, sort_keys=True))
        # f = open("files/InsertedAdditionalFeatures.json", "w+")
        # f.write("Last Revision = " + self.RevLetter + "}" + "\n")
        # f.write(json.dumps(self.dictAdditionalFeatures, indent=4, sort_keys=True))
        # f = open("files/OptionalAdditionalFeatures.json", "w+")
        # f.write("Last Revision = " + self.RevLetter + "}" + "\n")
        # f.write(json.dumps(self.dictOptionalAdditionalFeatures, indent=4, sort_keys=True))
    # Method for Writing dictionaries to json



    # Method for retreiveing a list of pdf dictionaries
    def PDFlist(self):
        list_PDF = {}
        list_PDF["Components"] = self.dictComponents
        list_PDF["OptionalComponents"] = self.dictOptionalComponents
        list_PDF["AdditionalFeatures"] = self.dictAdditionalFeatures
        list_PDF["OptionalAdditionalFeatures"] = self.dictOptionalAdditionalFeatures

        return list_PDF
    # End of Method for retreiveing a list of pdf dictionaries




# End of Class PDF



class classExcel:
    errorList=[]

    def __init__(self, path):
        self.path = path
        self.sheet_EBOM_DATA=self.get_sheet("EBOM Data", path)
        self.sheet_IDM = self.get_sheet("ITEM MASTER Data", path)
        self.sheet_APPROVAL = self.get_sheet("APPROVAL", path)
        self.RevLetter=self.get_sheet_Revision()
        self.ID=self.get_sheet_CN()
        self.dict_RevAssemblies = self.get_RevAssemblies()
        self.dict_DataList = self.get_DataList(self.sheet_EBOM_DATA)
        self.dict_Partnumbers, self.dict_AdditionalFeatures = self.final_dict(self.dict_DataList)
        self.list_Excel=self.EXCEL()



    def get_sheet(self, name, path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_name(name)
        return sheet

    def add_weight(self,mount, dict, weight):
        if "weight" in dict[mount]:
            dict[mount]["weight"] += weight
        else:
            dict[mount]["weight"] = weight
        return dict

    def get_RevAssemblies(self):
        dict_RevAssembly = {"SM1": {}, "SM2": {}, "HP1": {}, "CMP": {}}
        n_rows = self.sheet_IDM.nrows
        weights = [0, 0, 0, 0]
        for row in range(7, n_rows):  # table starts at line 7
            name = self.sheet_IDM.cell(row, 0).value
            assembly = self.get_assembly(name)
            item_name = self.sheet_IDM.cell(row, 1).value
            weight = self.sheet_IDM.cell(row, 6).value
            if "SM1" in item_name:
                dict_RevAssembly["SM1"][assembly] = item_name
                weights[1] += weight
            elif "SM2" in item_name:
                dict_RevAssembly["SM2"][assembly] = item_name
                weights[0] += weight
            elif "HP1" in item_name:
                dict_RevAssembly["HP1"][assembly] = item_name
                weights[2] += weight
            elif "CMP" in item_name:
                dict_RevAssembly["CMP"][assembly] = item_name
                weights[3] += weight
            self.compare_weight(weights)

        return dict_RevAssembly

    def compare_weight(self,weights):
        for x in range(len(weights) - 1):
            for y in range(x + 1, len(weights)):
                if weights[x] > weights[y]:
                    error = ("Error:" + " Weight of Assembly "+  self.change_numbers(x)+ " is bigger than Assembly "+ self.change_numbers(y))
                    self.errorList.append(error + "\n")

    def change_numbers(self,x):
        if x == 0:
            return "SM2"
        elif x == 1:
            return "SM1"
        elif x == 2:
            return "HP1"
        else:
            return "CMP"


    def get_DataList(self,sheet_EBOMData):
        list_Assemblies = self.Get_Assemblies(sheet_EBOMData)
        dict_DataList = {"SM1": {}, "SM2": {}, "HP1": {}, "CMP": {}}
        nRows = sheet_EBOMData.nrows
        for list_index in range(len(list_Assemblies) - 1):  # nao verifica a ˙ltima tabela
            Assembly = list_Assemblies[list_index][1]  # assembly number
            list_dataList = []

            assemblyRow = list_Assemblies[list_index][0]  # position 0 of array in list is the row number
            start_row = self.get_StartRow(sheet_EBOMData, assemblyRow, nRows)
            end_row = list_Assemblies[list_index + 1][0] - 2  # table ends 3 rows above partnumber
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

        # last table
        assemblyRow = list_Assemblies[len(list_Assemblies) - 1][0]
        start_row = self.get_StartRow(sheet_EBOMData, assemblyRow, nRows)
        end_row = sheet_EBOMData.nrows
        Assembly = list_Assemblies[len(list_Assemblies) - 1][1]
        list_dataList = []
        for row in range(start_row, end_row):
            lineData = sheet_EBOMData.row_values(row, 1, 7)
            list_dataList.append(lineData)

        description = list_Assemblies[len(list_Assemblies) - 1][2]
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

    def get_StartRow(self,sheet, AssemblyRow, lenth_sheet):
        for row in range(AssemblyRow, lenth_sheet):
            if sheet.cell(row, 0).value == "Ll":
                startRow = row + 1
                break
        return startRow

    def Get_Assemblies(self,sheet_EBOM_data):
        list_Assemblies = []
        nrows = sheet_EBOM_data.nrows
        for row in range(nrows):
            if sheet_EBOM_data.cell(row, 0).value == "Part Number":
                list_Assemblies.append(
                    [row, sheet_EBOM_data.cell(row, 1).value, sheet_EBOM_data.cell(row + 3, 1).value])
        return list_Assemblies  # contains star row, assembly number and assembly description

    def checkCoherence(self):
        for mount in self.dict_RevAssemblies:

            for assembly in self.dict_RevAssemblies[mount]:
                if not assembly in self.dict_DataList[mount]:
                    error = "Error:" + " Assembly: " + str(assembly) + " , " + str(mount) + " from ITEM MASTER Data is not present in " + str(mount) + " in EBOM Data"
                    self.errorList.append(error + "\n")

    def checkCMP(self, dict_DataList):
        if dict_DataList["CMP"] != {}:
            self.retrieveData(dict_DataList["CMP"])

    def retrieveData(self, dict_CMPAssemblies):
        for assembly in dict_CMPAssemblies:
            edd, dwg, schematic = self.get_Features(dict_CMPAssemblies[assembly])
            if edd != "" or dwg != "" or schematic != "":
                error = "ERROR: " + "Assembly: " + assembly + " => CMP is missing " + edd + " " + dwg + " " + schematic
                self.errorList.append(error + "\n")

    def get_Features(self, list_assemblies):  # n˙mero part number

        edd = "EDD"
        dwg = "DWG"
        schematic = "SCHEMATIC"
        for part in range(len(list_assemblies)):
            partnumber = list_assemblies[part][1]
            description = list_assemblies[part][3]
            if "EDD" in partnumber:
                edd = ""
            elif "DWG" in partnumber:
                dwg = ""
            elif "SCHEMATIC" in description:
                schematic = ""
        return edd, dwg, schematic

    def final_dict(self, dict_Tables):
        dict_Partnumbers = {}
        dict_AdditionalFeatures = {}
        for mount in dict_Tables:
            dict_Partnumbers[mount] = {}
            dict_AdditionalFeatures[mount] = {}
            for assembly in dict_Tables[mount]:
                dict_Partnumbers[mount][assembly] = {}
                dict_AdditionalFeatures[mount][assembly] = {}
                table = dict_Tables[mount][assembly]
                partnumbers, additional_features = self.get_partnumbersExcel(table)
                for value in partnumbers:
                    if not value in dict_Partnumbers[mount][assembly]:
                        dict_Partnumbers[mount][assembly][value] = partnumbers[value]
                    else:
                        erro = "Partnumber repetida em: " + assembly + " em " + mount
                        self.errorList.append(erro + "\n")
                for value in additional_features:
                    if not value in dict_AdditionalFeatures[mount][assembly]:
                        dict_AdditionalFeatures[mount][assembly][value] = additional_features[value]
                    else:
                        erro = "Partnumber repetida em: " + assembly + " em " + mount
                        self.errorList.append(erro + "\n")
        return dict_Partnumbers, dict_AdditionalFeatures

    def get_partnumbersExcel(self, table):
        partnumbers = {}
        additional_features = {}
        for item in range(len(table)):
            IsNumber = re.match('\d{1,}', table[item][0])  # check if there are digits in de F/N column
            if IsNumber:
                number = table[item][1]
                description = table[item][3]
                if not table[item][5] == "PC":
                    additional_features[number] = {"qty": 1, "description": description}
                else:
                    qty = table[item][4]
                    partnumbers[number] = {"qty": qty, "description": description}
        return partnumbers, additional_features

    # Excel Main

    def EXCEL(self):

        # stage 2 - Checks coherence between ITEM MASTER Data and EBOM Data.
        self.checkCoherence()



        list_Excel = []
        list_Excel.append(self.dict_Partnumbers)
        list_Excel.append(self.dict_AdditionalFeatures)

        return list_Excel

    def get_sheet_CN(self):
        CN = self.sheet_APPROVAL.cell(4, 3).value  # retira valor do CN
        return CN

    def get_sheet_Revision(self):
        revision = self.sheet_APPROVAL.cell(4, 1).value  # retira valor da ultima revisao
        return revision

    def get_assembly(self, name):

        lenth_assembly = 0
        for chr in range(len(name)):
            if name[lenth_assembly] == ",":
                break
            else:
                lenth_assembly += 1

        assembly = name[:(lenth_assembly)]
        return assembly




# Class Excel

class classExcel:
    errorList=[]

    def __init__(self, path):
        self.path = path
        self.sheet_EBOM_DATA=self.get_sheet("EBOM Data", path)
        self.sheet_IDM = self.get_sheet("ITEM MASTER Data", path)
        self.sheet_APPROVAL = self.get_sheet("APPROVAL", path)
        self.RevLetter=self.get_sheet_Revision()
        self.ID=self.get_sheet_CN()
        self.dict_RevAssemblies = self.get_RevAssemblies()
        self.dict_DataList = self.get_DataList(self.sheet_EBOM_DATA)
        self.dict_Partnumbers, self.dict_AdditionalFeatures = self.final_dict(self.dict_DataList)
        self.list_Excel=self.EXCEL()

    def writeJSON(self):
        f = open("files/InfoExcel.json", "w+")
        f.write(json.dumps(self.list_Excel, indent=4, sort_keys=True))

    def get_sheet(self, name, path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_name(name)
        return sheet

    def add_weight(self,mount, dict, weight):
        if "weight" in dict[mount]:
            dict[mount]["weight"] += weight
        else:
            dict[mount]["weight"] = weight
        return dict

    def get_RevAssemblies(self):
        dict_RevAssembly = {"SM1": {}, "SM2": {}, "HP1": {}, "CMP": {}}
        n_rows = self.sheet_IDM.nrows
        weights = [0, 0, 0, 0]
        for row in range(7, n_rows):  # table starts at line 7
            name = self.sheet_IDM.cell(row, 0).value
            assembly = self.get_assembly(name)
            item_name = self.sheet_IDM.cell(row, 1).value
            weight = self.sheet_IDM.cell(row, 6).value
            if "SM1" in item_name:
                dict_RevAssembly["SM1"][assembly] = item_name
                weights[1] += weight
            elif "SM2" in item_name:
                dict_RevAssembly["SM2"][assembly] = item_name
                weights[0] += weight
            elif "HP1" in item_name:
                dict_RevAssembly["HP1"][assembly] = item_name
                weights[2] += weight
            elif "CMP" in item_name:
                dict_RevAssembly["CMP"][assembly] = item_name
                weights[3] += weight
            self.compare_weight(weights)

        return dict_RevAssembly

    def compare_weight(self,weights):
        for x in range(len(weights) - 1):
            for y in range(x + 1, len(weights)):
                if weights[x] > weights[y]:
                    error = ("Error:" + " Weight of Assembly "+  self.change_numbers(x)+ " is bigger than Assembly "+ self.change_numbers(y))
                    self.errorList.append(error + "\n")

    def change_numbers(self,x):
        if x == 0:
            return "SM2"
        elif x == 1:
            return "SM1"
        elif x == 2:
            return "HP1"
        else:
            return "CMP"


    def get_DataList(self,sheet_EBOMData):
        list_Assemblies = self.Get_Assemblies(sheet_EBOMData)
        dict_DataList = {"SM1": {}, "SM2": {}, "HP1": {}, "CMP": {}}
        nRows = sheet_EBOMData.nrows
        for list_index in range(len(list_Assemblies) - 1):  # nao verifica a ˙ltima tabela
            Assembly = list_Assemblies[list_index][1]  # assembly number
            list_dataList = []

            assemblyRow = list_Assemblies[list_index][0]  # position 0 of array in list is the row number
            start_row = self.get_StartRow(sheet_EBOMData, assemblyRow, nRows)
            end_row = list_Assemblies[list_index + 1][0] - 2  # table ends 3 rows above partnumber
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

        # last table
        assemblyRow = list_Assemblies[len(list_Assemblies) - 1][0]
        start_row = self.get_StartRow(sheet_EBOMData, assemblyRow, nRows)
        end_row = sheet_EBOMData.nrows
        Assembly = list_Assemblies[len(list_Assemblies) - 1][1]
        list_dataList = []
        for row in range(start_row, end_row):
            lineData = sheet_EBOMData.row_values(row, 1, 7)
            list_dataList.append(lineData)

        description = list_Assemblies[len(list_Assemblies) - 1][2]
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

    def get_StartRow(self,sheet, AssemblyRow, lenth_sheet):
        for row in range(AssemblyRow, lenth_sheet):
            if sheet.cell(row, 0).value == "Ll":
                startRow = row + 1
                break
        return startRow

    def Get_Assemblies(self,sheet_EBOM_data):
        list_Assemblies = []
        nrows = sheet_EBOM_data.nrows
        for row in range(nrows):
            if sheet_EBOM_data.cell(row, 0).value == "Part Number":
                list_Assemblies.append(
                    [row, sheet_EBOM_data.cell(row, 1).value, sheet_EBOM_data.cell(row + 3, 1).value])
        return list_Assemblies  # contains star row, assembly number and assembly description

    def checkCoherence(self):
        for mount in self.dict_RevAssemblies:

            for assembly in self.dict_RevAssemblies[mount]:
                if not assembly in self.dict_DataList[mount]:
                    error = "Error:" + " Assembly: " + str(assembly) + " , " + str(mount) + " from ITEM MASTER Data is not present in " + str(mount) + " in EBOM Data"
                    self.errorList.append(error + "\n")

    def checkCMP(self, dict_DataList):
        if dict_DataList["CMP"] != {}:
            self.retrieveData(dict_DataList["CMP"])

    def retrieveData(self, dict_CMPAssemblies):
        for assembly in dict_CMPAssemblies:
            edd, dwg, schematic = self.get_Features(dict_CMPAssemblies[assembly])
            if edd != "" or dwg != "" or schematic != "":
                error = "ERROR: " + "Assembly: " + assembly + " => CMP is missing " + edd + " " + dwg + " " + schematic
                self.errorList.append(error + "\n")

    def get_Features(self, list_assemblies):  # n˙mero part number

        edd = "EDD"
        dwg = "DWG"
        schematic = "SCHEMATIC"
        for part in range(len(list_assemblies)):
            partnumber = list_assemblies[part][1]
            description = list_assemblies[part][3]
            if "EDD" in partnumber:
                edd = ""
            elif "DWG" in partnumber:
                dwg = ""
            elif "SCHEMATIC" in description:
                schematic = ""
        return edd, dwg, schematic

    def final_dict(self, dict_Tables):
        dict_Partnumbers = {}
        dict_AdditionalFeatures = {}
        for mount in dict_Tables:
            dict_Partnumbers[mount] = {}
            dict_AdditionalFeatures[mount] = {}
            for assembly in dict_Tables[mount]:
                dict_Partnumbers[mount][assembly] = {}
                dict_AdditionalFeatures[mount][assembly] = {}
                table = dict_Tables[mount][assembly]
                partnumbers, additional_features = self.get_partnumbersExcel(table)
                for value in partnumbers:
                    if not value in dict_Partnumbers[mount][assembly]:
                        dict_Partnumbers[mount][assembly][value] = partnumbers[value]
                    else:
                        erro = "Partnumber repetida em: " + assembly + " em " + mount
                        self.errorList.append(erro + "\n")
                for value in additional_features:
                    if not value in dict_AdditionalFeatures[mount][assembly]:
                        dict_AdditionalFeatures[mount][assembly][value] = additional_features[value]
                    else:
                        erro = "Partnumber repetida em: " + assembly + " em " + mount
                        self.errorList.append(erro + "\n")
        return dict_Partnumbers, dict_AdditionalFeatures

    def get_partnumbersExcel(self, table):
        partnumbers = {}
        additional_features = {}
        for item in range(len(table)):
            IsNumber = re.match('\d{1,}', table[item][0])  # check if there are digits in de F/N column
            if IsNumber:
                number = table[item][1]
                description = table[item][3]
                if not table[item][5] == "PC":
                    additional_features[number] = {"qty": 1, "description": description}
                else:
                    qty = table[item][4]
                    partnumbers[number] = {"qty": qty, "description": description}
        return partnumbers, additional_features

    # Excel Main

    def EXCEL(self):

        # stage 2 - Checks coherence between ITEM MASTER Data and EBOM Data.
        self.checkCoherence()

        list_Excel = {}
        list_Excel["Components"] = self.dict_Partnumbers
        list_Excel["AdditionalFeatures"] = self.dict_AdditionalFeatures


        return list_Excel

    def get_sheet_CN(self):
        CN = self.sheet_APPROVAL.cell(4, 3).value  # retira valor do CN
        return CN

    def get_sheet_Revision(self):
        revision = self.sheet_APPROVAL.cell(4, 1).value  # retira valor da ultima revisao
        return revision

    def get_assembly(self, name):

        lenth_assembly = 0
        for chr in range(len(name)):
            if name[lenth_assembly] == ",":
                break
            else:
                lenth_assembly += 1

        assembly = name[:(lenth_assembly)]
        return assembly


# End of Class Excel

# #Excel
#
# # 1 get Assmeblies and tables
#
#
# def get_all(path):
#
#     book = xlrd.open_workbook(path)
#     sheet_EBOM_DATA = book.sheet_by_name("EBOM Data")
#     sheet_IMD = book.sheet_by_name("ITEM MASTER Data")
#     dict_RevAssemblies = get_RevAssemblies(sheet_IMD)
#     dict_DataList=  get_DataList(sheet_EBOM_DATA)
#
#     return dict_RevAssemblies, dict_DataList
#
#
#
# def get_RevAssemblies(sheet):
#     dict_RevAssembly = {"SM1" : {}, "SM2" : {}, "HP1" : {}, "CMP" : {}}
#     n_rows = sheet.nrows
#     for row in range(7, n_rows): #table starts at line 7
#         name = sheet.cell(row, 0).value
#         assembly = get_assembly(name)
#         item_name = sheet.cell(row, 1).value
#         if "SM1" in item_name:
#             dict_RevAssembly["SM1"][assembly] = item_name
#         elif "SM2" in item_name:
#             dict_RevAssembly["SM2"][assembly] = item_name
#         elif "HP1" in item_name:
#             dict_RevAssembly["HP1"][assembly] = item_name
#         elif "CMP" in item_name:
#             dict_RevAssembly["CMP"][assembly] = item_name
#
#
#     return dict_RevAssembly
#
#
# def get_assembly(name):
#
#     lenth_assembly=0
#     for chr in range(len(name)):
#         if name[lenth_assembly]==",":
#             break
#         else:
#             lenth_assembly += 1
#
#     assembly=name[:(lenth_assembly)]
#     return assembly
#
#
# def get_DataList(sheet_EBOMData):
#     list_Assemblies = Get_Assemblies(sheet_EBOMData)
#     dict_DataList = {"SM1" : {}, "SM2" : {}, "HP1" : {}, "CMP" : {}}
#     nRows = sheet_EBOMData.nrows
#     for list_index in range(len(list_Assemblies)-1): # nao verifica a última tabela
#         Assembly= list_Assemblies[list_index][1] #assembly number
#         list_dataList=[]
#
#         assemblyRow = list_Assemblies[list_index][0] #position 0 of array in list is the row number
#         start_row = get_StartRow(sheet_EBOMData, assemblyRow, nRows)
#         end_row = list_Assemblies[list_index+1][0]-2  #table ends 3 rows above partnumber
#         for row in range(start_row, end_row):
#             lineData = sheet_EBOMData.row_values(row, 1, 7)
#             list_dataList.append(lineData)
#
#         description = list_Assemblies[list_index][2]
#         mount = ""
#         if "SM1" in description:
#             mount = "SM1"
#         elif "SM2" in description:
#             mount = "SM2"
#         elif "HP1" in description:
#             mount = "HP1"
#         elif "CMP" in description:
#             mount = "CMP"
#         dict_DataList[mount][Assembly] = list_dataList
#
#
#     #last table
#     assemblyRow = list_Assemblies[len(list_Assemblies) - 1][0]
#     start_row = get_StartRow(sheet_EBOMData, assemblyRow, nRows)
#     end_row = sheet_EBOMData.nrows
#     Assembly = list_Assemblies[len(list_Assemblies)-1][1]
#     list_dataList = []
#     for row in range(start_row, end_row):
#         lineData = sheet_EBOMData.row_values(row, 1, 7)
#         list_dataList.append(lineData)
#
#     description = list_Assemblies[len(list_Assemblies)-1][2]
#     mount = ""
#     if "SM1" in description:
#         mount = "SM1"
#     elif "SM2" in description:
#         mount = "SM2"
#     elif "HP1" in description:
#         mount = "HP1"
#     elif "CMP" in description:
#         mount = "CMP"
#     dict_DataList[mount][Assembly] = list_dataList
#
#     return dict_DataList
#
#
#
# def get_StartRow(sheet, AssemblyRow, lenth_sheet):
#     for row in range(AssemblyRow, lenth_sheet):
#         x = sheet.cell(row, 0)
#         if sheet.cell(row, 0).value == "Ll":
#             startRow = row+1
#             break
#     return startRow
#
#
#
#
# def Get_Assemblies(sheet_EBOM_data):
#     list_Assemblies=[]
#     nrows = sheet_EBOM_data.nrows
#     for row in range(nrows):
#         if sheet_EBOM_data.cell(row, 0).value=="Part Number":
#             list_Assemblies.append([row, sheet_EBOM_data.cell(row, 1).value, sheet_EBOM_data.cell(row+3, 1).value])
#     return list_Assemblies #contains star row, assembly number and assembly description
#
#
# def checkCoherence(dict_RevAssemblies, dict_DataList):
#     for mount in dict_RevAssemblies:
#         for assembly in dict_RevAssemblies[mount]:
#             if not assembly in dict_DataList[mount]:
#                 error = "Error: Assembly: " + str(assembly) + " , " + str(mount) + " from ITEM MASTER Data is not present in " + str(mount) + " in EBOM Data"
#                 add_error_item(error)
#
#
# def checkCMP(dict_DataList):
#     if dict_DataList["CMP"] != {}:
#         retrieveData(dict_DataList["CMP"])
#
#
#
#
#
#
# def retrieveData(dict_CMPAssemblies):
#     for assembly in dict_CMPAssemblies:
#         edd, dwg, schematic = get_Features(dict_CMPAssemblies[assembly])
#         if edd != "" or dwg != "" or schematic != "":
#             error = "Assembly: " + assembly + " => CMP is missing " + edd + " " +  dwg + " " + schematic
#             add_error_item(error)
#
#
# def get_Features(list_assemblies):  # número part number
#
#     edd = "EDD"
#     dwg = "DWG"
#     schematic = "SCHEMATIC"
#     for part in range(len(list_assemblies)):
#         partnumber =list_assemblies[part][1]
#         description = list_assemblies[part][3]
#         if "EDD" in partnumber:
#             edd = ""
#         elif "DWG" in partnumber:
#             dwg = ""
#         elif "SCHEMATIC" in description:
#             schematic = ""
#     return edd, dwg, schematic
#
#
# def final_dict(dict_Tables):
#     dict_Partnumbers = {}
#     dict_AdditionalFeatures = {}
#     for mount in dict_Tables:
#         dict_Partnumbers[mount]={}
#         dict_AdditionalFeatures[mount]={}
#         for assembly in dict_Tables[mount]:
#             dict_Partnumbers[mount][assembly] ={}
#             dict_AdditionalFeatures[mount][assembly] = {}
#             table = dict_Tables[mount][assembly]
#             partnumbers, additional_features = get_partnumbersExcel(table)
#             for value in partnumbers:
#                 if not value in dict_Partnumbers[mount][assembly]:
#                     dict_Partnumbers[mount][assembly][value] = partnumbers[value]
#                 else:
#                     erro = "Partnumber repetida em: " + assembly + " em " + mount
#             for value in additional_features:
#                 if not value in dict_AdditionalFeatures[mount][assembly]:
#                     dict_AdditionalFeatures[mount][assembly][value] = additional_features[value]
#                 else:
#                     erro = "Partnumber repetida em: " + assembly + " em " + mount
#
#     return dict_Partnumbers, dict_AdditionalFeatures
#
#
#
#
# def get_partnumbersExcel(table):
#     partnumbers = {}
#     additional_features = {}
#     for item in range(len(table)):
#         IsNumber=re.match('\d{1,}', table[item][0]) #check if there are digits in de F/N column
#         if IsNumber:
#             number = table[item][1]
#             description = table[item][3]
#             if not table[item][5]=="PC":
#                 additional_features[number] = {"qty" : 1, "description" : description}
#             else:
#                 qty = table[item][4]
#                 partnumbers[number] = {"qty": qty, "description": description}
#     return partnumbers, additional_features
#
#
#
# #Excel Main
#
# def EXCEL(path):
#     #stage 1 - collect assemblies revised and collect independent tables
#     dict_RevAssemblies, dict_DataList = get_all(path)
#     pass
#
#
#     #stage 2 - Checks coherence between ITEM MASTER Data and EBOM Data.
#     checkCoherence(dict_RevAssemblies, dict_DataList)
#
#
#     #stage 3 - Checks if all the needed components in CMP are in place (DWG,EDD and SCHEMATIC), retrieves and filters Part Numbers, getting the final dictionary to compare with PDF File.
#     checkCMP(dict_DataList)
#     dict_Partnumbers, dict_AdditionalFeatures = final_dict(dict_DataList)
#     pass
#
#
#     f = open("files/ExcelPartnumbers.json", "w+")
#     f.write(json.dumps(dict_Partnumbers, indent=4, sort_keys=True))
#     f = open("files/ExcelAdditionalFeatures.json", "w+")
#     f.write(json.dumps(dict_AdditionalFeatures, indent=4, sort_keys=True))
#     pass
#
#     list_Excel = []
#     list_Excel.append(dict_Partnumbers)
#     list_Excel.append(dict_AdditionalFeatures)
#
#     return list_Excel


#compare

def compare(InfoPDF, InfoExcel):  # Pdf has 4 dict and excel has 2

    with open(InfoPDF, 'r') as f:
        dictionaryPDF = json.load(f)
    with open(InfoExcel, 'r') as f:
        dictionaryExcel = json.load(f)


    dictPDF_Components = dictionaryPDF["Components"]
    dictPDF_OptComponents = dictionaryPDF["OptionalComponents"]
    dictPDF_AdditionalFeatures = dictionaryPDF["AdditionalFeatures"]
    dictPDF_OptAdditionalFeatures = dictionaryPDF["OptionalAdditionalFeatures"]
    dictExcel_Components = dictionaryExcel["Components"]
    dictExcel_AdditionalFeatures = dictionaryExcel["AdditionalFeatures"]
    check_Partnumbers(dictPDF_Components, dictPDF_OptComponents, dictExcel_Components) #validation of inserted components
    check_Partnumbers(dictPDF_AdditionalFeatures, dictPDF_OptAdditionalFeatures, dictExcel_AdditionalFeatures) #validation of inserted addtional features




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
        errorDisc(partnumber, assembly, mount)

def checkQty(partnumber, assembly, mount, dictPDF_Partnumbers, dictPDF_OptPartnumbers, dictExcel_Partnumbers):
    qtyPDF = int(dictPDF_Partnumbers[mount][assembly][partnumber]["qty"])
    qtyExcel = int(dictExcel_Partnumbers[mount][assembly][partnumber]["qty"])
    if qtyPDF > qtyExcel:
        errorQTY(partnumber, assembly, mount, qtyExcel, qtyPDF)
    elif qtyPDF < qtyExcel:
        compareOPT(partnumber, assembly, mount, dictPDF_Partnumbers, dictPDF_OptPartnumbers,dictExcel_Partnumbers)



def compareOPT(partnumber, assembly, mount, dictPDF_Partnumbers, dictPDF_OptPartnumbers,dictExcel_Partnumbers):
    qtyPDF = (dictPDF_Partnumbers[mount][assembly][partnumber]["qty"])
    qtyExcel = (dictExcel_Partnumbers[mount][assembly][partnumber]["qty"])
    qtyOPT = (dictPDF_OptPartnumbers[mount][assembly][partnumber]["qty"])
    if not existsInDictionary(partnumber, assembly, mount, dictPDF_OptPartnumbers):
        errorQTY(partnumber, assembly, mount, qtyExcel, qtyPDF)
    else:
        qty_OPTplusInserted = qtyPDF + qtyOPT
        if qtyExcel > qty_OPTplusInserted: #checks if qty in excel is higher than the sum of mandatory partnumbers and optional
            errorQTY(partnumber, assembly, mount, qtyExcel, qtyPDF)


def existsInDictionary(partnumber, assembly, mount, dictionary):
    aux = False
    if mount in dictionary:
        if assembly in dictionary[mount]:
            if partnumber in dictionary[mount][assembly]:
                aux = True
    return aux

def errorQTY(partnumber, assembly, mount, qtyExcel, qtyPDF):
    error = "ERROR: Quantity of partnumber " + partnumber + " in assembly " + assembly + " " + mount + " in Excel: "\
            +  str(qtyExcel) + " different from quantity in PDF: " + str(qtyPDF)
    add_error_item(error)

def errorDisc(partnumber, assembly, mount):
    error = "WARNING: Description of partnumber " + partnumber + " in assembly " + assembly + " " + mount + " does not match between PDF and Excel"
    add_error_item(error)






