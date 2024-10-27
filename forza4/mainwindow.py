# This Python file uses the following encoding: utf-8
import sys
import random

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from ui_form import Ui_MainWindow
from WinConPlayer.wincon import WinCondition
from Board.board import Board
from Ai.ai import Ai
from Referee.referee import Referee


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Bool that will handle turns
        self.yellowTurn = False
        self.redTurn = False
        #Yellow player move coordinates
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
        Board.button_assign_function(self)

        #Assign restart button function.
        self.ui.restartButton.clicked.connect(self.resetBoard)

        #Call start_game function.
        Board.start_game(self)
        Board.randomTurn(self)
        if self.yellowTurn == False:
            self.ui.currentTurn.setStyleSheet(("color: red; background-color: red"))
        else:
            self.ui.currentTurn.setStyleSheet(("color: yellow; background-color: yellow"))
        if self.redTurn:
            Ai.redMove(self) 

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
                    Board.enable_coins(self) #Enable certain spots when a coin is
                    Board.matrix_handling(self)
                    Board.enable_coins(self)
                    WinCondition.vertical_win_con(self)
                    WinCondition.horizontal_win_con(self) 
                    WinCondition.diagonal_win_con_negative(self)
                    WinCondition.diagonal_win_con_positive(self)
                    Referee.check_winner(self)
                    Board.print_grid(self)
                    self.yellowTurn = False
                    if self.yellowTurn == False:
                        self.ui.currentTurn.setStyleSheet(("color: red; background-color: red"))
                    self.redTurn = True
                    QTimer.singleShot(2000, lambda: Ai.redMove(self))

 
    #----------------------------------------------------------------------------------------------------------------------------#
    #                                           AI MOVE                                                                          #
    #----------------------------------------------------------------------------------------------------------------------------#
 
    def resetBoard(self):
        '''Function to resetBoard to 0. It can be called either by clicking or winning/drawing the game.'''
        self.ui.label.setText("")
        for button in self.buttons:
            button.setStyleSheet(("border-radius:40px; background-color:rgb(0,81,44);"))
        Board.start_game(self)
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
        Board.randomTurn(self)
        if self.redTurn:
            Ai.redMove(self)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
