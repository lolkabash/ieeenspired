import PyPDF2


def bookmark_dict(bookmark_list):
    result = {}
    for item in bookmark_list:
        if isinstance(item, list):
            # recursive call
            result.update(bookmark_dict(item))
        else:
            try:
                result[reader.getDestinationPageNumber(item) + 1] = item.title
            except:
                pass
    return result


def filter(bookmarks):
    search_start = "Substance and Materials Requirements"
    search_end = "Revision History"

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


reader = PyPDF2.PdfFileReader("c04932490.pdf")
bookmarks = bookmark_dict(reader.getOutlines())
# filtered_bookmarks = filter(bookmarks)
# search_pages = list(filtered_bookmarks.values())

print(bookmarks)
# print(list(filtered_bookmarks.values()))
