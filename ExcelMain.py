path = "files/Impact_Report_for_CN1080582853.xls"

#stage 1 - collect assemblies revised and collect independent tables
from excel1.get_all import get_all
dict_RevAssemblies, dict_DataList = get_all(path)
pass
