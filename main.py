import sys

import PuzzleManager as Pm


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main():
    try:
        puzzle_manager = Pm.PuzzleManager()
        puzzle_manager.solve_puzzles()

    except Exception, err:
        print >> sys.stderr, err.message
        print >> sys.stderr, "Well, this is embarrassing."
        return 2


if __name__ == "__main__":
    sys.exit(main())