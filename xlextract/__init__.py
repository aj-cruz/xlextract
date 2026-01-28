import pandas as pd
from xlextract.classes import OpenPyXLGetSheet, OpenPyXLGetKeyCoords


class BaseExtract:
    def __init__(self, xlfile: str, sheet: str, keyword: str, display_warnings: bool = True, data_only: bool = True):
        self.filename: str = xlfile
        self.sheetname: str = sheet
        self.sheet = OpenPyXLGetSheet(xlfile, sheet, data_only=data_only).get_sheet()
        self.display_warnings: bool = display_warnings
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
        Function to build a list of table data using pandas. Uses the keyword to
        locate the table header row, then builds a table of all data below the
        header row until it encounters the first empty row. Assumes all data is
        populated contiguously.
        """
        df: pd.DataFrame = pd.read_excel(self.filename, sheet_name=self.sheetname, header=None)

        # Locate the header row using the keyword
        matches = df.index[df.eq(self.keyword).any(axis=1)]
        if matches.empty:
            raise ValueError(
                f"\nNo table found for keyword '{self.keyword}' on sheet '{self.sheetname}'\n"
            )
        else:
            # If multiple matches found, warn user and use first match
            if len(matches) > 1:
                print(f"\nWarning: Keyword '{self.keyword}' found multiple times at rows {list(matches)}. Using the first occurrence.\n")
            header_idx = matches[0]
            header_idx = df.index[df.eq(self.keyword).any(axis=1)][0]

            table = df.iloc[header_idx + 1:]

            end_idx = table.index[table.isna().all(axis=1)]
            if not end_idx.empty:
                table = table.loc[:end_idx[0] - 1]

            headers = df.iloc[header_idx]

            cols_to_keep = [
                col for col in table.columns
                if not (pd.isna(headers[col]) and table[col].isna().all())
            ]

            table = table[cols_to_keep]
            table.columns = headers[cols_to_keep]

            table = table.astype(object).where(pd.notna(table), None)

            table = table.dropna(subset=[self.keyword])

            self.value = table.to_dict(orient="records")