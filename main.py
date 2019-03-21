path = "files/24090330_H.pdf"

#create error file
from errors.error_list import create_file
create_file()


#stage 1
# with this command we get all pages in a lsit. Each page is a list of dataframes containing all useful info. The pages that have no useful info are a string "ignore"
from dim1_parse_pages.get_pages import getPages
pages = getPages(path)

pass

#stage 2
#retrieve last rev letter, retrive list with separeted data, retrive mount list(checking which mounts are in pdf file)
from dim2.retrieve_all import retrieve
rev_letter, data_list, mount_list, verticalAssemblyList = retrieve(path, pages)

pass

#stage3
#associates data_list with mounts, returning the dictionary which will be analised
from dim3.associate import assoc
dictFile = assoc(data_list, mount_list)
verticalAssemblyDict = assoc(verticalAssemblyList, mount_list)

from dim3.check_rev_assemblies import revAssembliesList
revAssembliesList = revAssembliesList(pages, rev_letter)

pass

#stage4
#getting the columns positions to check in each mount
from dim4.column_numbers import columns_to_analyze
positions = columns_to_analyze(revAssembliesList, verticalAssemblyDict)


pass


#stage5
#buliding the full dictionary
from dim5.build_dictionary import final_dictionary
dict_FinalDataFile, dict_OptionalFinalDataFile = final_dictionary(dictFile,revAssembliesList, positions, verticalAssemblyDict)


pass
import json
f = open("files/dictTeste", "w+")
f.write(json.dumps(dict_FinalDataFile, indent=4, sort_keys=True))