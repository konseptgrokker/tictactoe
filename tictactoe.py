def getboard(matrix):
    # Initialize board (This string will be the one returned)
    board = ""
    # Iterate over all slots
    for row_index, row in enumerate(matrix):
        # Add a row
        for slot_index, slot in enumerate(row):
            # Add X or O according to matrix
            board += (" " * 5 if slot == 0 else
                      ("  O  " if slot == 1 else
                       "  X  "))
            # Add veritcal line, except after the last slot (slot 3)
            if slot_index < 2:
                board += "|"

        # Add line, except under last row (row 3)
        if row_index < 2:
            board += f"\n{'-' * 17}\n"

    return board

if __name__ == "__main__":
    b = getboard([
        [0, 1, 0],
        [2, 2, 1],
        [1, 0, 1]])
    print(b)
