import pygame
from sys import exit
import numpy as np
from copy import deepcopy
from math import hypot

WINDOW_HEIGHT = 600
WINDOW_WIDTH  = 600

BOARD_HEIGHT = 8
BOARD_WIDTH  = 8

SQUARE_SIZE = min(WINDOW_HEIGHT//BOARD_HEIGHT,WINDOW_WIDTH//BOARD_WIDTH)

#pieces:
BLANK = 0
BLACK_MAN = 1
WHITE_MAN = 2

#colors:
BLACK = 1
WHITE = 2

player_color = WHITE
enemy_color  = BLACK

BLACK_PIECE_COLOR = '#1E1E1E'
WHITE_PIECE_COLOR = '#D5C5B2'

#game states:
WAITING_PLAYER = 0
PIECE_SELECTED = 1
PC_TURN = 2
BLACK_VICTORY = 3
WHITE_VICTORY = 4
DRAW = 5
START_SCREEN = 6

game_state = START_SCREEN

def init_board(width, height):
    board = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(BLANK)
        
        board.append(row)
    
    for j in range(0, width // 2):
        board[0][j] = enemy_color
        board[1][j] = enemy_color
        
        board[height-1][width-1-j] = player_color
        board[height-2][width-1-j] = player_color
    
    return np.array(board)
    
player_move = []
last_pc_move = []

def draw_board():
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_HEIGHT):
            x = j * SQUARE_SIZE
            y = i * SQUARE_SIZE
            
            color = '#A47449' # light square color
            if (i+j)%2 == 0:
                color = '#63462D' #dark square color
                
            pygame.draw.rect(screen, color, pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))
            
    if len(last_pc_move) >= 2: # Highlights squares to indicate last PC movement
        (i_from, j_from) = last_pc_move[0]
        (i_to, j_to) = last_pc_move[1]
        
        x = j_from * SQUARE_SIZE
        y = i_from * SQUARE_SIZE
        
        pygame.draw.rect(screen, '#DC143C', pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)) # Draws redish square
        
        x = j_to * SQUARE_SIZE
        y = i_to * SQUARE_SIZE
        
        pygame.draw.rect(screen, '#DC143C', pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))
        
        
    if game_state == PIECE_SELECTED:
        highlight_squares(board)
        
def highlight_squares(board):
    
    squares = [x for x in calculate_available_moves(board, player_color) if x[0] == player_move[0]]
    piece_size = SQUARE_SIZE * 0.25
    
    for s in squares:
        (i, j) = s[1]
        x = j * SQUARE_SIZE + (SQUARE_SIZE - piece_size) // 2
        y = i * SQUARE_SIZE + (SQUARE_SIZE - piece_size) // 2
        pygame.draw.ellipse(screen, '#D8D8D8', pygame.Rect(x, y, piece_size, piece_size)) # draw gray circles on available squares
    
    (i, j) = player_move[0]    
    x = j * SQUARE_SIZE
    y = i * SQUARE_SIZE
    
    pygame.draw.rect(screen, '#DC143C', pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)) # draw redish square under selected piece
               
def draw_pieces(board):
    shp = np.shape(board)
    #print(board)
    height = shp[0]
    width = shp[1]
    
    factor = 0.8
    
    for i in range(height):
        for j in range(width):
        
            piece_size = SQUARE_SIZE * factor
            x = j * SQUARE_SIZE + (SQUARE_SIZE - piece_size) // 2
            y = i * SQUARE_SIZE + (SQUARE_SIZE - piece_size) // 2
        
            if board[i, j] == BLACK:
                pygame.draw.ellipse(screen, BLACK_PIECE_COLOR, pygame.Rect(x, y, piece_size, piece_size))
                
            elif board[i, j] == WHITE:
                pygame.draw.ellipse(screen, WHITE_PIECE_COLOR, pygame.Rect(x, y, piece_size, piece_size))

def calculate_available_moves(board, color):
    
    available_moves = []
    
    shp = np.shape(board)
    height = shp[0]
    width = shp[1]
    
    if color == player_color:
        
        for i in range(height):
            for j in range(width):
                
                if board[i, j] == player_color: 
                    
                    if j > 0:
                        if board[i, j-1] == BLANK:
                            available_moves.append([(i,j), (i,j-1)])
                    
                    if j < width-1:
                        if board[i, j+1] == BLANK:
                            available_moves.append([(i,j), (i,j+1)])
                    
                    if j > 1:
                        if board[i, j-2] == BLANK and board[i, j-1] > BLANK:
                            available_moves.append([(i,j), (i,j-2)])
                    
                    if j < width-2:
                        if board[i, j+2] == BLANK and board[i, j+1] > BLANK:
                            available_moves.append([(i,j), (i,j+2)])
                        
                    if i > 0:
                    
                        if board[i-1, j] == BLANK:
                            available_moves.append([(i,j), (i-1,j)])
                            
                        if j > 0:
                            if board[i-1, j-1] == BLANK:
                                available_moves.append([(i,j), (i-1,j-1)])
                            
                        if j < width-1:
                            if board[i-1, j+1] == BLANK:
                                available_moves.append([(i,j), (i-1,j+1)])
                    
                    if i > 1:
                    
                        if board[i-2, j] == BLANK and board[i-1, j] > BLANK:
                            available_moves.append([(i,j), (i-2,j)])
                            
                        if j > 1:
                            if board[i-2, j-2] == BLANK and board[i-1, j-1] > BLANK:
                                available_moves.append([(i,j), (i-2,j-2)])
                            
                        if j < width-2:
                            if board[i-2, j+2] == BLANK and board[i-1, j+1] > BLANK:
                                available_moves.append([(i,j), (i-2,j+2)])
    
    elif color == enemy_color:
        
        for i in range(height):
            for j in range(width):
            
                move = [] # move.append((i, j))
                
                if board[i][j] == enemy_color: 
                    
                    if j > 0:
                        if board[i, j-1] == BLANK:
                            available_moves.append([(i,j), (i,j-1)])
                    
                    if j < width-1:
                        if board[i, j+1] == BLANK:
                            available_moves.append([(i,j), (i,j+1)]) 
                    
                    if j > 1:
                        if board[i, j-2] == BLANK and board[i, j-1] > BLANK:
                            available_moves.append([(i,j), (i,j-2)])
                    
                    if j < width-2:
                        if board[i, j+2] == BLANK and board[i, j+1] > BLANK:
                            available_moves.append([(i,j), (i,j+2)])
                
                    if i < height-1:
                    
                        if board[i+1, j] == BLANK:
                            available_moves.append([(i,j), (i+1,j)])
                            
                        if j > 0:
                            if board[i+1, j-1] == BLANK:
                                available_moves.append([(i,j), (i+1,j-1)])
                            
                        if j < width-1:
                            if board[i+1, j+1] == BLANK:
                                available_moves.append([(i,j), (i+1,j+1)])
                        
                        if i < height-2:
                        
                            if board[i+2, j] == BLANK and board[i+1, j] > BLANK:
                                available_moves.append([(i,j), (i+2,j)])
                                
                            if j > 1:
                                if board[i+2, j-2] == BLANK and board[i+1, j-1] > BLANK:
                                    available_moves.append([(i,j), (i+2,j-2)])
                                
                            if j < width-2:
                                if board[i+2, j+2] == BLANK and board[i+1, j+1] > BLANK:
                                    available_moves.append([(i,j), (i+2,j+2)])
    
    return available_moves

def is_move_valid(board, move):
    
    (i_from, j_from) = move[0]
    
    color = board[i_from, j_from]
    
    return move in calculate_available_moves(board, color)

def play_move(board, move):
    global game_state
    board_cpy = deepcopy(board)
   
    (i_from, j_from) = move[0]
    (i_to, j_to) = move[1]
    
    board_cpy[i_to, j_to] = board_cpy[i_from, j_from]
    
    board_cpy[i_from, j_from] = BLANK
    
    return board_cpy
    
def count_winning_pieces(board, color):
    shp = np.shape(board)
    height = shp[0]
    width = shp[1]
    
    winning_pieces = 0
    
    if color == enemy_color:
        for i in range(height-2, height):
            for j in range(width // 2, width):
                if board[i, j] == enemy_color:
                    winning_pieces += 1
                            
    else:
        for i in range(0, 2):
            for j in range(0, width // 2):
                if board[i, j] == player_color:
                    winning_pieces += 1
                    
    return winning_pieces
    
def evaluate(board):
    shp = np.shape(board)
    height = shp[0]
    width = shp[1]
    
    winning_enemy_count = 0
    avg_enemy_distance = 0
    winning_player_count = 0
    avg_player_distance = 0
    
    for i in range(0, height):
        for j in range(0, width):

            if board[i, j] == enemy_color:
                if i >= height - 2 and j >= width // 2:
                    winning_enemy_count += 1    
#                avg_enemy_distance += (height-1) - i + (width-1) - j # manhatan distance
                avg_enemy_distance += hypot((height-1) - i, (width-1) - j) # euclidian distance
            
            elif board[i, j] == player_color:
                if i <= 1 and j < width // 2:
                    winning_player_count += 1
                avg_player_distance += hypot(i, j) # manhatan distance
    
    if winning_enemy_count >= 8:
        return 1000
        
    if winning_player_count >= 8:
        return -1000
    
    avg_enemy_distance = avg_enemy_distance / 8
    avg_player_distance = avg_player_distance / 8
                
    return 1.25 * (winning_enemy_count - winning_player_count) - 2.5 * (avg_enemy_distance - avg_player_distance)

def winner(board):
    if count_winning_pieces(board, enemy_color) == 8:
        return enemy_color
    if count_winning_pieces(board, player_color) == 8:
        return player_color
        
    return BLANK

MINIMAX_MAX_DEPTH = 3
    
def minimax(board, is_maximizer, depth):
    global last_pc_move
    
    if depth == 0 or winner(board) != BLANK:
        return evaluate(board), board
        
    if is_maximizer:
        
        available_moves = calculate_available_moves(board, enemy_color)
        
        best_move = play_move(board, available_moves[-1]) # placeholder movement
        best_value = float('-inf')
        
        for move in available_moves:
            value, _ = minimax(play_move(board, move), False, depth-1)
    
            if value > best_value:
                best_value = value
                best_move = play_move(board, move)
        
                if depth == MINIMAX_MAX_DEPTH:
                    last_pc_move = move
            
        return best_value, best_move
        
    else:
        
        available_moves = calculate_available_moves(board, player_color)
        
        best_move = play_move(board, available_moves[-1]) # placeholder movement
        best_value = float('inf')
        
        for move in available_moves:
            value, _ = minimax(play_move(board, move), True, depth-1)
    
            if value < best_value:
                best_value = value
                best_move = play_move(board, move)
        
        return best_value, best_move

def pc_move(board):

    return minimax(board, True, MINIMAX_MAX_DEPTH)[1]
        
                
def event_loop():

    global game_state
    global player_move
    global board

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
             (x, y) = event.pos
             
             i = y // SQUARE_SIZE
             j = x // SQUARE_SIZE
             
             if game_state == WAITING_PLAYER:
                
                if board[i, j] == player_color:
                    player_move.append((i,j))
                    game_state = PIECE_SELECTED
             
             elif game_state == PIECE_SELECTED:
                
                (i_from, j_from) = player_move[0]
                
                if i == i_from and j == j_from:
                    player_move = []
                    game_state = WAITING_PLAYER
                    
                elif board[i, j] == player_color:
                    player_move = [(i,j)]
                    
                elif board[i, j] == BLANK:
                
                    player_move.append((i,j))
                    
                    if is_move_valid(board, player_move):
                        board = play_move(board, player_move)
                        player_move = []
                        game_state = PC_TURN
                        #game_state = WAITING_PLAYER
                    else:
                        player_move.pop()
                        
             elif game_state == BLACK_VICTORY or game_state == WHITE_VICTORY:
                game_state = START_SCREEN
                     

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Checkers Variant')
clock = pygame.time.Clock()

def draw_splash_screen():
    draw_board()
    piece_size = SQUARE_SIZE * 0.8
    x = SQUARE_SIZE * 3 + (SQUARE_SIZE - piece_size) // 2
    y = SQUARE_SIZE * 3 + (SQUARE_SIZE - piece_size) // 2

    pygame.draw.ellipse(screen, BLACK_PIECE_COLOR, pygame.Rect(x, y, piece_size, piece_size))

    x += SQUARE_SIZE
    y += SQUARE_SIZE

    pygame.draw.ellipse(screen, WHITE_PIECE_COLOR, pygame.Rect(x, y, piece_size, piece_size))

    test_font = pygame.font.SysFont('Arial', 35)
    
    initial_message = test_font.render('Choose your pieces',False,'#F5F5F5')
    initial_message_rect = initial_message.get_rect(center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
    screen.blit(initial_message,initial_message_rect)

while True:
    
    last_pc_move = []

    draw_splash_screen()
    pygame.display.update()
    
    while game_state == START_SCREEN:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 (x, y) = event.pos
                 game_state = WAITING_PLAYER
                 
                 if y < WINDOW_HEIGHT // 2:
                    player_color = BLACK
                    enemy_color  = WHITE
                    game_state = PC_TURN


    board = init_board(BOARD_WIDTH, BOARD_HEIGHT)


    while game_state != START_SCREEN:

        draw_board()
        draw_pieces(board)
        
        if winner(board) != BLANK: 
            game_state = BLACK_VICTORY
            winner_str = 'Black'
            
            if winner(board) == WHITE:
                game_state = WHITE_VICTORY
                winner_str = 'White'
        
            test_font = pygame.font.SysFont('Arial', 35)
    
            end_message_1 = test_font.render(winner_str + ' won',False,'#F5F5F5')
            end_message_rect_1 = end_message_1.get_rect(midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(end_message_1,end_message_rect_1)
    
            end_message_1 = test_font.render('Click the screen to play again',False,'#F5F5F5')
            end_message_rect_1 = end_message_1.get_rect(midtop = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(end_message_1,end_message_rect_1)
        
        event_loop()
        
        if game_state == PC_TURN:
            board = pc_move(board)
            game_state = WAITING_PLAYER
            #print(evaluate(board))
        
        clock.tick(60)
        pygame.display.update()
        
