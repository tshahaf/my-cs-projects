import random
import sys
from typing import Optional, Tuple
from reversi import Reversi

def smart_bot_move(game: Reversi, player: int) -> Tuple[int, int]:
    """
    Smart bot scans all available moves, creates a sim_game that counts
    how many pieces will be on the board per available move, and returns
    the move that yields the largest count of pieces
    """
    moves = game.available_moves
    best_move = None
    best_count = 0
    for move in moves:
        sim_game = game.simulate_moves([move])
        count = len(sim_game._grid._location_of_pieces[player])
        if count > best_count:
            best_count = count
            best_move = move
    return best_move

def smarter_bot_move(game: Reversi, player: int) -> Tuple[int, int]:
    """
    Smarter bot scans all available moves. For each move, it creates a sim_game
    with the list of moves the other player has, creates another sim_game for 
    each move the enemy has and counts average num of pieces player has 
    after enemy moves. Then returns the move with the highest average. 
    """
    moves = game.available_moves
    best_move = None
    best_count = 0
    for move in moves:
        count = 0
        sim_game = game.simulate_moves([move])
        opponent_moves = sim_game.available_moves
        for o_move in opponent_moves:
            sim_game = game.simulate_moves([o_move])
            count += len(sim_game._grid._location_of_pieces[player])
        if len(opponent_moves) == 0:
            return move
        else:
            avg_count = count // len(opponent_moves)
        if avg_count > best_count:
            best_count = avg_count
            best_move = move
    return best_move

num_games = 100
player1_strat = ""
player2_strat = ""

for i, item in enumerate(sys.argv):
    if item == "-n":
        num_games = int(sys.argv[i + 1])
    if item == "-1":
        player1_strat = sys.argv[i + 1]
    if item == "-2":
        player2_strat = sys.argv[i + 1]

curr_game = 0
player_1_wins = 0
player_2_wins = 0
ties = 0

while curr_game < num_games:
    game = Reversi(8, 2, True)
    while not game.done:
        if game._turn == 1:
            if player1_strat == "smart":
                game.apply_move(smart_bot_move(game, 1))
            elif player1_strat == "very-smart":
                game.apply_move(smarter_bot_move(game, 1))
            else:
                game.apply_move(random.choice(game.available_moves))
        if game._turn == 2:
            if player2_strat == "smart":
                game.apply_move(smart_bot_move(game, 2))
            elif player2_strat == "very-smart":
                game.apply_move(smarter_bot_move(game, 2))
            else:
                game.apply_move(random.choice(game.available_moves))
    if game.outcome == [1]:
        player_1_wins += 1
    if game.outcome == [2]:
        player_2_wins += 1
    if game.outcome == [1,2]:    
        ties += 1 
    curr_game += 1



p1 = float("{:.2f}".format(player_1_wins / num_games * 100))
p2 = float("{:.2f}".format(player_2_wins / num_games * 100))
ties_percent = float("{:.2f}".format(ties / num_games * 100))
print(f"Player 1 wins:  {p1}%")
print(f"Player 2 wins:  {p2}%")
print(f"Ties:  {ties_percent}%")