import camelot
import pandas as pd


def pdf_csv_generator(pdf, search_range):
    # Extract all PDF tables using Camelot
    tables = camelot.read_pdf(pdf, pages="14-30", strip_text="\n", flag_size=True)

    # Convert extracted table into Panda dataframe
    frames = []
    for i in range(len(tables)):
        frames.append(tables[i].df)

    # Get the column headers
    headers = list(frames[0].iloc[1])

    # Discard the first 2 rows from all dataframes
    for df in frames:
        df.drop(df.index[:2], inplace=True)

    # Merge all dataframes into one
    result = pd.concat(frames, ignore_index=True)

    # Set the column header for the new dataframe
    result.columns = headers

    # Export as CSV
    # result.to_csv("sample1.csv")

    return result


search_range = "14-30"
