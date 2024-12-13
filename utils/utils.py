class Point(object):
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        self._row = row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col

    def __str__(self):
        return f'Point(row={self._row}, col={self._col})'

    def __repr__(self):
        return f'Point(row={self._row}, col={self._col})'

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self._row, self._col))
