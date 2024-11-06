import numpy as np 
import random 
import time


boardtypes = [
    [
        "############################",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#o####.#####.##.#####.####o#",
        "#.####.#####.##.#####.####.#",
        "#..........................#",
        "#.####.##.########.##.####.#",
        "#.####.##.########.##.####.#",
        "#......##....##....##......#",
        "######.##### ## #####.######",
        "######.##### ## #####.######",
        "######.##          ##.######",
        "######.## ###  ### ##.######",
        "######.## #  b   # ##.######",
        " p     ##   c  d   ##       ",
        "######.## #   a  # ##.######",
        "######.## ###  ### ##.######",
        "######.##          ##.######",
        "######.## ######## ##.######",
        "######.## ######## ##.######",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#.####.#####.##.#####.####.#",
        "#o..##................##..o#",
        "###.##.##.########.##.##.###",
        "###.##.##.########.##.##.###",
        "#......##....##....##......#",
        "#.##########.##.##########.#",
        "#.##########.##.##########.#",
        "#..........................#",
        "############################"]
]

class Player:
    def __init__(self, player_pos):
        self.points = 0
        self.x, self.y = player_pos 
        
    
    def __getitem__(self, index):
        return self.player_pos[index]

    def is_dead(self, board, x, y):
        return board[x][y] in "abcd"  

    def move(self, board):
        moves = [
            ("up", self.x - 1, self.y), 
            ("down", self.x + 1, self.y), 
            ("left", self.x, self.y - 1), 
            ("right", self.x, self.y + 1)
        ]

        valid_moves = [
            (direction, new_x, new_y) 
            for direction, new_x, new_y in moves 
            if board[new_x][new_y] != "#" and board[new_x][new_y] not in "abcd"
        ]

        if not valid_moves:
            return 'death'
        
        food_moves = [(d, nx, ny) for d, nx, ny in valid_moves if board[nx][ny] == '.']
        direction, new_x, new_y = food_moves[0] if food_moves else valid_moves[0]
        board[self.x][self.y] = ' '
        if board[new_x][new_y] == '.':
            self.points += 1
        self.x, self.y = new_x, new_y
        board[self.x][self.y] = 'p'

class Ghost:
    
    def __init__(self,ghost_pos,ghost_id):
        self.x, self.y = ghost_pos
        self.id = ghost_id
        self.last_block = ' '

    def move(self,board,move):
        
        move = random.choice(["up", "down", "left", "right"])
        moves = {"up": (self.x - 1, self.y), 
                 "down": (self.x + 1, self.y), 
                 "left": (self.x, self.y - 1), 
                 "right": (self.x, self.y + 1)}
        new_x, new_y = moves[move]

        if board[new_x][new_y] in "#abcd":
            return 

        if board[new_x][new_y] == 'p':
            return 'death'

        board[self.x][self.y] = self.last_block
        self.last_block = board[new_x][new_y]
        self.x, self.y = new_x, new_y
        board[self.x][self.y] = self.id
class Board:
    def __init__(self):
        self.board = np.array([list(row) for row in boardtypes[0]])
        self.row, self.col = self.board.shape

    def food_left(self):
        return np.count_nonzero(self.board == '.')
       
    def display(self):
        for row in self.board:
            print(' '.join(row))

    def __getitem__(self, index):
        return self.board[index]
    
    def __setitem__(self,index,value):
        self.board[index] = value

    def get_positions(self):
        player_pos = ghost1_pos = ghost2_pos = ghost3_pos = ghost4_pos = None
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i, j] == 'p':
                    player_pos = [i, j]
                elif self.board[i, j] == 'a':
                    ghost1_pos = [i, j]
                elif self.board[i, j] == 'b':
                    ghost2_pos = [i, j]
                elif self.board[i, j] == 'c':
                    ghost3_pos = [i, j]
                elif self.board[i, j] == 'd':  
                    ghost4_pos = [i, j]
        return player_pos, ghost1_pos, ghost2_pos, ghost3_pos, ghost4_pos           
   

def get_moves(board, points):
    try:
        ghost_moves = {'a': [0, 0, 0, 0], 'b': [0, 0, 0, 0], 'c': [0, 0, 0, 0], 'd': [0, 0, 0, 0]} 
        player_moves = [0, 0, 0, 0]  
        player_pos = None
        ghost_positions = {'a': None, 'b': None, 'c': None, 'd': None}

        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c] == 'P':
                    player_pos = (r, c)
                elif board[r][c] in ghost_positions:
                    ghost_positions[board[r][c]] = (r, c)
        if player_pos is None:
            raise ValueError("Player position not found on the board.")
        for ghost, pos in ghost_positions.items():
            if pos:
                ghost_row, ghost_col = pos
                if ghost_row < player_pos[0]:
                    ghost_moves[1] = 1
                elif ghost_row > player_pos[0]:
                    ghost_moves[0] = 1
                elif ghost_col < player_pos[1]:  
                    ghost_moves[3] = 1 
                elif ghost_col > player_pos[1]:
                    ghost_moves[2] = 1  
        player_moves[0] = 1
        return ghost_moves, player_moves
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
def game_loop():
    board = Board()
    player = Player(board.get_positions()[0])
    ghosts = [
        Ghost(board.get_positions()[1], 'a'),
        Ghost(board.get_positions()[2], 'b'),
        Ghost(board.get_positions()[3], 'c'),
        Ghost(board.get_positions()[4], 'd')
    ]
    while True:
        board.display()
        result = player.move(board.board)

        if result == 'death' or board[player.x][player.y] in "abcd":
            print("You were caught by a ghost! Game Over!")
            return 
        print(f"Points: {player.points}")
        if player.points >= 2:  
            print("All food eaten! You win!")
            return
        time.sleep(1)

        for ghost in ghosts:
            result = ghost.move(board.board)
            if result == 'death' or board[player.x][player.y] in "abcd":
                print("You were caught by a ghost! Game Over!")
                return

game_loop()