# This Python file uses the following encoding: utf-8
import sys
import random

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from ui_form import Ui_MainWindow
from WinConPlayer.wincon import WinCondition
from WinConAi.winconAi import AiWinCondition



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Bool that will handle turns
        self.yellowTurn = False
        self.redTurn = False

        self.coordinateX = None
        self.coordinateY = None

        #Bool to check if someone won.
        self.red_player_won = False
        self.yellow_player_won = False

        #Winner text set to blank at start.
        self.ui.label.setText("")

        #2D matrix to simulate board. We'll use this to detect winners.
        self.matrix = [
            [None, None, None, None, None, None, None], 
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
        ]

        #Buttons list from where we'll retrieve buttons to  enable, disable etc.
        self.buttons = [
            self.ui.b00, self.ui.b01, self.ui.b02, self.ui.b03, self.ui.b04, self.ui.b05, self.ui.b06,
            self.ui.b10, self.ui.b11, self.ui.b12, self.ui.b13, self.ui.b14, self.ui.b15, self.ui.b16,
            self.ui.b20, self.ui.b21, self.ui.b22, self.ui.b23, self.ui.b24, self.ui.b25, self.ui.b26,
            self.ui.b30, self.ui.b31, self.ui.b32, self.ui.b33, self.ui.b34, self.ui.b35, self.ui.b36,
            self.ui.b40, self.ui.b41, self.ui.b42, self.ui.b43, self.ui.b44, self.ui.b45, self.ui.b46,
            self.ui.b50, self.ui.b51, self.ui.b52, self.ui.b53, self.ui.b54, self.ui.b55, self.ui.b56
            ]


        #Call self.button assign function.
        self.button_assign_function()

        #Assign restart button function.
        self.ui.restartButton.clicked.connect(self.resetBoard)

        #Call start_game function.
        self.start_game()
        self.randomTurn()
        if self.yellowTurn == False:
            self.ui.currentTurn.setStyleSheet(("color: red; background-color: red"))
        else:
            self.ui.currentTurn.setStyleSheet(("color: yellow; background-color: yellow"))
        if self.redTurn:
            self.redMove()


    def print_grid(self):
        ''' FUnction to print  the self.matrix to the stdout. It will join each element that is not none into a string followed by a " | ". Else
            it will place a "."'''
        print("Stato attuale della griglia:")
        for row in self.matrix:
            print(" | ".join(str(elem) if elem is not None else '.' for elem in row)) 
        print("-" * 29)

    
    def button_assign_function(self):
        '''Function to assign to each button the self.buttonPressed() function on click.'''
        for button in self.buttons:
            button.clicked.connect(self.yellowMove)

    def start_game(self):
        '''Function that will enable only deepest coin's slots to make it so the player cannot place floating coins.'''
        for button in self.buttons:
            if button.objectName() in ["b50","b51","b52","b53","b54","b55","b56"]:
                button.setEnabled(True)
            else:
                button.setMinimumSize(0,80)
                button.setMaximumSize(80,80)
                button.setStyleSheet("border-radius:40px; background-color:rgb(0,81,44);")
                button.setEnabled(False)    

    def enable_coins(self):
        '''Function that will enable and set-stylesheet for certain buttons. This button will be Y-1 cell from  selected button.'''
        if self.yellowTurn:
            self.coin_to_enable = (f"b{self.coordinateY - 1}{self.coordinateX}")
        elif self.redTurn:
            self.coin_to_enable = (f"b{self.redCoordinateY -1}{self.redCoordinateX}")
        for button in self.buttons:
            if button.objectName() == self.coin_to_enable:
                button.setEnabled(True)
                button.setMinimumSize(0,80)
                button.setMaximumSize(80,80)
                button.setStyleSheet("border-radius:40px; background-color: rgb(0,81,44)")

    def matrix_handling(self):
        '''Function to put "Y" on a 2d matrix. We'll need this function in order to detect a potential winner'''
        if self.yellowTurn:
            self.coordinateY = int(self.button_name[1])
            self.coordinateX = int(self.button_name[2])
            self.matrix[self.coordinateY][self.coordinateX] = "Y"
        else:
            self.redCoordinateY = int(self.red_button_name[1])
            self.redCoordinateX = int(self.red_button_name[2])
            self.matrix[self.redCoordinateY][self.redCoordinateX] = "R"

#------------------------------------------------------------------------------------------------------------------------#
#                                               YELLOW MOVE                                                              #
#------------------------------------------------------------------------------------------------------------------------#

    def yellowMove(self):
        '''Function that will handle player input. It places the coin on any choosen available spot, checks for win condition and
            eventually switch turn. It also uses a Qtimer Oneshot that will simulate bot thinking (2 seconds timer)'''
        if self.yellowTurn:
            self.button_name = self.sender().objectName()
            for button in self.buttons:
                if self.button_name == button.objectName():

                    #Change button style when clicked.
                    #Since buttons are by default square we've to edit min-max size and border radius each time a button is clicked.
                    button.setEnabled(False) #Make it so clicked buttons are disabled to avoid strange behaviours.
                    button.setMinimumSize(0,80) 
                    button.setMaximumSize(80,80)
                    button.setStyleSheet("border-radius:40px; color: yellow; background-color: yellow")

                    #Retrieve button coordinates. Coordinates serves different purposes like enabling coin spots etc.
                    self.coordinateY = int(self.button_name[1])
                    self.coordinateX = int(self.button_name[2])
                    
                    #Various methods used to fill the board and check wincons.
                    self.enable_coins() #Enable certain spots when a coin is
                    self.matrix_handling()
                    self.enable_coins()
                    WinCondition.vertical_win_con(self)
                    WinCondition.horizontal_win_con(self) 
                    WinCondition.diagonal_win_con_negative(self)
                    WinCondition.diagonal_win_con_positive(self)
                    self.check_winner()
                    self.print_grid()
                    self.yellowTurn = False
                    if self.yellowTurn == False:
                        self.ui.currentTurn.setStyleSheet(("color: red; background-color: red"))
                    self.redTurn = True
                    QTimer.singleShot(2000,self.redMove)

    def redMove(self):
        '''Function that handles red turn. It places coins, checks for win conditions and switch turn when self turn has finished.'''
        if self.redTurn:
            self.check_available_moves() #Check available move
            self.red_insert_coin() #Use above method to place a red coin.
            self.enable_coins() #Enable the coin above the one we've just placed.
            self.matrix_handling() #Place a "R" on the virtual 2d matrix.

            #Red players winCon
            AiWinCondition.red_horizontal_win_con(self)
            AiWinCondition.red_vertical_win_con(self)
            AiWinCondition.red_diagonal_win_con_negative(self)
            AiWinCondition.red_diagonal_win_con_positive(self)
            self.check_winner()
            #Uncomment to print grid to the stdout.
            self.print_grid()

            #Switch turn
            self.redTurn = False
            if self.redTurn == False:
                self.ui.currentTurn.setStyleSheet(("color: yellow; background-color: yellow"))
            self.yellowTurn = True
    

    #----------------------------------------------------------------------------------------------------------------------------#
    #                                           AI MOVE                                                                          #
    #----------------------------------------------------------------------------------------------------------------------------#
    

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

    def check_winner(self):
        '''Function that triggers if self.red_player_won or self.yellow_player_won is True.
           It displays a text message on screen and reset winner's bool to False'''
        if self.red_player_won:
            self.ui.label.setEnabled(True)
            self.ui.label.setText("BOT WON! CONGRATZ ᕙ(  •̀ ᗜ •́  )ᕗ")
            self.red_player_won = False
            QTimer.singleShot(2000, self.resetBoard)

        elif self.yellow_player_won:
            self.ui.label.setEnabled(True)
            self.ui.label.setText("YOU WON! CONGRATZ ᕙ(  •̀ ᗜ •́  )ᕗ")
            self.yellow_player_won = False
            QTimer.singleShot(2000,self.resetBoard)

    def draw(self):
        '''Function that will handle draws'''
        i = 1
        for button in self.buttons:
            if button.isEnabled():
                print(f"{i} bottoni abilitati")
                i += 1

    def resetBoard(self):
        '''Function to resetBoard to 0. It can be called either by clicking or winning/drawing the game.'''
        self.ui.label.setText("")
        for button in self.buttons:
            button.setStyleSheet(("border-radius:40px; background-color:rgb(0,81,44);"))
        self.start_game()
        self.ui.label.setText("")
        self.matrix = [
            [None, None, None, None, None, None, None], 
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
        ]
        self.yellowTurn = False
        self.redTurn = False
        self.randomTurn()
        if self.redTurn:
            self.redMove()
            
            
    def randomTurn(self):
        '''Function to choose whoever is gonna make the first move. Uses a tuple and random library to choose.'''
        random_choice = ('red','yellow')
        random_turn = random.choice(random_choice)
        if random_turn == 'red':
            print("Comincia il rosso!")
            self.redTurn = True
        else:
            print("Comincia il giallo!")
            self.yellowTurn = True
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
