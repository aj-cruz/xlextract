from xlextract.classes import OpenPyXLGetSheet, OpenPyXLGetKeyCoords


class BaseExtract:
    def __init__(self, xlfile: str, sheet: str, keyword: str):
        self.filename: str = xlfile
        self.sheetname: str = sheet
        self.sheet = OpenPyXLGetSheet(xlfile, sheet).get_sheet()
        self.keyword: str = keyword
        self.keycoords: str = OpenPyXLGetKeyCoords(
            self.sheet, sheet, self.keyword
        ).coords
        self.value: list | str = []

    def __str__(self) -> str:
        return f"{self.sheet}({self.keyword})"

    def RLookup(self) -> None:
        raise NotImplementedError

    def LLookup(self) -> None:
        raise NotImplementedError

    def TLookup(self) -> None:
        raise NotImplementedError


class XLExtract(BaseExtract):
    def RLookup(self) -> None:
        """
        Returns the value (string) of the cell to the Right of the keyword
        """
        row: int = self.sheet[self.keycoords].row
        col: int = self.sheet[self.keycoords].column + 1
        self.value = self.sheet.cell(row, col).value

    def LLookup(self) -> None:
        """
        Returns the value (string) of the cell to the Left of the keyword
        """
        row: int = self.sheet[self.keycoords].row
        col: int = self.sheet[self.keycoords].column - 1
        self.value = self.sheet.cell(row, col).value

    def BLookup(self) -> None:
        """
        Returns the value (string) of the cell immediately below the keyword
        """
        row: int = self.sheet[self.keycoords].row + 1
        col: int = self.sheet[self.keycoords].column 
        self.value = self.sheet.cell(row, col).value

    def TLookup(self) -> None:
        """
        Function to build a table (dict) of data. Using keyword coordinates as a
        reference point. Searches down, left, and right of the reference coords
        and builds a table of all data (list of flat dictionaries) ending when it
        encounters the first empty cell (assumes all data is populated contiguously)
        """
        table: list = []
        # Establish points of reference
        header_row: int = self.sheet[self.keycoords].row
        data_row: int = self.sheet[self.keycoords].row + 1
        keyword_column: int = self.sheet[self.keycoords].column

        # Establish column range/table width by discovering header text
        col_range: list[int] = [keyword_column, keyword_column]
        left_current_column: int = keyword_column
        while True:  # Begin Searching Left of Keyword
            left_cell_content: str = self.sheet.cell(
                header_row, left_current_column
            ).value
            if (
                not left_cell_content
            ):  # Encountered empty cell, exit left boundary discovery
                col_range[0] = left_current_column + 1
                break
            elif left_current_column == 1:  # Left edge of the spreadsheet reached
                col_range[0] = 1
                break
            else:
                left_current_column -= 1

        right_current_column: int = keyword_column
        while True:  # Begin Searching Right of Keyword
            try:
                right_cell_content: str = self.sheet.cell(
                    header_row, right_current_column
                ).value
            except IndexError:
                col_range[1] = right_current_column
                break
            if (
                not right_cell_content
            ):  # Encountered empty cell, exit right boundary discovery
                col_range[1] = right_current_column
                break
            else:
                right_current_column += 1

        col_start: int = col_range[0]
        col_end: int = col_range[1]

        # Loop through the rows and columns to build the table
        while True:
            cell_content: str | None
            try:
                cell_content = self.sheet.cell(data_row, keyword_column).value
            except IndexError:
                cell_content = None
            if not cell_content:  # Empty cell detected, exit table build
                break
            else:
                # Build dictionary for this row using header row as the keys
                this_row_dict: dict = {}
                for col in range(col_start, col_end):
                    dict_key: str = self.sheet.cell(header_row, col).value
                    dict_val: str = self.sheet.cell(data_row, col).value
                    this_row_dict[dict_key] = dict_val
                table.append(this_row_dict)
            data_row += 1  # All done with this row, move to next row
        self.value = table

        if not self.value:
            print(
                f"\nWARNING: The table generated for keyword '{self.keyword}' is empty. This probably means the cell immediately below the keyword is empty.\n"
            )
