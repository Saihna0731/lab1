import sys
import pygame
import numpy as np

# colors
white = (255, 255, 255)
Gray = (180, 180, 180)
Red = (255, 0, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)

# Preportions & sizes
Width = 300
Height = 300
Line_Width = 15
Board_Rows = 3
Board_Cols = 3
SQUARE_SIZE = Width // Board_Cols
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 12
CROSS_SPACE = SQUARE_SIZE // 4

HUMAN = 1
AI = 2

screen = None
board = np.zeros((Board_Rows, Board_Cols))
nodes_evaluated = 0


def draw_lines(color=white):
    for i in range(1, Board_Rows):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (Width, SQUARE_SIZE * i), Line_Width)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, Height), Line_Width)


def draw_figures(color=white):
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            left = col * SQUARE_SIZE + CROSS_SPACE
            right = col * SQUARE_SIZE + SQUARE_SIZE - CROSS_SPACE
            top = row * SQUARE_SIZE + CROSS_SPACE
            bottom = row * SQUARE_SIZE + SQUARE_SIZE - CROSS_SPACE

            if board[row][col] == HUMAN:
                center = (
                    int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                    int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                )
                pygame.draw.circle(screen, color, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == AI:
                pygame.draw.line(screen, color, (left, top), (right, bottom), CROSS_WIDTH)
                pygame.draw.line(screen, color, (left, bottom), (right, top), CROSS_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def avaible_square(row, col):
    return board[row][col] == 0


def is_board_full(check_board=None):
    if check_board is None:
        check_board = board
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            if check_board[row][col] == 0:
                return False
    return True


def check_win(player, check_board=None):
    if check_board is None:
        check_board = board

    for row in range(Board_Rows):
        if all(check_board[row][col] == player for col in range(Board_Cols)):
            return True
    for col in range(Board_Cols):
        if all(check_board[row][col] == player for row in range(Board_Rows)):
            return True
    if all(check_board[i][i] == player for i in range(Board_Rows)):
        return True
    if all(check_board[i][Board_Rows - 1 - i] == player for i in range(Board_Rows)):
        return True
    return False


def evaluate(check_board, depth):
    if check_win(AI, check_board):
        return 10 - depth
    if check_win(HUMAN, check_board):
        return depth - 10
    if is_board_full(check_board):
        return 0
    return None


def minimax(minimax_board, depth, is_maximizing):
    global nodes_evaluated
    nodes_evaluated += 1

    score = evaluate(minimax_board, depth)
    if score is not None:
        return score

    if is_maximizing:
        best_score = -1000
        for row in range(Board_Rows):
            for col in range(Board_Cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = AI
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(Board_Rows):
            for col in range(Board_Cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = HUMAN
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score


def best_move():
    global nodes_evaluated
    nodes_evaluated = 0
    best_score = -1000
    move = (-1, -1)
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            if board[row][col] == 0:
                board[row][col] = AI
                score = minimax(board, 1, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], AI)
        print(f"AI move {move}, score {best_score}, nodes {nodes_evaluated}")
        return True
    return False


def restart_game():
    screen.fill(Black)
    draw_lines()
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            board[row][col] = 0


def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption('XOXO Game')
    screen.fill(Black)
    draw_lines()

    player = HUMAN
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if avaible_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                    player = player % 2 + 1

                    if not game_over and not is_board_full():
                        best_move()
                        if check_win(AI):
                            game_over = True
                        player = player % 2 + 1

                    if not game_over and is_board_full():
                        game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    player = HUMAN
                    game_over = False

        if not game_over:
            draw_figures()
        else:
            if check_win(HUMAN):
                draw_figures(Green)
                draw_lines(Green)
            elif check_win(AI):
                draw_figures(Red)
                draw_lines(Red)
            else:
                draw_figures(Gray)
                draw_lines(Gray)

        pygame.display.update()


if __name__ == "__main__":
    main()
