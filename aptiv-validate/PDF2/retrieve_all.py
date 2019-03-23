from PDF2.rev_letter import rev
from PDF2.data_list import select_data
from PDF2.mounts import mounts_list
from PDF2.vertical_assembly import retrieve_data
from PDF2.check_rev_error import rev_error

def retrieve(path, pages):

    rev_letter = rev(pages[0])
    data_list = select_data(pages)
    mount_list = mounts_list(pages)
    verticalAssemblyList = retrieve_data(path, pages)
    rev_error(pages[0])

    return rev_letter, data_list, mount_list, verticalAssemblyList




