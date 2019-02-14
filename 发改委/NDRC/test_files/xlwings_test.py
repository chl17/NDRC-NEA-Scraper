import xlwings as xw

file_path = '/Users/chenhaolin/PycharmProjects/SRT/发改委/NDRC/FILES/test_xls.xls'
wb = xw.Book(file_path)
sheet = wb.sheets[0]
RANGE = sheet.range('A1').expand('table')
row_count = RANGE.rows.count
col_count = RANGE.columns.count
print(str(row_count) + ' ' + str(col_count))

print(RANGE.rows)

for row in range(row_count):
    print(sheet.range('A' + str(row + 1)).value)
