


class Piece(object):

    def __init__(self, value, position, white=True):
        self.value = value
        self.position = position
        self.white = white

    def get_value(self):
        return self.value

    def get_position(self):
        return self.position

class Pawn(Piece):

    def __init__(self, position, white=True):
        value = 1
        if not white:
            value = -1
        super(Piece, value, position, white)

    def is_putting_king_in_check(self, king_position):
        row, col = self.position
        if self.white:
            return king_position == (row-1, col-1) or king_position == (row-1, col+1)
        else:
            return king_position == (row+1, col-1) or king_position == (row+1, col+1)

class Bishop(Piece):

    def __init__(self, position, white=True):
        value = 2
        if not white:
            value = -2
        super(Piece, value, position, white)

class Knight(Piece):

    def __init__(self, position, white=True):
        value = 3
        if not white:
            value = -3
        super(Piece, value, position, white)

class Rook(Piece):

    def __init__(self, position, white=True):
        value = 4
        if not white:
            value = -4
        super(Piece, value, position, white)

class Queen(Piece):

    def __init__(self, position, white=True):
        value = 5
        if not white:
            value = -5
        super(Piece, value, position, white)

class King(Piece):

    def __init__(self, position, white=True):
        value = 6
        if not white:
            value = -6
        super(Piece, value, position, white)