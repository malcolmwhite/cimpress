from numpy import subtract, asarray, copy, zeros
import Square as sq
import matplotlib.pyplot as plt
import PuzzleSolution as pz

class PuzzleSolver(object):
    API_KEY = "38c5fe81bf6549bdaafd1898db3a5269"
    BASE_URL = "http://techchallenge.cimpress.com/"
    ENV = "trial"
    URL = '{0}/{1}/{2}/puzzle'.format(BASE_URL, API_KEY, ENV)
    FALSE = "false"
    TRUE = "true"
    DEBUG_VIZ = True
    ROW_MAJOR = True

    def __init__(self, puzzle):
        self.puzzle = puzzle
        puzzle_width = puzzle["width"]
        puzzle_height = puzzle["height"]
        self.puzzle_id = puzzle["id"]
        self.grid = self.get_grid_from_puzzle(self, puzzle=puzzle, width=puzzle_width, height=puzzle_height)
        self.last_row_index = self.grid.shape[0] - 1
        self.last_col_index = self.grid.shape[1] - 1
        self.original_grid = copy(self.grid)
        self.grid_vis = zeros(shape=self.grid.shape)
        self.recent_square = None
        self.current_max_size = 0
        self.solution = pz.PuzzleSolution(self.puzzle_id)

    def solve(self):
        squares_remain = True

        num_sweeps = 0
        max_sweeps = self.last_col_index * self.last_row_index
        while squares_remain:
            squares_remain = False
            valid_size = 0
            print "num, max, valid, current max: ",num_sweeps, max_sweeps, valid_size, self.current_max_size
            num_sweeps += 1
            found_grid = False
            for row in range(0, self.last_row_index + 1):
                for col in range(0, self.last_col_index + 1):
                    if self.grid[row, col]:
                        squares_remain = True
                        # print "scanning at ", row, col
                        test_size = 1
                        test_square = sq.Square(col=col, row=row, size=test_size, row_major=self.ROW_MAJOR)
                        while self.is_valid_square(test_square):
                            test_size += 1
                            test_square = sq.Square(col=col, row=row, size=test_size, row_major=self.ROW_MAJOR)

                        valid_size = test_size - 1

                        if valid_size > self.current_max_size:
                            self.current_max_size = valid_size
                            self.recent_square = sq.Square(col=col, row=row, size=valid_size, row_major=self.ROW_MAJOR)
                    if col + valid_size > self.last_col_index:
                        break
                if row + valid_size > self.last_row_index:
                    break

            # After a full grid sweep, check to see if any squares were found
            # If none were found, the partition has completed
            if self.recent_square is not None:
                self.save_square(self.recent_square)


        if self.DEBUG_VIZ:
            self.visualize_grids(self, self.original_grid, self.grid_vis)

    def dummy_solve(self):
        for row in xrange(0, self.last_row_index):
            for col in xrange(0, self.last_col_index):
                if self.puzzle['puzzle'][row][col]:
                    self.solution.add_square(sq.Square(col=col, row=row, size=1, row_major=self.ROW_MAJOR))

    def get_solution(self):
        return self.solution

    def save_square(self, square):
        start_col = square.get_col_start(self.ROW_MAJOR)
        start_row = square.get_row_start(self.ROW_MAJOR)
        end_col = square.get_col_end(self.ROW_MAJOR)
        end_row = square.get_row_end(self.ROW_MAJOR)
        square_num = len(self.solution.get_squares())
        self.solution.add_square(square)
        self.recent_square = None
        self.current_max_size = 0
        print "saving", start_row, start_col, end_row, end_col
        for col in xrange(start_col, end_col + 1):
            for row in xrange(start_row, end_row + 1):
                self.grid[row, col] = False
                if self.DEBUG_VIZ:
                    self.grid_vis[row, col] = square_num


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
        array = asarray(puzzle_grid, order='F')
        return array


    def is_valid_square(self, square):
        start_row = square.get_row_start(self.ROW_MAJOR)
        end_row = square.get_row_end(self.ROW_MAJOR)
        start_col = square.get_col_start(self.ROW_MAJOR)
        end_col = square.get_col_end(self.ROW_MAJOR)

        if end_row > self.last_row_index or end_col > self.last_col_index:
            return False
        for row in xrange(start_row, end_row + 1):
            for col in xrange(start_col, end_col + 1):
                if not self.grid[row, col]:
                    return False

        return True