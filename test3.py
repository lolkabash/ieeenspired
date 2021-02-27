import PyPDF2

PDFFile = open("c04932490.pdf", "rb")

PDF = PyPDF2.PdfFileReader(PDFFile)
pages = PDF.getNumPages()
key = "/Annots"
uri = "/URI"
ank = "/A"

for page in range(pages):

    pageSliced = PDF.getPage(page)
    pageObject = pageSliced.getObject()

    if pageObject.has_key(key):
        ann = pageObject[key]
        for a in ann:
            u = a.getObject()
            if u[ank].has_key(uri):
                print(u[ank][uri])