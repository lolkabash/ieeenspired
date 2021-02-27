# You need install :
# pip install PyPDF2 - > Read and parse your content pdf
# pip install requests - > request for get the pdf
# pip install BeautifulSoup - > for parse the html and find all url hrf with ".pdf" final
from PyPDF2 import PdfFileReader
import requests
import io
from bs4 import BeautifulSoup


urlpdf = "https://h20195.www2.hp.com/v2/getpdf.aspx/c04932490.pdf"
response = requests.get(urlpdf)
with io.BytesIO(response.content) as f:
    pdf = PdfFileReader(f)
    information = pdf.getDocumentInfo()
    number_of_pages = pdf.getNumPages()
    txt = f"""
    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """
    # Here the metadata of your pdf
    print(txt)
    # numpage for the number page
    for i in range(10, 21):
        print(f"\n\nPage {i}\n\n")
        numpage = i
        page = pdf.getPage(numpage)
        page_content = page.extractText()
        # print the content in the page 20
        print(page_content)