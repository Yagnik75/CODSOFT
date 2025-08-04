from termcolor import colored

# Initial board

board = [[" " for _ in range(3)] for _ in range(3)]


# Print the board
def print_board(board):
    for i in range(3):
        print(" " + " | ".join(board[i]))
        if i < 2:
            print("---+---+---")
    print()


# Check for winner
def check_winner(board):
    for row in board:
        if row.count(row[0]) == 3 and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None


# Check if board is full
def is_full(board):
    return all(cell != " " for row in board for cell in row)


# Human vs Human
def human():
    print("You are now playing against a human.")
    player = "X"
    while True:
        print_board(board)
        print(colored(f"{player}'s turn.", "red"))
        try:
            row = int(input("Enter row (0, 1, or 2): "))
            col = int(input("Enter column (0, 1, or 2): "))
        except ValueError:
            print("Please enter numbers only.")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            exit()
        if not (0 <= row < 3 and 0 <= col < 3):
            print("That's out of bounds. Try again.")
            continue
        if board[row][col] != " ":
            print("Cell already taken! Try again.")
            continue
        board[row][col] = player

        if check_winner(board):
            print_board(board)
            print(colored(f"Player {player} wins!", "yellow"))
            break
        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break

        player = "O" if player == "X" else "X"


# Human vs Computer
def computer():
    print("You are playing against the computer.")

    # Ask user for symbol and who goes first
    while True:
        human_symbol = input("Choose your symbol (X or O): ").upper()
        if human_symbol in ["X", "O"]:
            break
        else:
            print("Please enter X or O only.")

    ai_symbol = "O" if human_symbol == "X" else "X"

    while True:
        first = input("Do you want to go first? (y/n): ").lower()
        if first in ["y", "n"]:
            break
        else:
            print("Please enter y or n.")

    player = human_symbol if first == "y" else ai_symbol

    # Minimax algorithm
    def minimax(board, is_maximizing):
        winner = check_winner(board)
        if winner == ai_symbol:
            return 1
        elif winner == human_symbol:
            return -1
        elif is_full(board):
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = ai_symbol
                        score = minimax(board, False)
                        board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = human_symbol
                        score = minimax(board, True)
                        board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    # AI best move
    def best_move():
        best_score = -float("inf")
        move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = ai_symbol
                    score = minimax(board, False)
                    board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    # Play game
    while True:
        if player == ai_symbol:
            print("Computer goes first.")
            row, col = best_move()
            board[row][col] = ai_symbol
            player = human_symbol  # Switch to human for next turn
        print_board(board)

        if player == human_symbol:
            print(f"Your turn! (You are {human_symbol})")
            try:
                row = int(input("Enter row (0, 1, or 2): "))
                col = int(input("Enter column (0, 1, or 2): "))
            except ValueError:
                print("Please enter numbers only.")
                continue
            except (EOFError, KeyboardInterrupt):
                print("\nExiting game.")
                exit()
            if not (0 <= row < 3 and 0 <= col < 3):
                print("That's out of bounds. Try again.")
                continue
            if board[row][col] != " ":
                print("That spot is already taken. Try again.")
                continue
            board[row][col] = human_symbol
        else:
            print("Computer is thinking...")
            row, col = best_move()
            board[row][col] = ai_symbol

        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == human_symbol:
                print("You win!")
            else:
                print("Computer wins!")
            break

        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break

        player = ai_symbol if player == human_symbol else human_symbol


# Game launcher
choice = input("Do you want to play against a human? (y/n): ").lower()
if choice == "y":
    human()
else:
    computer()
