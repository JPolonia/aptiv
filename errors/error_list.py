path_error = "files/Errors_List.txt"

def create_file():
    error_file = open(path_error,"w+")
    error_file.write("No Errors")
    error_file.close()


def add_error_item(error):
    error_file = open(path_error, "-a")
    line = error + "\n"
    error_file.writelines(line)
    error_file.close()
