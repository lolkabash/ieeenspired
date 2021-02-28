## Specifications:

# PS1:
1. Translate Sample Document (Chinese/Japanese > English)
2. Extract Chemical Data & Transfer it to client_excel_sheet sorted by category
3. Internet search for HP General Specification for Environment (GSE)
✔️ 4. Navigate to GSE document
✔️ 5. Navigate to relevant document: “Substances and Materials Requirements”
✔️ 6. Find the tables with chemical information to be checked against
✔️ 7. Extract and covert tables to universal format (Excel/JSON)
✔️ 8. Match chemicals in Step 2. to look-up table in Step 7
9. Append relevant chemical information to client_excel_sheet from look-up table
10. Profit


# Additional Features:
1. Analyse the various generated client_excel_sheet for:
> The most common requested chemicals (Graphs)
> The least commonly requested chemical
> Build a database of the various chemicals requested along with timestamp to show trend of client's request

# To predict trends in sustainability.

## To generate the lookup table, run `main.py`.