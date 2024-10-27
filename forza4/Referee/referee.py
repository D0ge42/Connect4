from PySide6.QtCore import QTimer

class Referee():
    
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

    #WIP
    def draw(self):
        '''Function that will handle draws'''
        i = 1
        for button in self.buttons:
            if button.isEnabled():
                print(f"{i} bottoni abilitati")
                i += 1