class Square:
    def __init__(self, X, Y, size):
        self.X = X
        self.Y = Y
        self.size = size

    def __unicode__(self):
        return u'x: %d, y: %d, size: %d' % (self.X, self.Y, self.size)

    def __str__(self):
        return 'x: %d, y: %d, size: %d' % (self.X, self.Y, self.size)