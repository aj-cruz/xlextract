[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xlextract.svg)](https://img.shields.io/pypi/pyversions/xlextract)
[![PyPI](https://img.shields.io/pypi/v/xlextract.svg)](https://pypi.python.org/pypi/xlextract)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

XLExtract
=========

An abstraction layer for quickly pulling data out of Microsoft Excel Spreadsheets.

The project is currently powered by the [openpyxl](https://pypi.org/project/openpyxl/) library but you don't need to know anything about the underlying library and it could change in the future.

## Installation
xlextract can be installed via poetry with: ```poetry add xlextract```  
or via pip with: ```pip install xlextract```

## What does it do?
xlextract searches a spreadsheet for a keyword you provide and extracts nearby data.  
It provides three operations:
1. Right Lookup: Extract cell value to the immediate right of the keyword
2. Left Lookup: Extract cell value to the immediate left of the keyword
2. Bottom Lookup: Extract cell value immediateley below the keyword
3. Table Lookup: Extract an entire Excel table of data adjacent to the keyword. The table is modeled as a list of dictionaries where each list item represents a row in the table and the list item is a dictionary (key/value pairs) where each item in the dictionary represents a column of the row and where the key is the column header. An example will be provided below.

## How do I use it in my project?
You need four bits of information to use xlextract:
1. The name of the Excel file
2. The name of the sheet in the Excel file
3. The keyword you want to search for
4. The type of lookup you want to do (Right, Left, or Table)

The project provides a class named ```XLExtract``` that requires the first 3 inputs above as strings.  
The lookup is done via one of four class methods:
1. ```RLookup()``` (Right Lookup)
2. ```LLookup()``` (Left Lookup)
3. ```BLookup()``` (Bottom Lookup)
4. ```TLookup()``` (Table Lookup)

Here is an example of how to import the library and create a sheet object ready for lookup:
```python
import json # This is just to print our example table with formatting

from xlextract import XLExtract

vrf_table = XLExtract("design_document.xlsx", "Tenants", "VRF NAME")
```

# Table Lookup Example
Assuming we have an Excel spreadsheet with a "Tenants" tab that contains a table that looks like this:  
![Sample Excel Table](https://github.com/aj-cruz/xlextract/blob/main/art/ACI_VRF_Table.jpg?raw=true)
If we then do this in our Python code:
```python
vrf_table.TLookup()

print(json.dumps(vrf_table.value, indent = 4))
```

We would get the following output:
```python
[
    {
        "TENANT": "Prod-tn",
        "VRF NAME": "Prod-VRF",
        "ENABLE PREFERRED GROUP": "enabled"
    },
    {
        "TENANT": "Prod-tn",
        "VRF NAME": "Dev-VRF",
        "ENABLE PREFERRED GROUP": "enabled"
    }
]
```

## How does it do the table lookup?
The table lookup assumes the keyword you provide resides in the table header.  
It first searches cells left of the keyword, then right of the keyword to establish table width.  
When it encounters the first empty cell it assumes the edge of the table.  
Then it moves down from the keyword cell, if data is present it captures the row.  
When it encounters the first empty cell it assumes the bottom of the table, completing the extraction.

## CAVEATS
The source Excel spreadsheet content should be planned ahead of time to account for these operational caveats:
- Keywords on a given sheet must be unique
- Keywords for a table should be one of the column headers
- All cells in a table header should be populated for the table lookup to determine the correct table width
- All data cells in the keyword column should be populated for the table lookup to determine the correct table height. Because of this you should not use columns with optional data for the keyword, or if you must, populate all the cells in the column with something ("N/A" or "empty" if a cell has no value for example).