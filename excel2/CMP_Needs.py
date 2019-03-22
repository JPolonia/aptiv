def cmp_additional_features(x, first_sheet, pnos):  # número part number

    a = 0
    b = 0
    c = 0
    if x != len(pnos) - 1:
        for y in range(pnos[x][0] + 18, pnos[x + 1][0] - 2):
            df = first_sheet.cell(y, 2).value
            ef = first_sheet.cell(y, 4).value
            if df[0:3] == "EDD":
                a = 1
            elif df[0:3] == "DWG":
                b = 1
            elif ef[0:9] == "SCHEMATIC":
                c = 1
    else:
        for y in range(pnos[x][0] + 18, first_sheet.nrows - 1):
            df = first_sheet.cell(y, 2).value
            ef = first_sheet.cell(y, 4).value
            if df[0:3] == "EDD":
                a = 1
            elif df[0:3] == "DWG":
                b = 1
            elif ef[0:9] == "SCHEMATIC":
                c = 1
    d = ""
    if a == 0:
        d += "Falta EDD. "
    if b == 0:
        d += "Falta DWG. "
    if c == 0:
        d += "Falta SCHEMATIC. "
    if a == 1 and b == 1 and c == 1:
        return ("Complete corretamente estipulada.")
    else:
        return b

def ser_cmp(partname):
    a = 0
    for x in range(len(partname) - 3):
        b=partname[x:x + 3]
        if b == "CMP":
            a = 1
    return a
