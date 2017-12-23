def get_board(matrix):
    # Initialize board (This string will be the one returned)
    board = ""
    # Iterate over all slots
    for row_index, row in enumerate(matrix):
        # Add a row
        for slot_index, slot in enumerate(row):
            # Add X's and O's aaccording to matrix
            board += (" " * 5 if slot == 0 else
                      ("  x  " if slot == 1 else
                       "  o  "))
            # Add veritcal line, except after the last slot (slot 3)
            if slot_index < 2:
                board += "|"
        # Add line, except under last row (row 3)
        if row_index < 2:
            board += f"\n{'-' * 17}\n"
    return board


def make_move(matrix, piece, x, y):
    # In matrices the y-axis goes down, so we subtract it from the height
    # Subtract 1 from x to start from 1 and not 0
    if matrix[3 - y][x - 1] == 0:
        matrix[3 - y][x - 1] = piece
    return matrix

# def has_won(matrix, piece)

if __name__ == "__main__":
    matrix = [[0, 0, 0] for _ in range(3)]
    print(get_board(matrix), matrix)
    matrix = make_move(matrix, 2, 3, 3)
    print(get_board(matrix))
    print(matrix)
