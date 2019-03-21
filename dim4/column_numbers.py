
def number_vertical_assemblys(verticalAssemblyDict):
    total_columns = {}
    for key in verticalAssemblyDict:
        total_columns[key] = len(verticalAssemblyDict[key])
    return total_columns


def columns_to_analyze(revAssemblyList, verticalAssemblyDict):
    positions = {"SM1" : {}, "SM2" : {}, "HP1" : {} }
    total_columns = number_vertical_assemblys(verticalAssemblyDict)
    for mount in revAssemblyList:
        if revAssemblyList[mount] is not None:
            if mount in verticalAssemblyDict:
                for i in range(total_columns[mount]):
                    if verticalAssemblyDict[mount][i] in revAssemblyList[mount]:
                        positions[mount][verticalAssemblyDict[mount][i]] = i
    return positions
