
#creates deictionary, keys are mounts and the data ara the respective pages of that mount
def assoc(data_list, mount_list):
    dict = {}
    for i in range(len(data_list)):
        dict[mount_list[i]] = data_list[i]
    if not len(data_list) == len(mount_list):
        from errors.error_list import add_error_item
        add_error_item("Not every mount from 1st page is defined through out PDF or otherwise, rest of analysis might be corrupted")
    return dict

