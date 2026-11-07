import pandas as pd

csv = pd.read_csv('out.csv', sep=';')

excelWriter = pd.ExcelWriter('new.xlsx')

csv.to_excel(excelWriter, index_label="index")

excelWriter.close()