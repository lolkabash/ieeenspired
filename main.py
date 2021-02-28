# Imports
import PyPDF2
import requests
import io
import camelot
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Extracting all the bookmarks from PDF
def bookmark_dict(pdf, bookmark_list):
    result = {}
    for item in bookmark_list:
        if isinstance(item, list):
            # recursive call
            result.update(bookmark_dict(pdf, item))
        else:
            try:
                result[item.title] = pdf.getDestinationPageNumber(item) + 1
            except:
                pass
    return result


# Filtering Dictionary Of Bookmarks for Specific Key Terms
def bookmark_filter(bookmarks, search_start, search_end):

    start = None
    end = None
    temp = {}
    filtered_bookmarks = {}

    for key in bookmarks:
        if search_start in key and key not in temp:
            temp[key] = bookmarks[key]
            start = key
        if search_end in key and start in temp:
            temp[key] = bookmarks[key]
            end = key
            break

    filtered_bookmarks[start] = temp[start]
    filtered_bookmarks[end] = temp[end]

    return filtered_bookmarks


# Generates a Pandas Dataframe which can be exported as CSV
def pdf_csv_generator(pdf, search_range):
    # Extract all PDF tables using Camelot
    tables = camelot.read_pdf(pdf, pages=search_range, strip_text="\n", flag_size=True)

    # Convert extracted table into Panda dataframe
    frames = []
    for i in range(len(tables)):
        df = tables[i].df
        df.replace("<s\s*.*>\s*.*<\/s>", "", regex=True, inplace=True)
        frames.append(df)

    # Table Title
    title = list(frames[0].iloc[0])[0]

    print(title)

    # Get the column headers
    headers = list(frames[0].iloc[1])

    # Discard the first 2 rows from all dataframes
    for df in frames:
        df.drop(df.index[:2], inplace=True)
        # df.drop(df.index[:2], inplace=True)

    # Merge all dataframes into one
    result = pd.concat(frames, ignore_index=True)

    # Set the column header for the new dataframe
    result.columns = headers

    # Export as CSV
    csv_name = "data.csv"
    result.to_csv(csv_name)
    print(f"Created lookup file: {csv_name}")
    return result


# Formatting list of ranges into strings
def range_format(pages):
    return "-".join(map(str, pages))


# Variable URL PDF to get form search query for latest version
def onlinepdfparser(urlpdf):
    response = requests.get(urlpdf)

    with io.BytesIO(response.content) as file:
        # Opening File
        pdf = PyPDF2.PdfFileReader(file)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

        # Search Key Terms
        search_start = "Substance and Materials Requirements"
        search_end = "Revision History"

        # Metadata Template
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

        # Bookmarks of your pdf
        bookmarks = bookmark_dict(pdf, pdf.getOutlines())
        flipped_bookmarks = dict([(value, key) for key, value in bookmarks.items()])
        filtered_bookmarks = bookmark_filter(bookmarks, search_start, search_end)
        search_pages = list(filtered_bookmarks.values())
        range_pages = [
            item
            for item in flipped_bookmarks.keys()
            if search_pages[0] <= item <= search_pages[1]
        ]

        # Variable Search
        search_string = range_format(range_pages[1:3])

        # Debugging
        # print(bookmarks)
        # print(filtered_bookmarks)
        # print(flipped_bookmarks)
        # print(search_pages)
        # print(range_pages)
        # print(search_string)
        print(pdf_csv_generator(urlpdf, search_string))
        return


# Searching for latest document
def get_link(search, results):
    page = requests.get(f"https://www.google.com/search?q={search}&num={results}")
    soup = BeautifulSoup(page.content, "html5lib")
    links = soup.findAll("a")

    extracted_links = []
    for link in links:
        link_href = link.get("href")
        if "url?q=" in link_href and not "webcache" in link_href:
            temp_link = link.get("href").split("?q=")[1].split("&sa=U")[0]
            extracted_links.append(temp_link)
    return extracted_links


# Variables & Calling main function

# Main UI
def run():
    print(
        """
    Welcome to the tool to help you generate a data.csv lookup table
    using the latest HP General Specification for Environment (GSE)
    document available!
    """
    )

    search = "HP General Specification for Environment (GSE) Substances and Materials Requirements"
    results = 5  # valid options 10, 20, 30, 40, 50, and 100

    print(
        f"""
    Searching using the search term: [{search}]
    
    Showing the first {results} results...
    """
    )

    extracted_links = get_link(search, results)[0:5]

    for link in extracted_links:
        print(link)

    urlpdf = extracted_links[0]

    print(
        f"""
    Choosing the best option...
    Selected: {urlpdf}
    """
    )

    print(
        """
    Generating lookup table...
    """
    )

    onlinepdfparser(urlpdf)

    return


run()