""" Script to solve "One Tough Puzzle" a.k.a. "Impuzzable"
as seen at http://nrich.maths.org/1388

Author: Sam Thomson
Date: 1/1/2012
"""
HEART, CLUB, DAIMOND, SPADE = "hcds"
NUM_ROWS = 3
NUM_COLS = 3
NUM_PIECES = NUM_ROWS * NUM_COLS
PIECE_WIDTH = 16 # in characters, for printing
# enumeration of sides of all pieces, clockwise from top. pieces were
# arranged so that top and right are out, bottom and left are in.
PIECE_SIDES = (
    (CLUB, HEART, DAIMOND, CLUB),
    (HEART, DAIMOND, DAIMOND, HEART),
    (DAIMOND, CLUB, CLUB, DAIMOND),
    (SPADE, DAIMOND, SPADE, HEART),
    (HEART, SPADE, SPADE, CLUB),
    (CLUB, HEART, SPADE, HEART),
    (HEART, DAIMOND, CLUB, CLUB),
    (SPADE, DAIMOND, HEART, DAIMOND),
    (SPADE, SPADE, HEART, CLUB)
)

def row_repr(row):
    """ Pretty print a row of pieces """
    result = []
    for piece in row:
        result.extend([repr(piece.top).center(PIECE_WIDTH), ' | '])
    result.append('\n')
    for piece in row:
        result.extend([repr(piece.left), '      ', str(piece.right), ' | '])
    result.append('\n')
    for piece in row:
        result.extend([repr(piece.bottom).center(PIECE_WIDTH), ' | '])
    result.append('\n')
    return ''.join(result)


def reshape(pieces, width=NUM_COLS, height=NUM_ROWS):
    """ Reshape a list into a height-by-width matrix (list-of-lists).
    Fill in across from left to right, then down.
    """
    return [pieces[i:i+width] for i in range(0, len(pieces), width)]
    

class Side(object):
    """ A side of one piece. Each side has a shape (one of HEART, CLUB,
    DAIMOND, SPADE), and an extrude (True or False) which represents whether
    or not it's sticking in or out.
    """
    def __init__(self, shape, extrude):
        self.shape = shape
        self.extrude = extrude
    
    def __repr__(self):
        return "%s %s" % (self.shape, "out" if self.extrude else "in ")

    def fits_with(self, other):
        # to match, need same shape, and one in, one out
        return self.shape == other.shape and self.extrude != other.extrude


class Piece(object):
    """ One piece of the puzzle. Each piece has four sides - two in and two
    out.
    """
    def __init__(self, sides):
        """ Construct a Piece given a list of four Sides """
        self.sides = sides
        self.top, self.right, self.bottom, self.left = self.sides
    
    def __repr__(self):
        """ Pretty print the piece """
        return row_repr((self,))
    
    def spun(self, rotation):
        """ A new Piece, gotten by rotating self 'rotation' quarter-turns
        counterclockwise """
        return Piece((self.sides * 2)[rotation:rotation+4])

    def fits_right(self, other):
        return self.right.fits_with(other.left)

    def fits_bottom(self, other):
        return self.bottom.fits_with(other.top)


# The starting pieces
PIECES = [Piece((Side(top, True), Side(right, True),
                 Side(bottom, False), Side(left, False)))
          for top, right, bottom, left in PIECE_SIDES]


class PartialSolution(object):
    """ A partial solution, represented as a possibly incomplete 3x3 grid of
    Pieces
    """
    def __init__(self, pieces):
        """ Construct the grid from a list of pieces """
        self.grid = pieces
    
    def __repr__(self):
        """ Pretty print the solution """
        result = []
        for row in self.grid:
            result.append(row_repr(row))
            result.extend(['-'] * (PIECE_WIDTH + 3) * len(row))
            result.append('\n')
        return ''.join(result)

    def check_rows(self):
        """ Check that all pieces fit together in each row """
        for row in self.grid:
            for left, right in zip(row, row[1:]):
                if not left.fits_right(right):
                    return False
        return True

    def check_cols(self):
        """ Check that all pieces fit together in each column """
        # transpose grid
        for col in zip(*self.grid):
            for top, bottom in zip(col, col[1:]):
                if not top.fits_bottom(bottom):
                    return False
        return True
    
    def check(self):
        """ Check that all pieces fit together """
        return self.check_rows() and self.check_cols()


class Solver(object):
    def solve(self, indexes=(), rotations=()):
        """ Find a solution by depth-first search """
        pieces = [PIECES[i].spun(rot)
                  for i, rot in zip(indexes, rotations)]
        soln = PartialSolution(reshape(pieces))
        if not soln.check():
            # partial solution is impossible. give up on this branch.
            return None
        if len(indexes) == NUM_PIECES:
            # solution is possible and complete. we're done!
            return soln
        # solution is possible so far, but incomplete
        for idx in set(range(NUM_PIECES)) - set(indexes):
            # try the next piece
            for rot in range(4):
                # try the next rotation
                soln = self.solve(indexes + (idx,), rotations + (rot,))
                if soln:
                    return soln


if __name__ == "__main__":
    solver = Solver()
    soln = solver.solve()
    print soln
