from tkinter import *
from tkinter import messagebox
import math
import random

one = []
zero = []
# board eval
def evaluate(board1,com,player):
    winlist = ["012","345","678","036","147","258","048","246"]
    for i in range(8):
        a = winlist[i]
        b,c,d = int(a[0]),int(a[1]),int(a[2])
        if board1[b] == board1[c] == board1[d] == player:
            return -1
        elif board1[b] == board1[c] == board1[d] == com:
            return 1
     
    # check for win/lose
    for i in range(9):
        if board1[i] == "N":
            return None
    return 0
# minimax
def minimax(board2, depth, alpha, beta, ismax,com,player):
   global zero, one, minone
   score = evaluate(board2,com,player)
   if not score == None:
      return score
   elif ismax:
      best_score = -3
      for i in range(9):
         if board2[i] == "N":
            board2[i] = com
            score = minimax(board2,depth+1,alpha,beta,False,com,player)
            best_score = max(best_score,score)
            board2[i] = "N"
            if best_score == 1:
               one.append(i)
            elif best_score == 0:
               zero.append(i)
            alpha = max(alpha,score)
            if beta <= alpha:
                break
      return best_score
   elif not ismax:
      best_score = 3
      for i in range(9):
         if board2[i] == "N":
            board2[i] = player
            score = minimax(board2,depth+1,alpha,beta,True,com,player)
            best_score = min(best_score,score)
            board2[i] = "N"
            beta = min(beta,score)
            if beta <= alpha:
                break
      return best_score
#find best move
def find_best_move(board,com,player):
    best_move = None
    best_score = -float("inf")
    one = []
    zero = []
    minone = []
    for i in range(9):
        if board[i] == "N":
            board[i] = com
            score = minimax(board,0,-float("inf"),float("inf"),False,com,player)
            board[i] = "N"
            if score > best_score:
                best_score = score
                best_move = i
            if score == 1:
                one.append(i)
            elif score == 0:
                zero.append(i)
            elif score == -1:
                minone.append(i)
    if len(one) > 0:
        best_move = one[random.randint(0,len(one)-1)]   
    elif len(zero) > 0:
        best_move = zero[random.randint(0,len(zero)-1)]
    return best_move
#GUI
screen = Tk()
class TicTacToe():
    def __init__(self,screen):
        self.screen = screen
        self.buttons = []
        self.turn = " X "
        self.board = []
        self.moves = 0
        self.playerxo = " X "
        self.comxo = " O "
        self.screen.title("Tic Tac Toe")
        self.screen.resizable(False,False)
        self.win = 0
        self.draw = 0
        self.lose = 0
        self.singleplayer = True
        self.screen.configure(bg="Orange")
        img = PhotoImage(file="Logo.png")
        self.screen.iconphoto(False,img)

        for i in range(3):
            row = []
            r = []
            for j in range(3):
                button = Button(screen,text="    ",font=("Ds-Digital",30),bg="white",command=lambda x=i,y=j:self.change(x,y))
                button.grid(column=j,row=i+1)
                row.append(button)
                r.append("N")
            self.buttons.append(row)
            self.board.append(r)
        reset = Button(screen,text="  Reset  ",font=("Ds-Digital",25),fg="White",bg="Red",command=self.reset)
        reset.grid(row=3,column=3)
        self.bxo = Button(screen,text="Player as X",font=("Ds-Digital",25),bg="yellow",command=self.changexo)
        self.bxo.grid(row=2,column=3)
        l = Label(screen,text="XO Tic Tac Toe",font=("Ds-Digital",30),bg="orange")
        l.grid(row=0,columnspan=4)
        self.bsm = Button(screen,text="Singleplayer",font=("Ds-Digital",25),bg="blue",command=self.playerchange)
        self.bsm.grid(row=1,column=3)

    def change(self,x,y):
        if self.board[x][y] == "N" and self.turn==self.playerxo and self.singleplayer == True:
            self.buttons[x][y].config(text=self.playerxo)
            self.board[x][y] = self.playerxo
            self.moves += 1
            if self.checkwinner(self.playerxo):
                messagebox.showinfo(title="Info",message="You win!")
                self.reset()
            elif self.checkwinner(self.comxo):
                messagebox.showinfo(title="Info",message="Computer wins!")
                self.reset()
            elif self.moves == 9:
                messagebox.showinfo(title="Info",message="It's a draw!")
                self.reset()
            else:
                self.Ai_turn() 
        else:
            if self.board[x][y] == "N":
                self.board[x][y] = self.turn
                self.buttons[x][y].config(text=self.turn)
                self.moves += 1
                if self.checkwinner(self.turn):
                    if self.turn == " O ":
                        messagebox.showinfo(title="Info",message="Player O wins!")
                    else:
                        messagebox.showinfo(title="Info",message="Player X wins!")
                    self.reset()
                elif self.moves == 9:
                    messagebox.showinfo(title="Info",message="It's a draw!")
                    self.reset()
                else:
                    if self.turn == " X ":
                        self.turn = " O "
                    else:
                        self.turn = " X "
    def checkwinner(self,player):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                self.buttons[i][0].config(bg="green")
                self.buttons[i][1].config(bg="green")
                self.buttons[i][2].config(bg="green")
                return True
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                self.buttons[0][i].config(bg="green")
                self.buttons[1][i].config(bg="green")
                self.buttons[2][i].config(bg="green")
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            self.buttons[0][0].config(bg="green")
            self.buttons[1][1].config(bg="green")
            self.buttons[2][2].config(bg="green")
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            self.buttons[0][2].config(bg="green")
            self.buttons[1][1].config(bg="green")
            self.buttons[2][0].config(bg="green")
            return True
        return False
    def reset(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="    ",bg="white")
                self.board[i][j] = "N"
        self.moves = 0
        self.turn = " X "
        if self.singleplayer:
            if self.bxo['text'] == "Player as O":
                self.Ai_turn()
    def Ai_turn(self):
        self.turn = self.comxo
        boardcom = []
        for i in range(3):
            for j in range(3):
                boardcom.append(self.board[i][j])
        moves = find_best_move(boardcom,self.comxo,self.playerxo)
        if moves < 3:
            self.board[0][moves] = self.comxo
            self.buttons[0][moves].config(text=self.comxo)
            self.moves += 1
        elif moves >= 3 and moves < 6:
            self.board[1][moves-3] = self.comxo
            self.buttons[1][moves-3].config(text=self.comxo)
            self.moves += 1
        else:
            self.board[2][moves-6] = self.comxo
            self.buttons[2][moves-6].config(text=self.comxo)
            self.moves += 1
        if self.checkwinner(self.comxo):
            messagebox.showinfo(title="Info",message="Computer wins!")
            self.reset()
        elif self.checkwinner(self.playerxo):
            messagebox.showinfo(title="Info",message="You win!")
            self.reset()
        elif self.moves == 9:
            messagebox.showinfo(title="Info",message="It's a draw!")
            self.reset()
        else:
            self.turn = self.playerxo
    def changexo(self):
        if self.singleplayer:
            if self.bxo['text'] == "Player as X":
                self.bxo.config(text="Player as O")
                self.playerxo = " O "
                self.comxo = " X "
                self.reset()
            else:
                self.bxo.config(text="Player as X")
                self.playerxo = " X "
                self.comxo = " O "            
                self.reset()
    def playerchange(self):
        if self.singleplayer:
            self.singleplayer = False
            self.reset()
            self.bsm.config(text=" Multiplayer ")
        else:
            self.singleplayer = True
            self.reset()
            self.bsm.config(text="Singleplayer")
TicTacToe(screen)    
screen.mainloop()