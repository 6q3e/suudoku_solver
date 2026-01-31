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

def get_possible_values(board, r, c):
    used = set()

    for i in range(9):
        if board[r][i] != 0:
            used.add(board[r][i])

    for i in range(9):
        if board[i][c] != 0:
            used.add(board[i][c])
    
    start_r, start_c = 3 * (r // 3), 3 * (c // 3)
    for i in range(3):
        for j in range(3):
            val = board[start_r + i][start_c + j]
            if val != 0:
                used.add(val)
    
    return [num for num in range(1, 10) if num not in used]

def find_best_empty_cell(board):
    min_candidates_len = 10
    best_cell = None
    best_candidates = []

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                candidates = get_possible_values(board, r, c)
                num_candidates = len(candidates)

                if num_candidates == 0:
                    return (r, c), []
                
                if num_candidates < min_candidates_len:
                    min_candidates_len = num_candidates
                    best_cell = (r,c)
                    best_candidates = candidates

                    if min_candidates_len == 1:
                        return best_cell, best_candidates
    return best_cell, best_candidates

def check_initial_validity(board):
    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != 0:
                board[r][c] = 0
                candidates = get_possible_values(board, r, c)
                if num not in candidates:
                    board[r][c] = num
                    return False
                board[r][c] = num
    return True

def solve(board):
    cell, candidates = find_best_empty_cell(board)

    if cell is None:
        return True
    
    r,c = cell

    for num in candidates:
        board[r][c] = num

        if solve(board):
            return True
        
        board[r][c] = 0
    
    return False

def solve_sudoku(event):
    message_el = document.querySelector("#message")
    message_el.style.color = "var(--text-color)"
    message_el.innerText = "チェック中"

    board = get_board()

    if not check_initial_validity(board):
        message_el.innerText = "エラー：同じ列・行・ブロック内で数字が重複しています"
        message_el.style.color = "#d63384"
        return

    message_el.innerText = "計算中"

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