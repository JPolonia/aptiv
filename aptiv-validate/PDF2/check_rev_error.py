from universal.univ import check_start_column
from errors.error_list import add_error_item


def rev_error(page):
    dataframe = page[3]
    startColumn = check_start_column(dataframe)
    list_Finders = []
    list_Rev = []

    for row in range(len(dataframe[0])-1, -1, -1):
        if type(dataframe[startColumn][row]) != float:
            if "." in dataframe[startColumn][row]:
                revLetter = dataframe[startColumn+3][row]
                list_Rev.append(revLetter)
                list_Finders.append(list_Rev)
                list_Rev.reverse()
                list_Rev = []
            else:
                revLetter = dataframe[startColumn+3][row]
                list_Rev.append(revLetter)

    list_Finders.reverse()



    for finder in range(len(list_Finders)):
        counter = 0
        last_Rev = list_Finders[finder][0]
        for revision in range(1, len(list_Finders[finder])):
            revLetter = list_Finders[finder][revision]
            if revLetter == last_Rev:
                counter+=1
            elif revLetter >= last_Rev:
                error = "Error: Assembly in position " + str(revision +1) + " has later revision than CMP in finder "+ str(finder + 1)
                add_error_item(error)
        if counter == 0:
            warning = "Warning: CMP has later revision than all assemblies in finder " + str(finder +1)
            add_error_item(warning)



