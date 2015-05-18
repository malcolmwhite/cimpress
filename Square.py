class Square:
    def __init__(self, row, col, size):
        self.X = col
        self.Y = row
        self.Size = size

    def __unicode__(self):
        return u'x: %d, y: %d, size: %d' % (self.X, self.Y, self.Size)