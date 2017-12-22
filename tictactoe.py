def getboard(matrix):
    board = ""
    for row_index, row in enumerate(matrix):

        for item_index, item in enumerate(row):
            board += (" " * 5 if item == 0 else 
                    ("  O  " if item == 1 else 
                    "  X  "))
            if item_index < (len(row) - 1):
                board += "|"

        if row_index < (len(matrix) - 1):
            board += f"\n{'-' * 17}\n"

    return board

if __name__ == "__main__":
    b = getboard([
        [0, 1, 0],
        [2, 2, 1],
        [1, 0, 1]])
    print(b)          
