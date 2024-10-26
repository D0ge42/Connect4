    
#------------------------------------------------------------------------------------------------------------------#
#                                    CHECK YELLOW PLAYER WIN-CON                                                   #
#------------------------------------------------------------------------------------------------------------------#i

class WinCondition():

    def vertical_win_con(self):
        '''Function to check where there are 4 yellow coins in vertical'''
        consecutive_coins = 0
        for k in range(len(self.matrix[0])):
            consecutive_coins = 0
            for j in range(len(self.matrix)):
                if self.matrix[j][k] == "Y":
                    consecutive_coins += 1
                else:
                    consecutive_coins = 0
                if consecutive_coins == 4:
                    print("Yellow player won. Vertical win")
                    self.yellow_player_won = True
                    break

    def horizontal_win_con(self):
        '''Function to check where there are 4 yellow coins in horizontal.'''
        consecutive_coins = 0
        for k in range(len(self.matrix)):
            consecutive_coins = 0
            for j in range(len(self.matrix[0])):
                if self.matrix[k][j] == "Y":
                    consecutive_coins += 1
                else:
                    consecutive_coins = 0
                if consecutive_coins == 4:
                    print("Yellow player won. Horizontal win")
                    self.yellow_player_won = True
                    break

    def diagonal_win_con_negative(self):
        '''Function to check if there are 4 coins diagonally aligned in a negative manner.'''
        for k in range(3,len(self.matrix[0])):
            for j in range(len(self.matrix)):
                if (self.matrix[j][k] == "Y" and self.matrix[j-1][k-1] == "Y" and self.matrix[j-2][k-2] == "Y" and self.matrix[j-3][k-3] == "Y"):
                    consecutive_coins = 4
                    if consecutive_coins == 4:
                        print("Yellow player won Diagonally Negative!")
                        self.yellow_player_won = True

    def diagonal_win_con_positive(self):
        '''Function to check if there are 4 coins diagonally aligned in a positive manner.'''
        for k in range(len(self.matrix[0])-3):
            for j in range(3,len(self.matrix)):
                if (self.matrix[j][k] == "Y" and self.matrix[j-1][k+1] == "Y" and self.matrix[j-2][k+2] == "Y" and self.matrix[j-3][k+3] == "Y"):
                    consecutive_coins = 4
                    if consecutive_coins == 4:
                        print("Yellow player won Diagonally Positive!")
                        self.yellow_player_won = True