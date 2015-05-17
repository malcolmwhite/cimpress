from numpy import subtract, asarray, copy, zeros
import Square as sq
import matplotlib.pyplot as plt


class PuzzleSolver(object):
    API_KEY = "38c5fe81bf6549bdaafd1898db3a5269"
    BASE_URL = "http://techchallenge.cimpress.com/"
    ENV = "trial"
    URL = '{0}/{1}/{2}/puzzle'.format(BASE_URL, API_KEY, ENV)
    FALSE = "false"
    TRUE = "true"
    DEBUG_VIZ = True

    def __init__(self, puzzle):
        self.puzzle = puzzle
        puzzle_width = puzzle["width"]
        puzzle_height = puzzle["height"]
        self.last_col_index = puzzle_width
        self.last_row_index = puzzle_height
        self.puzzle_id = puzzle["id"]
        self.grid = self.get_grid_from_puzzle(self, puzzle=puzzle, width=puzzle_width, height=puzzle_height)
        self.original_grid = copy(self.grid)
        self.grid_vis = zeros(shape=self.grid.shape)
        self.largest_squares = []
        self.recent_square = None
        self.current_max_size = 0

    def solve(self):
        found_grid = True

        while found_grid:
            found_grid = False
            test_size = 1
            for row in xrange(self.last_row_index):
                for col in xrange(self.last_col_index):
                    if self.grid[row, col]:
                        found_grid = True
                    else:
                        continue

                    while self.is_valid_square(col, row, test_size):
                        test_size += 1
                    valid_size = test_size - 1

                    if valid_size > self.current_max_size:
                        self.current_max_size = valid_size
                        self.recent_square = sq.Square(col, row, valid_size)

            # After a full grid sweep, check to see if any squares were found
            # If none were found, the partition has completed
            if self.recent_square is None or not found_grid:
                found_square = False
            else:
                self.save_square(self.recent_square)
                self.recent_square = None
                self.current_max_size = 0
        if self.DEBUG_VIZ:
            self.visualize_grids(self, self.original_grid, self.grid_vis)

        return self.largest_squares

    def save_square(self, square):
        start_col = square.X
        start_row = square.Y
        end_col = start_col + square.size - 1
        end_row = start_row + square.size - 1
        self.largest_squares.append(self.recent_square)
        square_num = len(self.largest_squares)
        for col in xrange(start_col, end_col):
            for row in xrange(start_row, end_row):
                self.grid[row, col] = False
                if self.DEBUG_VIZ:
                    self.grid_vis[row, col] = True


    @staticmethod
    def visualize_grids(self, grid, split_grid):
        base_plot = plt.imshow(grid)
        base_plot.set_interpolation('nearest')

        plt.colorbar()
        plt.show()

        end_plot = plt.imshow(split_grid)
        end_plot.set_interpolation('nearest')


        plt.colorbar()
        plt.show()

        difference = subtract(grid, split_grid)
        difference_plot = plt.imshow(grid)
        difference_plot.set_interpolation('nearest')

        plt.colorbar()
        plt.show()


    @staticmethod
    def get_grid_from_puzzle(self, puzzle, width, height):
        puzzle_grid = puzzle["puzzle"]
        return asarray(puzzle_grid, order='F')

    @staticmethod
    def get_grid_shape(self, puzzle_grid):
        puzzle_height = len(puzzle_grid)
        puzzle_width = 0
        if puzzle_height:
            first_row = puzzle_grid[0]
            puzzle_width = len(first_row)
        return puzzle_width, puzzle_height

    def is_valid_square(self, start_col, start_row, size):
        end_col = start_col + size - 1
        end_row = start_row + size - 1
        if end_row > self.last_row_index or end_col > self.last_col_index:
            return False
        for col in xrange(start_col, end_col):
            for row in xrange(start_row, end_row):
                if not self.grid[row, col]:
                    return False

        return True