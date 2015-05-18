from numpy import asarray, copy, zeros
import matplotlib.pyplot as plt

import Square as Sq
import PuzzleSolution as Pz


class PuzzleSolver(object):
    DEBUG_VIZ = False
    ROW_MAJOR = True

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.puzzle_id = puzzle["id"]
        self.grid = self.get_grid_from_puzzle(puzzle=puzzle)
        self.last_row_index = self.grid.shape[0] - 1
        self.last_col_index = self.grid.shape[1] - 1
        self.original_grid = copy(self.grid)
        self.grid_vis = zeros(shape=self.grid.shape)
        self.solution = Pz.PuzzleSolution(self.puzzle_id)

    def top_left_solve(self):
        squares_remain = True
        previous_max_size = None

        while squares_remain:
            found_block = False
            squares_remain = False
            valid_size = 0
            test_size = 1
            start_col = 0
            start_row = 0
            current_max_size = 0

            for row in range(0, self.last_row_index + 1):
                for col in range(0, self.last_col_index + 1):
                    if self.grid[row, col]:
                        squares_remain = True
                        while self.is_valid_square(start_col = col, start_row = row, size = test_size):
                            test_size += 1
                        valid_size = test_size - 1
                        if valid_size > current_max_size:
                            current_max_size = valid_size
                            start_col = col
                            start_row = row
                            found_block = True
                            if previous_max_size is not None and valid_size == previous_max_size:
                                break
                    if col + valid_size > self.last_col_index:
                        break
                if previous_max_size is not None and valid_size == previous_max_size:
                            break
                if row + valid_size > self.last_row_index:
                    break

            # After a full grid sweep, check to see if any squares were found
            # If none were found, the partition has completed
            if found_block:
                self.save_square(start_row=start_row, start_col=start_col, size=current_max_size)
                previous_max_size = current_max_size

        if self.DEBUG_VIZ:
            self.visualize_grids(self.original_grid, self.grid_vis)

    def is_valid_square(self, start_col, start_row, size):
        end_col = start_col + size - 1
        end_row = start_row + size - 1

        if end_row > self.last_row_index or end_col > self.last_col_index:
            return False
        for row in xrange(start_row, end_row + 1):
            for col in xrange(start_col, end_col + 1):
                if not self.grid[row, col]:
                    return False

        return True

    def save_square(self, start_col, start_row, size):
        end_col = start_col + size - 1
        end_row = start_row + size - 1
        square_num = len(self.solution.get_squares())
        self.solution.add_square(Sq.Square(row=start_row, col=start_col, row_major=self.ROW_MAJOR, size=size))
        for col in xrange(start_col, end_col + 1):
            for row in xrange(start_row, end_row + 1):
                self.grid[row, col] = False
                if self.DEBUG_VIZ:
                    self.grid_vis[row, col] = square_num

    def get_solution(self):
        return self.solution

    @staticmethod
    def visualize_grids(grid, split_grid):
        base_plot = plt.imshow(grid)
        base_plot.set_interpolation('nearest')

        plt.colorbar()
        plt.show()

        end_plot = plt.imshow(split_grid)
        end_plot.set_interpolation('nearest')

        plt.colorbar()
        plt.show()

    @staticmethod
    def get_grid_from_puzzle(puzzle):
        puzzle_grid = puzzle["puzzle"]
        array = asarray(puzzle_grid, order='F')
        return array