#from tabula import convert_into
#convert_into('/Users/diogovalentepcs/Documents/FEUP/Academic_Games/24090330_with_Error/24090330_H.pdf', '/Users/diogovalentepcs/Documents/FEUP/Academic_Games/24090330_with_Error/teste123.csv', output_format= "csv" )




#from PyPDF2 import PdfFileReader
#input1 = PdfFileReader(open('/Users/diogovalentepcs/Documents/FEUP/Academic_Games/24090330_with_Error/24090330_H.pdf', 'rb'))
#input1.getPage(0).mediaBox
#RectangleObject([0, 0, 612, 792])


import pandas as pd
from tabula import  read_pdf
tabula1 = read_pdf('/Users/diogovalentepcs/Documents/FEUP/Academic_Games/24090330_with_Error/24090330_H.pdf', output_format="csv", encoding= 'utf-8', java_options= None, multiple_tables=True)

df = pd.DataFrame(tabula1)
pass



#df.at[4, 'B']

print(df)
# df.to_csv('/Users/diogovalentepcs/Documents/FEUP/Academic_Games/24090330_with_Error/2345.pdf')
#
#
# pd.to_csv()
#new_df = pd.DataFrame
#new_df = pd.concat([new_df, df], axis=0, ignore_index= True)
#print(new_df)
#new_df.to_csv('/Users/diogovalentepcs/Documents/FEUP/Academic_Games/24090330_with_Error/teste1.csv',index=False)

#print(df)

#x = df.at[1, 1]
#print(x)

pass