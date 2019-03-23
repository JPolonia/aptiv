import re

def check_rev(rev_letter,dataframe, start_column):
    column = start_column + 3
    positions = []
    for x in range(len(dataframe[column])):
        if dataframe[column][x] == rev_letter:
            positions.append(x)
    return positions


def get_assemblyLocals(rev_letter,dataframe):
    assemblyList = {"SM1": [], "SM2": [], "HP1": []}
    start_column = check_start_column(dataframe)
    positions = check_rev(rev_letter,dataframe, start_column)
    for value in positions:
        if "SM1" in dataframe[start_column + 1][value]:
            assemblyList["SM1"].append(dataframe[start_column][value])
            sorted(assemblyList["SM1"])
        elif "SM2" in dataframe[start_column + 1][value]:
            assemblyList["SM2"].append(dataframe[start_column][value])
            sorted(assemblyList["SM2"])
        elif "HP1" in dataframe[start_column + 1][value]:
            assemblyList["HP1"].append(dataframe[start_column][value])
            sorted(assemblyList["HP1"])

    return assemblyList




