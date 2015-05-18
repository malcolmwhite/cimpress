class Square:
    def __init__(self, row, col, size, row_major):
        self.X = col if row_major else row
        self.Y = row if row_major else col
        self.Size = size

    def __unicode__(self):
        return u'x: %d, y: %d, size: %d' % (self.X, self.Y, self.Size)

    def __str__(self):
        return 'x: %d, y: %d, size: %d' % (self.X, self.Y, self.Size)

    def get_row_start(self, row_major):
        return self.Y if row_major else self.X

    def get_row_end(self, row_major):
        length = self.Size - 1
        return self.Y + length if row_major else self.X + length

    def get_col_start(self, row_major):
        return self.X if row_major else self.Y

    def get_col_end(self, row_major):
        length = self.Size - 1
        return self.X + length if row_major else self.Y + length