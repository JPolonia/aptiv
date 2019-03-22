from universal.univ import check_start_column


#checks which rows have the latest revision
def last_revision_positions(rev_letter,dataframe, start_column):
    column = start_column + 3
    positions = []
    for x in range(len(dataframe[column])):
        if dataframe[column][x] == rev_letter:
            positions.append(x)
    return positions


#adds to respective mounts, the assemblies that are signelized as being last revised, this is the make up of my final dictionary
def revAssembliesList(pages, rev_letter):
    dataframe = pages[0][3]
    assemblyList = {"SM1": [], "SM2": [], "HP1": []}
    start_column = check_start_column(dataframe)
    positions = last_revision_positions(rev_letter,dataframe, start_column)
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
