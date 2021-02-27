import camelot
import pandas as pd

tables = camelot.read_pdf(pdf, pages=search_pages, strip_text="\n", flag_size=True)

frames = []
for i in range(len(tables)):
    frames.append(tables[i].df)
headers = list(frames[0].iloc[1])
for df in frames:
    df.drop(df.index[:2], inplace=True)
result = pd.concat(frames, ignore_index=True)
result.columns = headers

result.to_csv("sample.csv")