
class AiWinCondition():
        def red_vertical_win_con(self):
            '''Function to check where there are 4 red coins in vertical'''
            red_consecutive_coins = 0
            for k in range(len(self.matrix[0])):
                red_consecutive_coins = 0
                for j in range(len(self.matrix)):
                    if self.matrix[j][k] == "R":
                        red_consecutive_coins += 1
                    else:
                        red_consecutive_coins = 0
                    if red_consecutive_coins == 4:
                        print("Red player won. Vertical win")
                        self.red_player_won = True
                        break

        def red_horizontal_win_con(self):
            '''Function to check where there are 4 red coins in horizontal.'''
            red_consecutive_coins = 0
            for k in range(len(self.matrix)):
                red_consecutive_coins = 0
                for j in range(len(self.matrix[0])):
                    if self.matrix[k][j] == "R":
                        red_consecutive_coins += 1
                    else:
                        red_consecutive_coins = 0
                    if red_consecutive_coins == 4:
                        print("Yellow player won. Horizontal win")
                        self.red_player_won = True
                        break

        def red_diagonal_win_con_negative(self):
            '''Function to check if there are 4 red coins diagonally aligned in a negative manner.'''
            for k in range(3,len(self.matrix[0])):
                for j in range(len(self.matrix)):
                    if (self.matrix[j][k] == "R" and self.matrix[j-1][k-1] == "R" and self.matrix[j-2][k-2] == "R" and self.matrix[j-3][k-3] == "R"):
                        red_consecutive_coins = 4
                        if red_consecutive_coins == 4:
                            print("Yellow player won Diagonally Negative!")
                            self.red_player_won = True
        
        def red_diagonal_win_con_positive(self):
            '''Function to check if there are 4 red coins diagonally aligned in a positive manner.'''
            for k in range(len(self.matrix[0])-3):
                for j in range(3,len(self.matrix)):
                    if (self.matrix[j][k] == "R" and self.matrix[j-1][k+1] == "R" and self.matrix[j-2][k+2] == "R" and self.matrix[j-3][k+3] == "R"):
                        red_consecutive_coins = 4
                        if red_consecutive_coins == 4:
                            print("Yellow player won Diagonally Positive!")
                            self.red_player_won = True
