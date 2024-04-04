"""
Reversi implementation.

Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from copy import deepcopy
import operator
from typing import Dict, List, Tuple, Optional



BoardGridType = List[List[Optional[int]]]
"""
Type for representing the state of the game board (the "grid")
as a list of lists. Each entry will either be an integer (meaning
there is a piece at that location for that player) or None,
meaning there is no piece in that location. Players are
numbered from 1.
"""

ListMovesType = List[Tuple[int, int]]
"""
Type for representing lists of moves on the board.
"""

class Piece:
    """
    Class to represent pieces
    """
    player: int
    location: Tuple[int,int]
    def __init__(self, player: int, location: Tuple[int, int]):
        self._player_value = player
        self._location = location


class Board:
    """
    Class to represent a game board.

    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        board (list): the game board
        location_of_pieces (dictionary): the location of each piece on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """
    side: int
    board: List[List[Optional[Piece]]]
    location_of_pieces: Dict[str, List[Tuple[int, int]]]

    def __init__(self, size):
        self._side = size
        self._board = [[None] * self._side for _ in range(self._side)]
        self._location_of_pieces = {}

    
    @property
    def list_board(self):
        return self._board


    @property
    def piece_count(self):
        sum = 0
        for value in self._location_of_pieces.values():
            sum += len(value)
        return sum

    def add_piece(self, player: int, location: Tuple[int, int]) -> None:
        """
        Add a piece represented by a piece to the board.

        Inputs:
            piece (string): the piece to add
            location (tuple): the (row, column) location of where to add
                the piece
        """
        row, col = location

        self._board[row][col] = player
        if player in self._location_of_pieces:
            if location not in self._location_of_pieces[player]:
                self._location_of_pieces[player].append(location)
        else:
            self._location_of_pieces[player] = [location]
    
    def get_piece(self, pos):
        if pos[0] <= len(self._board) and pos[1] <= len(self._board[0]):
            return self._board[pos[0]][pos[1]]
        else:
            return "Position not on the board"
    

direction_list = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
]


class ReversiBase(ABC):
    """
    Abstract base class for the game of Reversi
    """

    _side: int
    _players: int
    _othello: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        self._side = side
        self._players = players
        self._othello = othello

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    @abstractmethod
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        raise NotImplementedError

    @abstractmethod
    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        raise NotImplementedError

    @abstractmethod
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        raise NotImplementedError

def possible_moves(direction_list: List, own_pieces: List, enemy_pieces: List,
                    rows: int, cols: int) -> List[Tuple[int, int]]:
    """
    Takes list of all pieces and compiles list of moves depending on color

    Inputs:
        direction_list (list): list of all possible directions as tuples
        own_pieces (list): list of friendly pieces
        enemy_pieces (list): list of enemy pieces
        rows (int): number of rows
        cols (int): number of columns

    Returns:
        List of possible moves for friendly
    """
    moves: set
    sum: Tuple

    moves = set()
    for p in own_pieces:
        for direction in direction_list:
            sum = tuple(map(operator.add, p, direction))
            if sum in enemy_pieces:
                while sum in enemy_pieces:
                    sum = tuple(map(operator.add, sum, direction))
                if (sum[0] >= 0 and sum[1] >= 0) and (sum[0] < rows and 
                                                      sum[1] < cols):
                    if sum in enemy_pieces or sum in own_pieces:
                        pass
                    else:
                        moves.add(sum)
    return list(moves)


class Reversi(ReversiBase):
    """
    Reversi game
    """

    _grid: Board
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        even_side = side % 2
        even_players = players % 2
        super().__init__(side, players, othello)
        if even_side != even_players:
            raise ValueError("The parity of the board does not match the"
                             " number of players")
        if side <= 3:
            raise ValueError("The board must be of size 4x4 or above")
        self._grid = Board(side)
        if othello:
            smaller_side = side // 2 - 1
            larger_side = side // 2
            self._grid.add_piece(1, (larger_side, smaller_side))
            self._grid.add_piece(1, (smaller_side, larger_side))
            self._grid.add_piece(2, (larger_side, larger_side))
            self._grid.add_piece(2, (smaller_side, smaller_side))

        self._turn = 1
        self._num_moves = 0
        

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        return self._grid.list_board

    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        return self._turn


    @property
    def odd_smaller_side(self) -> int:
        """
        Returns the smaller side index for odd othello boards
        """
        return int(self._side/2 - self.num_players/2)


    @property
    def odd_larger_side(self) -> int:
        """
        Returns the smaller side index for odd othello boards
        """
        return int(self._side/2 + self.num_players/2)


    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        direction_list: List[Tuple[int, int]]
        own_pieces: List[Tuple[int, int]]
        enemy_pieces: List[Tuple[int, int]]

        own_pieces = []
        enemy_pieces = []
        moves = []

        # Othello Check
        possible_moves_list = []
        othello_moves = []
        all_pieces = []
        for piece_list in self._grid._location_of_pieces.values():
            for piece in piece_list:
                all_pieces.append(piece)
        for row in range(self.odd_smaller_side, self.odd_larger_side):
            for col in range(self.odd_smaller_side, self.odd_larger_side):
                othello_moves.append((row, col))
        if not self._othello and self._grid.piece_count < self.num_players**2:
            for move in othello_moves:
                if move not in all_pieces:
                    moves.append(move)
            return moves
                    
        direction_list = [
            (0, 1), #right
            (1, 1), #right-down
            (1, 0), #down
            (1, -1), #left-down
            (0, -1), #left
            (-1, -1), #left-up
            (-1, 0), #up
            (-1, 1) #right-up
        ]
        if self._turn in self._grid._location_of_pieces:
            own_pieces = self._grid._location_of_pieces[self._turn]
        if self._grid._location_of_pieces:
            for key, value in self._grid._location_of_pieces.items():
                if key != self._turn:
                    for loc in value:
                        enemy_pieces.append(loc)
        possible_moves_list = possible_moves(direction_list, own_pieces,
            enemy_pieces, self.size, self.size)
        if possible_moves_list:
            for p_move in possible_moves_list:
                moves.append(p_move)
        return moves

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        i = 0
        while i < self.num_players:
            if not self.available_moves:
                if self._turn == self.num_players:
                    self._turn = 1
                else: 
                    self._turn = self._turn + 1
            else:
                return False
            i += 1
        return True

    @property
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        winner: List[int]
        winnner_piece_count = 0
        winner = []
        if self.done:
            for k, v in self._grid._location_of_pieces.items():
                if len(v) > winnner_piece_count:
                    winner = []
                    winner.append(k)
                    winnner_piece_count = len(self._grid._location_of_pieces[k])
                elif len(v) == winnner_piece_count:
                    winner.append(k)
        if len(winner) > 0:
            return winner
        else:
            return []
                

    #
    # METHODS
    #
    def helper_eating_function(self, eaten_list):
        for key, value in self._grid._location_of_pieces.items():
            for piece in eaten_list:
                if piece in value:
                    value.remove(piece)
        for piece in eaten_list:
            self._grid.add_piece(self._turn, piece)

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        row, col = pos

        if row > self.size - 1 or col > self.size - 1 or row < 0 or col < 0:
            raise ValueError("Position is outside of the board")
        return self._grid._board[row][col]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        row, col = pos
        # Check if position is outside board
        if row > self.size - 1 or col > self.size - 1 or row < 0 or col < 0:
            raise ValueError("Position is outside of the board")
        # Check if there's already a piece in that position
        if self._grid.get_piece(pos) is not None:
            return False
        # If non-othello, make sure middle pieces are filled out first
        if not self._othello and self._grid.piece_count < self.num_players**2:
            if row in range(self.odd_smaller_side, self.odd_larger_side):
                if col in range(self.odd_smaller_side, self.odd_larger_side):
                    return True
                return False
        if pos in self.available_moves:
            return True
        return False

    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        own_pieces = []
        enemy_pieces = []
        direction_list = [
                (0, 1), #right
                (1, 1), #right-down
                (1, 0), #down
                (1, -1), #left-down
                (0, -1), #left
                (-1, -1), #left-up
                (-1, 0), #up
                (-1, 1) #right-up
            ]
        if self._turn in self._grid._location_of_pieces:
                own_pieces = self._grid._location_of_pieces[self._turn]
        if self._grid._location_of_pieces:
            for key, value in self._grid._location_of_pieces.items():
                if key != self._turn:
                    for loc in value:
                        enemy_pieces.append(loc)

        if not self.done:
            self._grid.add_piece(self._turn, pos)
            # turn pieces after move
            for direction in direction_list:
                eat_pieces_list = []
                curr = tuple(map(operator.add, pos, direction))
                if curr in enemy_pieces:
                    eat_pieces_list.append(curr)
                    while curr in enemy_pieces:
                        curr = tuple(map(operator.add, curr, direction))
                        #tuple unpack helper_eating_function
                        c_row, c_col = curr
                        if ((c_row >= 0 and c_col >= 0) and
                            (c_row < self.size and c_col < self.size)):
                            if curr in enemy_pieces:
                                eat_pieces_list.append(curr)
                                pass
                            elif curr in own_pieces:
                                self.helper_eating_function(eat_pieces_list)

        i = 0
        if self._turn != self.num_players:
            self._turn = self._turn + 1
            while not self.available_moves and i < self.num_players:
                self._turn = self._turn + 1
                if self._turn >= self.num_players:
                    self._turn = 1
                i += 1

        elif self._turn == self.num_players:
            self._turn = 1
            while not self.available_moves and i < self.num_players:
                self._turn = self._turn + 1
                i += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        if turn > self.num_players or turn <= 0:
            raise ValueError("the value of turn is inconsistent with the"\
                " number of players")
        if len(grid) != self.size:
            raise ValueError("the size of the grid is inconsistent with the"
                " size of the original grid")
        for row in range(len(grid)):
            for col in range(len(grid)):
                player_at_loc = grid[row][col]
                if player_at_loc is None:
                    continue
                elif player_at_loc < 0 or player_at_loc > self.num_players:
                    raise ValueError("the value in the grid is inconsistent"\
                    " with the number of players")
                elif player_at_loc is not None:
                    self._grid.add_piece(player_at_loc, (row, col))

        self._turn = turn

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        new_game = deepcopy(self)
        for move in moves:
            new_game.apply_move(move)
        return new_game
