def check(page):
    data = ""
    if len(page) >= 4: #tem que ter o item 0 e o item 1
        data = page[3][0][0]  # returns dataframe no1 of page, then returns series number 4 of dataframe and finally returns data from index 0
    if not data=="If Package name is not available, then up to 15 characters of the geometry name\rwill appear in parentheses":
        page = "ignore"
    return page


def check_all(pages):
    n_pages = len(pages)
    for x in range(1, n_pages):
        pages[x] = check(pages[x])
    return pages
