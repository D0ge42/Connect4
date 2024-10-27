from Board.board import Board
from WinConAi.winconAi import AiWinCondition
from Referee.referee import Referee
import random

class Ai():
    
    def redMove(self):
        '''Function that handles red turn. It places coins, checks for win conditions and switch turn when self turn has finished.'''
        if self.redTurn:
            Ai.check_available_moves(self) #Check available move
            Ai.red_insert_coin(self) #Use above method to place a red coin.
            Board.enable_coins(self) #Enable the coin above the one we've just placed.
            Board.matrix_handling(self) #Place a "R" on the virtual 2d matrix.

            #Red players winCon
            AiWinCondition.red_horizontal_win_con(self)
            AiWinCondition.red_vertical_win_con(self)
            AiWinCondition.red_diagonal_win_con_negative(self)
            AiWinCondition.red_diagonal_win_con_positive(self)
            Referee.check_winner(self)
            #Uncomment to print grid to the stdout.
            Board.print_grid(self)

            #Switch turn
            self.redTurn = False
            if self.redTurn == False:
                self.ui.currentTurn.setStyleSheet(("color: yellow; background-color: yellow"))
            self.yellowTurn = True 

    def red_insert_coin(self):
        '''Function to place a red player coin. It will use the spot provided by check_available_moves.'''
        for button in self.buttons:
            if self.red_button_name == button.objectName():
                button.setEnabled(False) #Make it so clicked buttons are disabled to avoid strange behaviours.
                button.setMinimumSize(0,80) 
                button.setMaximumSize(80,80)
                button.setStyleSheet("border-radius:40px; color: red; background-color: red")
                self.redCoordinateY = int(self.red_button_name[1])
                self.redCoordinateX = int(self.red_button_name[2])

    def check_available_moves(self):
        '''Function to check which available moves are available for the bot.'''
        available_moves = []
        seen = None
        for button in self.buttons:
            if button.isEnabled() == True:
                available_moves.append(button)

        for button in available_moves:
            if button.isEnabled() == True:
                move = random.choice(available_moves)
                if seen != move:
                    move_to_use = move
                else:
                    continue
                break
        self.red_button_name = (move_to_use.objectName())
    