# This Python file uses the following encoding: utf-8
import sys
import random

from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Yellow dictionary where we'll put yellow player coin's coordinates.
        self.yellow_dic = {}

        #Bool that will handle turns
        self.yellowTurn = False
        self.redTurn = False

        #Bool to check if someone won.
        self.someone_won = False

        #2D matrix
        self.matrix = [
            [None, None, None, None, None, None, None], 
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
        ]

        #Index needed to feel the self.yellow dictionary.
        self.i = 0

        #Buttons list.
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

        #Call start_game function.
        self.start_game()
    
    
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
                button.setStyleSheet("border-radius:40px; background-color: #a4acb0")
                button.setEnabled(False)    

    def enable_coins(self):
        '''Function that will enable certain buttons. This button will be Y-1 cell from  selected button.'''
        self.coin_to_enable = (f"b{self.coordinateY - 1}{self.coordinateX}")
        for button in self.buttons:
            if button.objectName() == self.coin_to_enable:
                button.setEnabled(True)
                button.setMinimumSize(0,80)
                button.setMaximumSize(80,80)
                button.setStyleSheet("border-radius:40px; background-color: rgb(28, 113, 216)")

    def matrix_handling(self):
        '''Function to put "Y" on a 2d matrix. We'll need this function in order to detect a potential winner'''
        self.coordinateY = int(self.button_name[1])
        self.coordinateX = int(self.button_name[2])
        self.matrix[self.coordinateY][self.coordinateX] = "Y"

    #------------------------------------------------------------------------------------------------------------------#
    #                                    CHECK YELLOW PLAYER WIN-CON                                                   #
    #------------------------------------------------------------------------------------------------------------------#
    def vertical_win_con(self):
        '''Function to check where there are 4 yellow coins in vertical'''
        consecutive_coins = 0
        for k in range(len(self.matrix[0])):
            consecutive_coins = 0
            for j in range(len(self.matrix)):
                if self.matrix[j][k] == "Y":
                    consecutive_coins += 1
                if consecutive_coins == 4:
                    print("Yellow player won. Vertical win")
                    self.someone_won = True
                    break

    def horizontal_win_con(self):
        '''Function to check where there are 4 yellow coins in horizontal.'''
        consecutive_coins = 0
        for k in range(len(self.matrix)):
            consecutive_coins = 0
            for j in range(len(self.matrix[0])):
                if self.matrix[k][j] == "Y":
                    consecutive_coins += 1
                if consecutive_coins == 4:
                    print("Yellow player won. Horizontal win")
                    self.someone_won = True
                    break

    def diagonal_win_con_negative(self):
        '''Function to check if there are 4 coins diagonally aligned in a negative manner.'''
        for k in range(3,len(self.matrix[0])):
            for j in range(len(self.matrix)):
                if (self.matrix[j][k] == "Y" and self.matrix[j-1][k-1] == "Y" and self.matrix[j-2][k-2] == "Y" and self.matrix[j-3][k-3] == "Y"):
                    consecutive_coins = 4
                    if consecutive_coins == 4:
                        print("Yellow player won Diagonally Negative!")
    
    def diagonal_win_con_positive(self):
        '''Function to check if there are 4 coins diagonally aligned in a positive manner.'''
        for k in range(len(self.matrix[0])-3):
            for j in range(3,len(self.matrix)):
                if (self.matrix[j][k] == "Y" and self.matrix[j-1][k+1] == "Y" and self.matrix[j-2][k+2] == "Y" and self.matrix[j-3][k+3] == "Y"):
                    consecutive_coins = 4
                    if consecutive_coins == 4:
                        print("Yellow player won Diagonally Positive!")   

#------------------------------------------------------------------------------------------------------------------------#
#                                               YELLOW MOVE                                                              #
#------------------------------------------------------------------------------------------------------------------------#

    def yellowMove(self):
        '''Function that will handle button clicked event. When a button is clicked, we'll turn the current button to yellow.
        Each time a button is clicked and a coin is added, we'll check for vertical, horizontal and diagonal win condition'''
        self.button_name = self.sender().objectName()
        for button in self.buttons:
            if self.button_name == button.objectName():
                #Change button style when clicked.
                #Since buttons are by default square we've to edit min-max size and border radius each time a button is clicked.
                button.setEnabled(False) #Make it so clicked buttons are disabled to avoid strange behaviours.
                button.setMinimumSize(0,80) 
                button.setMaximumSize(80,80)
                button.setStyleSheet("border-radius:40px; color: yellow; background-color: yellow")
                #Retrieve button coordinates and put them inside the dictionary along with a "Yellow tag."
                self.coordinateY = int(self.button_name[1])
                self.coordinateX = int(self.button_name[2])
                #Previously declared index used for the dictionary.
                self.i += 1
                self.yellow_dic[self.i] = self.coordinateX, self.coordinateY , "yellow"

                #Various methods used to fill the board and check wincons.
                self.enable_coins() #Enable certain spots when a coin is
                self.matrix_handling()
                self.check_available_moves()
                self.vertical_win_con()
                self.horizontal_win_con()
                self.diagonal_win_con_negative()
                self.diagonal_win_con_positive()
    
    def yellowTurn(self):
        self.yellowTurn = True
        self.redTurn = False
    
    def redTurn(self):
        self.redTurn = True
        self.yellowTurn = False
    

    #----------------------------------------------------------------------------------------------------------------------------#
    #                                           AI MOVE                                                                          #
    #----------------------------------------------------------------------------------------------------------------------------#
    
    def check_available_moves(self):
        '''Function to check which available moves are available for the bot.'''
        available_moves = []
        for button in self.buttons:
            if button.isEnabled() == True:
                available_moves.append(button.objectName())
        return random.choice(available_moves)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
