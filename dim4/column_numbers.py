
def number_vertical_assemblys(verticalAssemblyDict):
    total_columns = {}
    for key in verticalAssemblyDict:
        total_columns[key] = len(verticalAssemblyDict[key])
    return total_columns


def columns_to_analyze(revAssemblyList, verticalAssemblyDict):
    positions = {"SM1" : [], "SM2" : [], "HP1" : [] }
    total_columns = number_vertical_assemblys(verticalAssemblyDict)
    for key in revAssemblyList:
        if revAssemblyList[key] is not None:
            for i in range(total_columns[key]):
                if verticalAssemblyDict[key][i] in revAssemblyList[key]:
                    positions[key].append(i)
    return positions
