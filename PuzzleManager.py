

import json
import requests
import PuzzleSolver as ps


class PuzzleManager:
    API_KEY = "38c5fe81bf6549bdaafd1898db3a5269"
    BASE_URL = "http://techchallenge.cimpress.com/"
    ENV = "trial"
    URL = '{0}/{1}/{2}/puzzle'.format(BASE_URL, API_KEY, ENV)

    def __init__(self, puzzles_to_solve=1):
        self.puzzles_to_solve = puzzles_to_solve
        pass


    def solve_puzzles(self):
        puzzles_solved = 0
        while puzzles_solved < self.puzzles_to_solve:
            solution = self.get_and_solve_puzzle()
            self.submit_solution(solution)
            puzzles_solved += 1

    def get_and_solve_puzzle(self):
        puzzle = self.get_puzzle()
        puzzle_solver = ps.PuzzleSolver(puzzle=puzzle)
        return puzzle_solver.solve()


    # Retrieve a puzzle from the server. Returns JSON.
    def get_puzzle(self):
        return json.loads(requests.get(self.URL).text)

    def submit_solution(self,solution):
        pass

