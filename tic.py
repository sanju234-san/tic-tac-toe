import streamlit as st
import random
import math

st.set_page_config(page_title="Tic Tac Toe Vs Asknova")

#  User Inputs for names and board size
player_name = st.text_input("Enter your name:", "Player")
board_input = st.text_input("Enter board size (e.g., 3x3):", "3x3")

try:
    size = int(board_input[0])
except ValueError:
    st.error("Invalid input. Please enter like '3x3'.")
    st.stop()

#  Title & Setup also choose the symbol and difficulty
st.title(f"{size} × {size} Tic Tac Toe: {player_name} Vs Asknova")
st.markdown("Choose your symbol and difficulty level to start!")

symbol = st.radio("Pick your symbol:", ('X', 'O'))
difficulty = st.selectbox("Select difficulty:", ['Easy', 'Medium', 'Hard'])

#  Session State Setup 
if "B" not in st.session_state or len(st.session_state.B) != size * size:
    st.session_state.B = [' '] * (size * size)
    st.session_state.game_over = False
st.session_state.player_symbol = symbol
st.session_state.bot_symbol = "O" if symbol == "X" else "X"
B = st.session_state.B

# Winner Check asknova or player
def check_winner():
    s = size
    # Rows
    for i in range(s):
        row = B[i * s:(i + 1) * s]
        if row.count(row[0]) == s and row[0] != ' ':
            return row[0]
    # Columns
    for i in range(s):
        col = [B[i + j * s] for j in range(s)]
        if col.count(col[0]) == s and col[0] != ' ':
            return col[0]
    # Diagonals
    diag1 = [B[i * (s + 1)] for i in range(s)]
    if diag1.count(diag1[0]) == s and diag1[0] != ' ':
        return diag1[0]
    diag2 = [B[(i + 1) * (s - 1)] for i in range(s)]
    if diag2.count(diag2[0]) == s and diag2[0] != ' ':
        return diag2[0]
    # Tie
    if ' ' not in B:
        return "Tie"
    return None

# Bot Logic 
def b_easy():
    empty = [i for i in range(size * size) if B[i] == ' ']
    if empty:
        move = random.choice(empty)
        B[move] = st.session_state.bot_symbol

def bot_move_medium():
    # Try to win
    for i in range(size * size):
        if B[i] == ' ':
            B[i] = st.session_state.bot_symbol
            if check_winner() == st.session_state.bot_symbol:
                return
            B[i] = ' '
    # Try to block
    for i in range(size * size):
        if B[i] == ' ':
            B[i] = st.session_state.player_symbol
            if check_winner() == st.session_state.player_symbol:
                B[i] = st.session_state.bot_symbol
                return
            B[i] = ' '
    b_easy()

def b_hard():
    best_score = -math.inf
    best_index = -1
    for i in range(size * size):
        if B[i] == ' ':
            B[i] = st.session_state.bot_symbol
            score = minimax(B, 0,False)
            B[i] = ' '
            if score > best_score:
                best_score = score
                best_index = i
    if best_index != -1:
        B[best_index] = st.session_state.bot_symbol

#  Minimax for Hard Mode 
def minimax(board, depth, is_maximizing):
    result = check_winner()
    if result == st.session_state.bot_symbol:
        return 10 - depth
    elif result == st.session_state.player_symbol:
        return  depth -10
    elif result == "Tie":
        return 0

    scores = []
    for i in range(size * size):
        if board[i] == ' ':
            board[i] = st.session_state.bot_symbol if is_maximizing else st.session_state.player_symbol
            score = minimax(board, depth + 1 , not is_maximizing)
            scores.append(score)
            board[i] = ' '

    return max(scores) if is_maximizing else min(scores)

# Asknova Turn 
def Asknova():
    st.toast(" Asknova is thinking...")
    if difficulty == "Easy":
        b_easy()
    elif difficulty == "Medium":
        bot_move_medium()
    else:
        b_hard()

#  Display Board 
cols = st.columns(size)
for i in range(size * size):
    with cols[i % size]:
        if B[i] == ' ' and not st.session_state.game_over:
            if st.button(" ", key=f"btn_{i}"):
                B[i] = st.session_state.player_symbol
                if check_winner():
                    st.session_state.game_over = True
                else:
                    Asknova()
                    if check_winner():
                        st.session_state.game_over = True
        else:
            st.button(B[i], key=f"disp_{i}", disabled=True)

#  Result Output 
result = check_winner()
if result == st.session_state.player_symbol:
    st.success("You win!")
elif result == st.session_state.bot_symbol:
    st.error(" Asknova wins!")
elif result == "Tie":
    st.info(" It's a tie!")

#  Reset Button 
if st.button(" Reset Game"):
    st.session_state.B = [' '] * (size * size)
    st.session_state.game_over = False
