from numpy import asarray

import Square as Sq
import PuzzleSolution as Pz


class PuzzleSolver(object):
    DEBUG_VIZ = True

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.puzzle_id = puzzle["id"]
        self.grid = self.get_grid_from_puzzle(puzzle=puzzle)
        self.grid_rows = self.grid.shape[0]
        self.grid_columns = self.grid.shape[1]
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

            for row in range(self.grid_rows):
                for col in range(self.grid_columns):
                    if self.grid[row, col]:
                        squares_remain = True
                        while self.is_valid_square(start_col=col, start_row=row, size=test_size):
                            test_size += 1
                        valid_size = test_size - 1
                        if valid_size > current_max_size:
                            current_max_size = valid_size
                            start_col = col
                            start_row = row
                            found_block = True
                            if previous_max_size is not None and valid_size == previous_max_size:
                                break
                    if col + valid_size > self.grid_columns:
                        break
                if previous_max_size is not None and valid_size == previous_max_size:
                            break
                elif row + valid_size > self.grid_rows:
                    break

            # After a full grid sweep, check to see if any squares were found
            # If none were found, the partition has completed
            if found_block:
                self.save_square(start_row=start_row, start_col=start_col, size=current_max_size)
                previous_max_size = current_max_size


    def is_valid_square(self, start_col, start_row, size):
        end_col = start_col + size
        end_row = start_row + size

        if end_row > self.grid_rows or end_col > self.grid_columns:
            return False
        for row in xrange(start_row, end_row):
            for col in xrange(start_col, end_col):
                if not self.grid[row, col]:
                    return False

        return True

    def save_square(self, start_col, start_row, size):
        end_col = start_col + size
        end_row = start_row + size
        self.solution.add_square(Sq.Square(row=start_row, col=start_col, size=size))
        for row in xrange(start_row, end_row):
            for col in xrange(start_col, end_col):
                self.grid[row, col] = False

    @staticmethod
    def get_grid_from_puzzle(puzzle):
        puzzle_grid = puzzle["puzzle"]
        return asarray(puzzle_grid)

    def get_solution(self):
        return self.solution
