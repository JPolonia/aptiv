def rev(page):
    x = 0
    while x <= len(page[5][0][2]):
        rev = page[5][0][2][x]
        aux = True
        for i in range (x+1, x + 6):
            if not type(page[5][0][2][i]) == float:
                aux=False
        if aux:
            if not type(rev) == float:
                x = len(page[5][0][2])
        x +=1
    return rev







