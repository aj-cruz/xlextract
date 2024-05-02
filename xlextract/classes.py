import openpyxl  # type: ignore


class GetSheet:
    def __init__(self, xlfile: str, sheet: str) -> None:
        self.filename: str = xlfile
        self.sheetname: str = sheet

    def __str__(self) -> str:
        return f"{self.filename}/{self.sheetname}"

    def get_sheet(self):
        raise NotImplementedError


class OpenPyXLGetSheet(GetSheet):
    def get_sheet(self):
        wb = openpyxl.load_workbook(self.filename)
        return wb[self.sheetname]


class GetKeyCoords:
    def __init__(self, sheet, sheetname: str, keyword: str) -> None:
        self.sheet = sheet
        self.sheetname: str = sheetname
        self.keyword: str = keyword
        self.extracted_coords: list = []
        self.coords: str = ""

        self.get_coords()
        self.validate_coordinates()

    def get_coords(self) -> None:
        raise NotImplementedError

    def validate_coordinates(self) -> None:
        if (
            len(self.extracted_coords) > 1
        ):  # Invalid sheet, multiple instances of the keyword found
            raise ValueError(
                f"Multiple instances of keyword '{self.keyword}' was found in sheet '{self.sheetname}'. Please ensure keywords are uniue in the sheet."
            )
        elif len(self.extracted_coords) == 0:  # Invalid sheet, keyword not found
            raise ValueError(
                f"Keyword '{self.keyword}' was not found in sheet '{self.sheetname}'."
            )

        self.coords = self.extracted_coords[0]


class OpenPyXLGetKeyCoords(GetKeyCoords):
    def get_coords(self) -> None:
        # LOCATE KEYWORD IN SHEET
        for row in self.sheet.iter_rows():  # Loop through rows in the Excel sheet
            for cell in row:  # Loop through columns (cells) in the row
                if cell.value and cell.value == self.keyword:
                    self.extracted_coords.append(cell.coordinate)
