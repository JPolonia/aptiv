from dim2.rev_letter import rev
from dim2.data_list import select_data
from dim2.mounts import mounts_list
from dim2.vertical_assembly import retrieve_data

def retrieve(path, pages):
    rev_letter = rev(pages[0])
    data_list = select_data(pages)
    mount_list = mounts_list(pages)
    verticalAssemblyList = retrieve_data(path, pages)

    return rev_letter, data_list, mount_list, verticalAssemblyList




