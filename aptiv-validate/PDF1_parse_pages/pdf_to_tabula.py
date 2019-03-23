import tabula
def pdf_to_tb(path, page):
    dt = tabula.read_pdf(path, output_format="dataframe", encoding="utf-8", java_options=None, pandas_options=None,
                         multiple_tables=True, pages=page)
    return dt  #returns list of the multiple dataframes inside a page

def pdf_to_tb_area(path, page, xl,yl, xr,yr):
    df = tabula.read_pdf(path, output_format="dataframe", encoding="utf-8", java_options=None, pandas_options=None,
                         multiple_tables=True, pages=page, spreadsheet=True, area=(xl,yl,xr,yr))
    return df


def pdf_to_tb_noPage(path):
    dt = tabula.read_pdf(path, output_format="dataframe", encoding="utf-8", java_options=None, pandas_options=None,
                         multiple_tables=True)
    return dt  #returns list of the multiple dataframes inside a page


