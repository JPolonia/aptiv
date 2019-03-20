def select_data(pages):
    data_list=[]

    n_pages = len(pages)
    i = n_pages

    aux = False
    i = 0
    while i < n_pages:
        if pages[i] == "ignore":
            if not i == n_pages-1:
                if not pages[i+1] == "ignore":
                    array = []
                    x = i +1
                    while pages[x] != "ignore":
                        array.append(pages[x])
                        x += 1
                    i = x - 1
                    data_list.append(array)
        i = i + 1
    return data_list