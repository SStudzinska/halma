import random
import time
import math

WHITE_START_POS = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), 
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), 
            (0, 3), (1, 3), (2, 3), (0, 4), (1, 4)]
BLACK_START_POS = [(11, 15), (12, 15), (13, 15), (14, 15), (15, 15),
            (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), 
            (12, 13), (13, 13), (14, 13), (15, 13), 
            (13, 12), (14, 12), (15, 12), 
            (14, 11), (15, 11)]
TOTAL_PAWNS = 19

class Halma:
    def __init__(self):
        self.board = [[0 for _ in range(16)] for _ in range(16)]  # Inicjalizacja planszy 16x16
        # Ustawienie pionków gracza 1
        for i in range(5):
            self.board[i][0] = 1
            self.board[i][1] = 1
            if (i-1 >= 0):
                self.board[i-1][2] = 1
            if (i-2 >= 0):
                self.board[i-2][3] = 1
            if (i-3 >= 0):
                self.board[i-3][4] = 1
        
        # Ustawienie pionków gracza 2
        for i in range(11, 16):
            self.board[i][15] = 2
            self.board[i][14] = 2
            if (i+1 < 16):
                self.board[i+1][13] = 2
            if (i+2 < 16):
                self.board[i+2][12] = 2
            if (i+3 < 16):
                self.board[i+3][11] = 2

        self.current_player = 1 
        self.rounds = 0
        self.winner = None
    
    def print_board(self):
    # Wypisanie numerów kolumn
        print("  ", end="")
        for i in range(16):
            print(f"|{i:2}", end=" ")
        print()
    
        # Wypisanie separatora
        print("  " + ("----" * 16))
    
        # Wypisanie planszy z numerami wierszy i zawartością pól
        for i in range(16):
            print(f"{i:2}|", end="")
            for j in range(16):
                print(f" {self.board[i][j]} ", end=" ")
            print()

    def is_valid_move(self, start, end):
        moves, num = self.generate_possible_moves()
        if ((start, end) in moves):
            return True
        else:
            return False

    def is_valid_in_camp_move(self, end):
        if self.current_player == 1:
            if(end in BLACK_START_POS):
                return True 
        else:
            if(end in WHITE_START_POS):
                return True

    def check_winner(self): 
        player1_in_player2_camp = 0 
        player2_in_player1_camp = 0
        winner = None
        
        for i, j in BLACK_START_POS:  
            if self.board[i][j] == 1:
                player1_in_player2_camp += 1
                winner = True
            elif self.board[i][j] == 0:  
                winner = False
                break

        if player1_in_player2_camp > 0 and winner:
            self.winner = 1
            return winner
        
        for i, j in WHITE_START_POS:  
            if self.board[i][j] == 2:
                player2_in_player1_camp += 1
                winner = True
            elif self.board[i][j] == 0: 
                winner = False
                break
            
        if player2_in_player1_camp > 0 and winner:
            self.winner = 2
            return winner
        return winner



    def generate_possible_moves(self):
        possible_moves = []
        for i in range(16):
            for j in range(16):
                if self.board[i][j] == self.current_player:
                    if self.is_in_opposing_camp(i, j, self.current_player):
                        self.check_adjacent_moves_in_camp(possible_moves, i, j)
                        self.check_jump_moves_in_camp(possible_moves, i, j)
                    else:
                        self.check_adjacent_moves(possible_moves, i, j)
                        self.check_jump_moves(possible_moves, i, j)
        moves_set = set(possible_moves)
        return list(moves_set), len(possible_moves)

    def check_adjacent_moves(self, possible_moves, i, j):
        if self.board[i][j] == self.current_player:
            if not self.is_in_opposing_camp(i, j, self.current_player):
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (dx, dy) != (0, 0):
                            x2, y2 = i + dx, j + dy
                            if 0 <= x2 < 16 and 0 <= y2 < 16 and self.board[x2][y2] == 0:
                                possible_moves.append(((i, j), (x2, y2)))

    def check_jump_moves(self, possible_moves, i, j):
        if self.board[i][j] == self.current_player:
            if not self.is_in_opposing_camp(i, j, self.current_player):
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (dx, dy) != (0, 0):
                            x2, y2 = i + dx, j + dy
                            jump_x, jump_y = i + 2*dx, j + 2*dy
                            if 0 <= x2 < 16 and 0 <= y2 < 16 and 0 <= jump_x < 16 and 0 <= jump_y < 16:
                                if self.board[x2][y2] != 0 and self.board[jump_x][jump_y] == 0:
                                    possible_moves.append(((i, j), (jump_x, jump_y)))
                                    self.check_additional_jumps(possible_moves,i, j, jump_x, jump_y)

    def check_additional_jumps(self, possible_moves, from_x, from_y, prev_x, prev_y):
        visited = []
        jump_x = prev_x
        jump_y = prev_y
        previous_position = (jump_x, jump_y)  # Zapamiętujemy poprzednią pozycję

        while True:
            found_jump = False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx, dy) != (0, 0):
                        x2, y2 = jump_x + dx, jump_y + dy
                        jump_x2, jump_y2 = jump_x + 2*dx, jump_y + 2*dy
                        if 0 <= x2 < 16 and 0 <= y2 < 16 and 0 <= jump_x2 < 16 and 0 <= jump_y2 < 16:
                            if self.board[x2][y2] != 0 and self.board[jump_x2][jump_y2] == 0:
                                if (jump_x2, jump_y2) != previous_position and (jump_x2, jump_y2) not in visited:  # Sprawdzamy, czy to nie jest powrót do poprzedniej pozycji i czy nie zostało już odwiedzone
                                    possible_moves.append(((from_x, from_y),(jump_x2, jump_y2)))
                                    jump_x, jump_y = jump_x2, jump_y2
                                    previous_position = (jump_x, jump_y)  # Aktualizujemy poprzednią pozycję
                                    visited.append((jump_x2, jump_y2))  # Dodajemy bieżącą pozycję do odwiedzonych
                                    found_jump = True
                                    break
            if not found_jump:
                break

    
    def check_adjacent_moves_in_camp(self, possible_moves, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) != (0, 0):
                    x2, y2 = x + dx, y + dy
                    if self.is_valid_in_camp_move((x2, y2)) and self.board[x2][y2] == 0:
                        possible_moves.append(((x, y), (x2, y2)))

    def check_jump_moves_in_camp(self, possible_moves, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) != (0, 0):
                    x2, y2 = x + dx, y + dy
                    jump_x, jump_y = x + 2*dx, y + 2*dy
                    if self.is_valid_in_camp_move((x2, y2)) and self.is_valid_in_camp_move((jump_x, jump_y)):
                        if self.board[x2][y2] != 0 and self.board[jump_x][jump_y] == 0:
                            possible_moves.append(((x, y), (jump_x, jump_y)))
                            #add additional jumps in camp


    def is_in_opposing_camp(self, x, y, player):
        if player == 1:
            return (y == 11 and x >= 14) or \
                   (y == 12 and x >= 13) or \
                   (y == 13 and x >= 12) or \
                   (y == 14 and x >= 11) or \
                   (y == 15 and x >= 11)
        else:
            return (y == 4 and x <= 1) or \
                   (y == 3 and x <=2) or \
                   (y == 2 and x <=3) or \
                   (y == 1 and x <= 4) or \
                   (y == 0 and x <=4)

    def make_move(self, start, end):
        x1, y1 = start
        x2, y2 = end
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = 0
        
    
    def undo_move(self, start, end):
        x1, y1 = start
        x2, y2 = end
        self.board[x1][y1] = self.board[x2][y2]
        self.board[x2][y2] = 0
        

    def get_player_pieces(self, player):
        player_pieces = []
        for row in range(16):
            for col in range(16):
                if self.board[row][col] == player:
                    player_pieces.append((row, col))
        return player_pieces
    

    def count_adjacent_player_pieces(self, position, player):
        count = 0
        row, col = position
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if 0 <= row + dr < len(self.board) and 0 <= col + dc < len(self.board[0]) and (dr != 0 or dc != 0):
                    if self.board[row + dr][col + dc] == player:
                        count += 1
        return count


    def evaluate(self, heuristic):
        return heuristic(self, self.current_player)

    
    def play(self, player1, player2, heuristic1, heuristic2):
        players = {1: (player1, heuristic1), 2: (player2, heuristic2)}
        start_time = time.time()
        winner = False
        while not winner:
            print("Current board:")
            self.print_board()
            print("Player", self.current_player, "turn.")
            print(self.generate_possible_moves())

            # Wybór ruchu dla aktualnego gracza na podstawie odpowiedniej heurystyki
            player_func, heuristic = players[self.current_player]
            start, end = player_func(self, heuristic)
            print("Player", self.current_player, " move is: ", start, end)

            if self.is_valid_move(start, end):
                
                self.make_move(start, end)
               
                winner = self.check_winner()
                if(self.current_player == 1):
                    self.rounds += 1
                self.current_player = 1 if self.current_player == 2 else 2
            else:
                print("Invalid move! Try again.")

        end_time = time.time()
        game_time = end_time - start_time
        print("Current board:")
        self.print_board()
        print("Number of rounds:", self.rounds)
        print("Player", self.winner, "wins!")
        print("Game time:", game_time, "seconds")






#strategies 

#losowe ale premia za wyjście z bazy


def player_strategy(board: Halma, heuristic):
    possible_moves, _ = board.generate_possible_moves()
    move_scores = {}
    for move in possible_moves:
        start, end = move
        board.make_move(start, end)
        score = board.evaluate(heuristic)
        board.undo_move(start, end)
        move_scores[move] = score
    if move_scores:
        sorted_moves = sorted(move_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_moves[0][0]
    else:
        return None
    
def minimax(board: Halma, heuristic):
    def minmax(board: Halma, curDepth, maxTurn):
        visited_nodes[0] += 1
        if board.check_winner():
            return None, 99999
        elif curDepth == 0:
            board.current_player = player
            return None, board.evaluate(heuristic)
        moves, _ = board.generate_possible_moves()
        if maxTurn:
            max_val = float('-inf')
            best_move = None
            board.current_player = player
            for move in moves:
                start, end = move
                board.make_move(start, end)
                _, val = minmax(board, curDepth - 1, False)
                if val > max_val:
                    max_val = val
                    best_move = move
                board.undo_move(start, end)
            return best_move, max_val
        else:
            min_val = float('inf')
            best_move = None
            board.current_player = 2
            for move in moves:
                start, end = move
                board.make_move(start, end)
                _, val = minmax(board, curDepth - 1, True)
                if val < min_val:
                    min_val = val
                    best_move = move
                board.undo_move(start, end)
            return best_move, min_val
    visited_nodes = [0]
    player = 1
    best_move, _ = minmax(board, 2, True)
    board.current_player = player
    print("Number of visited nodes: " + str(visited_nodes[0]))
    return best_move

def minimax_pruning(board: Halma, heuristic):
    visited_nodes = [0]
    def minmax(board: Halma, curDepth, maxTurn, alpha, beta):
        visited_nodes[0] += 1
        if board.check_winner(): return None, 99999
        elif curDepth == 0:
            board.current_player = player
            return None, board.evaluate(heuristic)
        if maxTurn:
            max_val = float('-inf')
            best_move = None
            board.current_player = player
            moves, _ = board.generate_possible_moves()
            for move in moves:
                start, end = move
                board.make_move(start, end)
                _, val = minmax(board, curDepth - 1, False, alpha, beta) 
                if val > max_val:
                    max_val = val
                    best_move = move
                alpha = max(alpha, val)
                if beta <= alpha: 
                    board.undo_move(start, end) 
                    break
                board.undo_move(start, end) 
            return best_move, max_val
        else:
            min_val = float('inf')
            best_move = None
            board.current_player = 2
            moves, _ = board.generate_possible_moves()
            for move in moves:
                start, end = move
                board.make_move(start, end)
                _, val = minmax(board, curDepth - 1, True, alpha, beta)
                if val < min_val:
                    min_val = val
                    best_move = move
                beta = min(beta, val)
                if beta <= alpha:
                    board.undo_move(start, end)
                    break
                board.undo_move(start, end)
            return best_move, min_val

    alpha = float('-inf')
    beta = float('inf')
    player = 1
    board.current_player = player
    best_move, _ = minmax(board, 2, True, alpha, beta)
    print("Number of visited nodes: " + str(visited_nodes[0]))
    return best_move




def random_heuristic(board: Halma, player):
   return random.randrange(0, 1000)


def manhattan_distance_heuristic(board: Halma, player):
    score = 0
    if player == 1:
        opponent_camp = BLACK_START_POS
        end_point = (15,15)
    else:
        opponent_camp = WHITE_START_POS
        end_point = (0,0)
    
    pieces = board.get_player_pieces(player)
    score = 0
    for row, col in pieces:

        score -= (abs(row - end_point[0]) + abs(col - end_point[1]))

        if (row, col) not in opponent_camp:
            score -= 5
    return score



def chebyshev_distance_heuristic(board: Halma, player):
    if player == 1:
        opponent_camp = BLACK_START_POS
        end_point = (15,15)
    else:
        opponent_camp = WHITE_START_POS
        end_point = (0,0)
    
    score = 0
    pieces = board.get_player_pieces(player)

    pawns_in_end_goal = sum(1 for row, col in board.get_player_pieces(player) if (row, col) in opponent_camp)

    if pawns_in_end_goal > 0.85 * TOTAL_PAWNS and pawns_in_end_goal <19:
        empty_positions = [pos for pos in opponent_camp if board.board[pos[0]][pos[1]] == 0]
    
        not_in_opp_camp = [piece for piece in pieces if piece not in opponent_camp]
        distances_to_empty_positions = [max(abs(piece[0] - empty_pos[0]), abs(piece[1] - empty_pos[1])) for \
                                        piece in not_in_opp_camp for empty_pos in empty_positions]

        if distances_to_empty_positions:
            score -= min(distances_to_empty_positions)
    elif pawns_in_end_goal == TOTAL_PAWNS: return 9999 
    else:
        for piece in pieces:
            score -= max(abs(piece[0] - end_point[0]), abs(piece[1] - end_point[1]))
            
    for piece in pieces:
        if piece not in opponent_camp:
                score -=10
    return score



def forward_movement_heuristic(board: Halma, player):
    if player == 1:
        opponent_camp = BLACK_START_POS
    else:
        opponent_camp = WHITE_START_POS
    
    score = 0
    pieces = board.get_player_pieces(player)
    for piece in pieces:
        if piece not in opponent_camp :
               score -= 15
        if player == 1:
            score += piece[0] + piece[1]
        else: 
            score += 30 - piece[0] - piece[1]

    return score


def distance_proximity_heuristic(board: Halma, player):
    white_distance = 0
    black_distance = 0   
    white_proximity = 0
    black_proximity = 0
    white_start_penalty = 0
    black_start_penalty = 0
    for row in range(16):
        for col in range(16):
            piece = board.board[row][col]
            if piece == 1:
                white_distance += (15 - row) + (15 - col)
                if (row, col) in BLACK_START_POS:
                    white_proximity += 1
                if (row, col) in WHITE_START_POS:
                    white_start_penalty+= 15
            if piece == 2:
                black_distance += row + col
                if (row,col) in WHITE_START_POS:
                    black_proximity += 1
                if (row, col) in BLACK_START_POS:
                    black_start_penalty +=15
    if player==1:
        evaluation = black_distance - white_distance + (white_proximity - black_proximity)*5 - white_start_penalty + black_start_penalty
    else:
        evaluation = white_distance - black_distance +(black_proximity - white_proximity)*5 - black_start_penalty + white_start_penalty
    return evaluation

def diff_euclidean_heuristic(board: Halma, player):
    
    if player == 1:
        own_camp = WHITE_START_POS
        opponent_camp = BLACK_START_POS
        end_point = (15,15)
        opp_end_point = (0,0)
    else:
        own_camp = BLACK_START_POS
        opponent_camp = WHITE_START_POS
        end_point = (0,0)
        opp_end_point = (15,15)

    score = 0
    distance_to_opponent_camp = 0
    pieces = board.get_player_pieces(player)

    for piece in pieces:
        distance_to_opponent_camp += math.sqrt(math.pow(piece[0] - end_point[0], 2) + math.pow(piece[1] - end_point[1], 2))
        if piece in own_camp:
            score -=10
        if piece in opponent_camp:
            score +=5

        
    opp_pieces = board.get_player_pieces(3 - player)
    opponent_distance_to_player_camp = sum(math.sqrt(math.pow(end[0] - opp_end_point[0], 2) + math.pow(end[1] - opp_end_point[1], 2)) \
                                           for end in opp_pieces)
    score += opponent_distance_to_player_camp +-distance_to_opponent_camp

    return score

















