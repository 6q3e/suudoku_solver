from pyscript import document

def get_board():
    board = []
    for r in range(9):
        row = []
        for c in range(9):
            index = r * 9 + c
            cell = document.querySelector(f"#cell-{index}")
            value = cell.value
            if value == "":
                row.append(0)
            else:
                row.append(int(value))
        board.append(row)
    return board

def is_valid(board, r, c, num):
    for i in range(9):
        if board[r][i] == num:
            return False
    for i in range(9):
        if board[i][c] == num:
            return False
        
    start_r, start_c = 3 * (r // 3), 3 * (c // 3)
    for i in range(3):
        for j in range(3):
            if board[start_r + i][start_c + j] == num:
                return False
    return True

def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for num in range(1, 10):
                    if is_valid(board, r, c, num):
                        board[r][c] = num
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True

def solve_sudoku(event):
    message_el = document.querySelector("#message")
    message_el.innerText = "計算中"

    board = get_board()

    initial_indices = []
    for r in range(9):
        for c in range(9): 
            if board[r][c] != 0:
                initial_indices.append(r * 9 + c)
    
    if solve(board):
        for r in range(9):
            for c in range(9):
                index = r * 9 + c
                cell = document.querySelector(f"#cell-{index}")
                cell.value = board[r][c]

                if index not in initial_indices:
                    cell.classList.add("solved-number")
                
        message_el.innerText = "解けました"
    else:
        message_el.innerText = "解けません"