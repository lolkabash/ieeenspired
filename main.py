# Imports
import PyPDF2
import requests
import io
import camelot
import pandas as pd


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
    # result.to_csv("sample1.csv")

    return result


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
        # print(txt)

        # Bookmarks of your pdf
        bookmarks = bookmark_dict(pdf, pdf.getOutlines())
        flipped_bookmarks = dict([(value, key) for key, value in bookmarks.items()])
        filtered_bookmarks = bookmark_filter(bookmarks, search_start, search_end)
        search_pages = list(filtered_bookmarks.values())
        sp_string = "-".join(map(str, search_pages))
        range_pages = [
            item
            for item in flipped_bookmarks.keys()
            if search_pages[0] <= item <= search_pages[1]
        ]

        # Debugging
        # print(bookmarks)
        # print(filtered_bookmarks)
        # print(flipped_bookmarks)
        # print(search_pages)
        # print(range_pages)
        print(pdf_csv_generator(urlpdf, "14-30"))

        return


# Variables & Calling main function
urlpdf = "https://h20195.www2.hp.com/v2/getpdf.aspx/c04932490.pdf"
onlinepdfparser(urlpdf)