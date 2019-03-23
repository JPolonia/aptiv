def check(page):
    aux = False
    for x in range(0,len(page) - 1):
        if page[x][0][0] == "If Package name is not available, then up to 15 characters of the geometry name\rwill appear in parentheses":
         aux = True
    if not aux:
        page = "ignore"
    return page



def ignore_complete(pages):  # assume que o cmp é só uma página e é a ultima não desenho
    n_pages = len(pages)
    i = n_pages
    aux = False

    while not aux and i > -1:
        if pages[i - 1] == "ignore":
            i = i - 1
        else:
            pages[i - 1] = "ignore"
            aux = True
    return pages
