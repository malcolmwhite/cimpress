import json
from pprint import pprint

import requests

import PuzzleSolver as Ps


class PuzzleManager:
    API_KEY = "38c5fe81bf6549bdaafd1898db3a5269"
    BASE_URL = "http://techchallenge.cimpress.com"
    ENV = "trial"
    GET_URL = '{0}/{1}/{2}/puzzle'.format(BASE_URL, API_KEY, ENV)
    POST_URL = '{0}/{1}/{2}/solution'.format(BASE_URL, API_KEY, ENV)

    def __init__(self, puzzles_to_solve=1):
        self.puzzles_to_solve = puzzles_to_solve
        pass

    def solve_puzzles(self):
        puzzle = self.get_puzzle()
        puzzle_solver = Ps.PuzzleSolver(puzzle=puzzle)
        puzzle_solver.top_left_solve()
        top_left_solution = puzzle_solver.get_solution()
        self.submit_solution(top_left_solution)

    # Retrieve a puzzle from the server. Returns JSON.
    def get_puzzle(self):
        return json.loads(requests.get(self.GET_URL).text)

    def submit_solution(self, solution):
        squares = solution.get_squares()
        data = {'id': solution.id, 'squares': squares}

        json_result = requests.post(self.POST_URL, data=json.dumps(data)).text
        response = json.loads(json_result)
        pprint(response)


