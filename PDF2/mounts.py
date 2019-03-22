from universal.univ import check_start_column


#returns boolean, wether each mount appears or not
def get_mounts(dataframe): #checks if there is SM1, SM2, HP1 in initial table
    start_column = check_start_column(dataframe)
    existsSM1 = False
    existsSM2 = False
    existsHP1 = False
    for x in range(len(dataframe[0])):
        if not type(dataframe[start_column + 1][x]) == float:
            if "SM1" in dataframe[start_column + 1][x]:
                existsSM1 = True
            elif "SM2" in dataframe[start_column + 1][x]:
                existsSM2 = True
            elif "HP1" in dataframe[start_column + 1][x]:
                existsHP1 = True
    return  existsSM1,  existsSM2, existsHP1



#returns list
def mounts_list(pages):
    list = []
    sm1, sm2, hp1 = get_mounts(pages[0][3]) #page 0 is the first one, and the info is in dataframe number 3, always
    if sm1:
        list.append("SM1")
    if sm2:
        list.append("SM2")
    if hp1:
        list.append("HP1")
    return list