import tkinter
import camelot

tables = camelot.read_pdf("c04932490.pdf")
print(tables)
# tables.export("test.csv", f="csv", compress=True)  # json, excel, html, sqlite
# print(tables[0])
# print(tables[0].parsing_report)
