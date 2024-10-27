
import random

class Board():

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

    def print_grid(self):
        ''' FUnction to print  the self.matrix to the stdout. It will join each element that is not none into a string followed by a " | ". Else
            it will place a "."'''
        print("Stato attuale della griglia:")
        for row in self.matrix:
            print(" | ".join(str(elem) if elem is not None else '.' for elem in row)) 
        print("-" * 29)

    def randomTurn(self):
        '''Function to choose whoever is gonna make the first move. Uses a tuple and random library to choose.'''
        random_choice = ('red','yellow')
        random_turn = random.choice(random_choice)
        if random_turn == 'red':
            print("Comincia il rosso!")
            self.redTurn = True
        else:
            print("Comincia il giallo!")
            Board.yellowTurn = True

    def button_assign_function(self):
        '''Function to assign to each button the self.buttonPressed() function on click.'''
        for button in self.buttons:
            button.clicked.connect(self.yellowMove)

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