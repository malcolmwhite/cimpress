class PuzzleSolution:
    def __init__(self, puzzle_id):
        self.id = puzzle_id
        self.squares = []

    def add_square(self, square):
        self.squares.append(square.__dict__)

    def get_squares(self):
        return self.squares