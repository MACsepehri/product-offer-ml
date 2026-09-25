import csv

class Reader:
    def __init__(self, filepath='all.csv'):
        with open(filepath, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)

            self.__columns = next(reader)
            self.__content = reader

    @property
    def columns(self): return self.__columns

    @property
    def content(self): return self.__content