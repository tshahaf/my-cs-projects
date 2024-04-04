import os
import sys
from typing import List, Tuple
import math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # pylint: disable=wrong-import-position
from pygame import mixer
from mocks import ReversiStub
from mocks import ReversiMock
from reversi import Reversi
import click



class ReversiGUI:
    """
    Class for a GUI-based reversi game
    """

    window : int
    surface : pygame.surface.Surface
    clock : pygame.time.Clock
    

    def __init__(self, window: int , side_len: int,
                 reversi: Reversi):
        """
        Constructor

        Parameters:
            window : int : height of window
            
            side : int : number of cells on a side of a square reversi grid
        """
        
        self.side = reversi.size


        self.window = window
        
        ##instance of reversi stub
        self.mock_instance = reversi
        
        # Initialize Pygame
        pygame.init()
        # Set window title
        pygame.display.set_caption("reversi")
        # Set window size
        self.surface = pygame.display.set_mode((window + side_len,
                                                window))
        self.clock = pygame.time.Clock()

        self.event_loop()
    
        
        
        
        pygame.mixer.music.load("media/background.wav")

        pygame.mixer.music.play(-1)  # -1 plays the music in an infinite loop

    
        

        
    

    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        side = self.side
        available_moves = self.mock_instance.available_moves
        
        
        # Background
        self.surface.fill((255, 255, 255))
        spacing = self.window/self.side
        for row in range(side):
            for col in range(side):
                #creating the grid
                grid_square = pygame.Rect(row*spacing, col*spacing, spacing, spacing)
                pygame.draw.rect(self.surface, (0, 0, 0), grid_square, 1)
                ##working on board pieces
                (x1, y1) = (row*spacing, col*spacing)
                (x2, y2) = (row*spacing + spacing, col*spacing + spacing)
                xcenter = (x1 + x2) / 2
                ycenter = (y1 + y2) / 2
                
                if self.mock_instance._grid._board[row][col] == 2:
                    pygame.draw.circle(self.surface, (1, 50, 32), (xcenter, ycenter), spacing/2.5)
                if self.mock_instance._grid._board[row][col] == 1:
                    pygame.draw.circle(self.surface, (250, 128, 114), (xcenter, ycenter), spacing/2.5)
                if self.mock_instance._grid._board[row][col] == 3:
                    pygame.draw.circle(self.surface, (0, 255, 255), (xcenter, ycenter), spacing/2.5)
                if self.mock_instance._grid._board[row][col] == 4:
                    pygame.draw.circle(self.surface, (102, 102, 255), (xcenter, ycenter), spacing/2.5)
                if self.mock_instance._grid._board[row][col] == 5:
                    pygame.draw.circle(self.surface, (255, 255, 0), (xcenter, ycenter), spacing/2.5)
                if self.mock_instance._grid._board[row][col] == 6:
                    pygame.draw.circle(self.surface, (255, 0, 0), (xcenter, ycenter), spacing/2.5)
                if self.mock_instance._grid._board[row][col] == 7:
                    pygame.draw.circle(self.surface, (51, 255, 255), (xcenter, ycenter), spacing/2.5)
                if self.mock_instance._grid._board[row][col] == 8:
                    pygame.draw.circle(self.surface, (153, 0, 153), (xcenter, ycenter), spacing/2.5)
                if self.mock_instance._grid._board[row][col] == 9:
                    pygame.draw.circle(self.surface, (0, 102, 0), (xcenter, ycenter), spacing/2.5)
        ##working on highlighting availiable moves
        for move in available_moves:
            m_row, m_col = move
            (x1, y1) = (m_row*spacing, m_col*spacing)
            (x2, y2) = (m_row*spacing + spacing, m_col*spacing + spacing)
            xcenter = (x1 + x2) / 2
            ycenter = (y1 + y2) / 2
            pygame.draw.circle(self.surface, (220, 220, 220), (xcenter, ycenter), spacing/2.5)
        ##screen when game is done
        if self.mock_instance.done:
            sub_surface = pygame.Surface((200, 150))
            sub_surface.fill((0,0,0))
            font = pygame.font.SysFont('comicsans', 24)
            winner = self.mock_instance.outcome
            if len(winner) == 2:
                text_surface = font.render('tie', True, (255, 255, 255))
                sub_surface.blit(text_surface, (10, 10))
                self.surface.blit(sub_surface,(200, 200))
            elif winner[0] == 1:
                text_surface = font.render('player 1 wins', True, (255, 255, 255))
                sub_surface.blit(text_surface, (10, 10))
                self.surface.blit(sub_surface,(200, 200))
            else:
                text_surface = font.render('player 2 wins', True, (255, 255, 255))
                sub_surface.blit(text_surface, (10, 10))
                self.surface.blit(sub_surface,(200, 200))
        ## working on player indication
        if self.mock_instance._turn == 1:
            pygame.draw.circle(self.surface, (250, 128, 114), (650, 300), 30 )
        elif self.mock_instance._turn == 2:
            pygame.draw.circle(self.surface,(1, 50, 32), (650, 300), 30 )
        elif self.mock_instance._turn == 3:
            pygame.draw.circle(self.surface,(0, 255, 255), (650, 300), 30 )
        elif self.mock_instance._turn == 4:
            pygame.draw.circle(self.surface,(102, 102, 255), (650, 300), 30 )
        elif self.mock_instance._turn == 5:
            pygame.draw.circle(self.surface,(255, 255, 0), (650, 300), 30 )
        elif self.mock_instance._turn == 6:
            pygame.draw.circle(self.surface,(255, 0, 0), (650, 300), 30 )
        elif self.mock_instance._turn == 7:
            pygame.draw.circle(self.surface,(51, 255, 255), (650, 300), 30 )
        elif self.mock_instance._turn == 8:
            pygame.draw.circle(self.surface,(153, 0, 153), (650, 300), 30 )
        elif self.mock_instance._turn == 9:
            pygame.draw.circle(self.surface,(0, 102, 0), (650, 300), 30 )
        


        





        


    def event_loop(self) -> None:
        """
        Handles user interactions

        Parameters: none beyond self

        Returns: nothing
        """
        side = self.side
        spacing = self.window/side
        

        while True:
            # Process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Handle any other event types here
                if event.type == pygame.MOUSEBUTTONDOWN and not self.mock_instance.done:
                    pos = pygame.mouse.get_pos()
                    mouse_x, mouse_y = pos
                    
                    cell_row = round((mouse_x - spacing/2)/spacing)
                    cell_col = round((mouse_y - spacing/2)/spacing)


                    
                    ## applying moves
                    if self.mock_instance.legal_move((cell_row, cell_col)):
                        self.mock_instance.apply_move((cell_row, cell_col))
                    

                    
                
                
            # Update the display
            self.draw_window()
            pygame.display.update()
            self.clock.tick(24)

@click.command()
@click.option('-n', '--num-players', type=int, default=2, help='Number of players')
@click.option('-s', '--board-size', type=int, default=8, help='Board size')
@click.option('--othello/--non-othello', default=True, help='Game mode')
def play_game(num_players, board_size, othello):
    # Check for valid combinations of parameters
    if (num_players % 2 == 1 and board_size % 2 == 0) or (num_players % 2 == 0 and board_size % 2 == 1):
        print('Invalid combination of players and board size.')
    reversi = ReversiGUI(window = 600, side_len = 100, reversi = Reversi(board_size, num_players, othello))

    
    


if __name__ == "__main__":
    play_game()
    
