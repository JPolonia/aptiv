path_error = "files/Errors_List.txt"
# from ..main import path_error

def create_file():
    error_file = open(path_error,"w+")
    #error_file.write("No Errors")
    error_file.close()


def add_error_item(error):
    error_file = open(path_error, "a")
    error_file.write(error + "\n")
    error_file.close()


#final imprimir no errors