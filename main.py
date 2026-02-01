from pyscript import document

class BitwiseSudokuSolver:
    def __init__(self, board):
        self.board = board
        self.row_bits = [0] * 9
        self.col_bits = [0] * 9
        self.box_bits = [0] * 9

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val != 0:
                    bit = 1 << (val - 1)
                    box_idx = (r // 3) * 3 + (c // 3)
                
                    if (self.row_bits[r] & bit) or (self.col_bits[c] & bit) or (self.box_bits[box_idx] & bit):
                        self.is_valid_initial = False
                        return
                    self.row_bits[r] |= bit
                    self.col_bits[c] |= bit
                    self.box_bits[box_idx] |= bit
        
        self.is_valid_initial = True
    
    def get_candidates_bits(self, r, c):
        box_idx = (r // 3) * 3 + (c // 3)
        used = self.row_bits[r] | self.col_bits[c] | self.box_bits[box_idx]
        return ~used & 0x1FF

    def solve(self):
        best_r, best_c = -1, -1
        min_candidates = 10
        best_candidates_bits = 0
        empty_found = False

        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    empty_found = True
                    candidates_bits = self.get_candidates_bits(r, c)
                    count = bin(candidates_bits).count('1')
                    if count == 0:
                        return False
                    
                    if count < min_candidates:
                        min_candidates = count
                        best_r, best_c = r, c
                        best_candidates_bits = candidates_bits
                        if count == 1:
                            break
                
            if min_candidates == 1:
                break

        if not empty_found:
            return True
        
        r, c = best_r, best_c
        box_idx = (r // 3) * 3 + (c // 3)
        temp_bits = best_candidates_bits
        while temp_bits > 0:
            bit = temp_bits & -temp_bits
            temp_bits ^= bit
            num = bit.bit_length()

            self.board[r][c] = sum
            self.row_bits[r] |= bit
            self.col_bits[c] |= bit
            self.box_bits[box_idx] |= bit

            if self.solve():
                return True
            
            self.board[r][c] = 0
            self.row_bits[r] ^= bit
            self.col_bits[c] ^= bit
            self.box_bits[box_idx] ^= bit

        return False

def get_board():
    board = []
    for r in range(9):
        row = []
        for c in range(9):
            index = r * 9 + c
            cell = document.querySelector(f"#cell-{index}")
            val = cell.value
            row.append(int(val) if val.isdigit() else 0)
        board.append(row)
    return board

def solve_sudoku(event):
    message_el = document.querySelector("#message")
    message_el.style.color = "var(--text-color)"
    message_el.innerText = "計算中"

    raw_board = get_board()

    solver = BitwiseSudokuSolver(raw_board)

    if not solver.is_valid_initial:
        message_el.innerText = "エラー：同じ列・行・ブロック内で数字が重複しています"
        message_el.style.color = "#d63384"
        return

    message_el.innerText = "計算中"
    
    if solver.solve():
        initial_indices = []
        for r in range(9):
            for c in range(9):
                index = r * 9 + c
                cell = document.querySelector(f"#cell-{index}")
                if cell.value == "":
                    cell.value = solver.board[r][c]
                    cell.classList.add("solved-number")
                
        message_el.innerText = "解けました"
    else:
        message_el.innerText = "解けません"