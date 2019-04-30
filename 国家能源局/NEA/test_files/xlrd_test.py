import xlrd

file_path = '/Users/chenhaolin/PycharmProjects/SRT/发改委/NDRC/FILES/test_xls.xls'

data = xlrd.open_workbook(file_path)
table = data.sheets()[0]
table_names = data.sheet_names()
row_count = table.nrows
col_count = table.ncols
print(row_count)
print('\n')
print(type(col_count))
print(table_names)
content_list = []
content_cleaned = []
for table_name in table_names:
    table = data.sheet_by_name(table_name)
    row_count = table.nrows
    col_count = table.ncols
    for col in range(col_count):
        content_list = content_list + table.col_values(col)
for element in content_list:
    if element != '' and (not ((type(element) == int) or (type(element) == float))):
        content_cleaned.append(str(element))
print(' '.join(content_cleaned))
a = 1.0
print(type(a) == int)