def draw_board(matrix):
    # Initialize board (This string will be the one returned)
    board = ""
    # Iterate over all slots
    for row_index, row in enumerate(matrix):
        # Add a row
        for slot_index, slot in enumerate(row):
            # Add X's and O's according to matrix
            board += (" " * 5 if slot == 0 else
                      ("  x  " if slot == 1 else
                       "  o  "))
            # Add veritcal line, except after the last slot (slot 2)
            if slot_index < 2:
                board += "|"
        # Add line, except under last row (row 2)
        if row_index < 2:
            board += f"\n{'-' * 17}\n"
    return board


def make_move(matrix, piece, x_pos, y_pos):
    # In matrices the y-axis goes down, so we subtract it from the height
    # Subtract 1 from x to start from 1 and not 0
    if matrix[3 - y_pos][x_pos - 1] == 0:
        matrix[3 - y_pos][x_pos - 1] = piece
    return matrix

def has_won(matrix):
    # Check the rows and columns
    # Matrix is a list of all rows, list(map(list, zip(*matrix))) is a list of all columns
    # We add them to first check rows, then check columns, in the same loop
    for row_or_column in matrix + list(map(list, zip(*matrix))):
        if row_or_column == [1, 1, 1]:
            return 1
        if row_or_column == [2, 2, 2]:
            return 2
    # Check the diagonals
    if ((matrix[0][0] == 1 and matrix[2][2] == 1) or \
    (matrix[0][2] == 1 and matrix[2][0] == 1)) \
      and matrix[1][1] == 1:
        return 1
    if ((matrix[0][0] == 2 and matrix[2][2] == 2) or \
    (matrix[0][2] == 2 and matrix[2][0] == 2)) \
      and matrix[1][1] == 2:
        return 2
    # If nobody won
    return 0

def is_full(matrix):
    return not any((0 in i) for i in matrix)

if __name__ == "__main__":

    round_count = 0
    play = True
    while play:
        p1_name = input("Player 1, what is your name?")
        p2_name = input("Player 2, what is your name?")


