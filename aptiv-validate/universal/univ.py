import re

#checks at which column starts the partnumbers
def check_start_column(dataframe):
    aux = False
    x = -1
    while not aux:
        x += 1
        if not type(dataframe[x][0]) == float:
             if not re.match('\d{5,}', dataframe[x][0]): #cell has to have 5 or more digits
                aux= True
    return  x