
import Tkinter

from Tkinter import *
import chessboard
from PIL import Image
from PIL import ImageTk



from tkFileDialog import askopenfilename

global game_board, turn, wcastle, bcastle, wcaptured, bcaptured

turn = 1
wcastle = 0
bcastle = 0
selected = None
moves = []
captures = []
wcaptured = []
bcaptured = []
game_board = [None for i in range(64)]
en_passent = None

def attacked_spaces(player,board):
    """Returns which spaces a player is currently able to attack"""

    attacked = []

    for i in range(64):
        if board[i] == None:
            continue

        # Pawn for player 1
        if board[i] == 'P1' and player == 1:
            if i%8 != 0:
                attacked.append(i+7)
            if i%8 != 7:
                attacked.append(i+9)

        # Pawn for player 2
        if board[i] == 'P2' and player == 2:
            if i%8 != 7:
                attacked.append(i-7)
            if i%8 != 0:
                attacked.append(i-9)

        # Rook and half of Queen for both players
        if board[i][0] in 'RQ' and board[i][1] == str(player):
            x,y = i%8,i//8

            for j in range(x+1,8,1):
                attacked.append(j+y*8)
                if board[j+y*8] != None:
                    break

            for j in range(x-1,-1,-1):
                attacked.append(j+y*8)
                if board[j+y*8] != None:
                    break

            for j in range(y+1,8,1):
                attacked.append(x+j*8)
                if board[x+j*8] != None:
                    break

            for j in range(y-1,-1,-1):
                attacked.append(x+j*8)
                if board[x+j*8] != None:
                    break

        # Bishop and other half of Queen for both players
        if board[i][0] in 'BQ' and board[i][1] == str(player):

            j = i+7
            while (j-7)%8 != 0 and (j-7)//8 != 7:
                attacked.append(j)
                if board[j] != None:
                    break
                j += 7

            j = i+9
            while (j-9)%8 != 7 and (j-9)//8 != 7:
                attacked.append(j)
                if board[j] != None:
                    break
                j += 9

            j = i-7
            while (j+7)%8 != 7 and (j+7)//8 != 0:
                attacked.append(j)
                if board[j] != None:
                    break
                j -= 7

            j = i-9
            while (j+9)%8 != 0 and (j+9)//8 != 0:
                attacked.append(j)
                if board[j] != None:
                    break
                j -= 9

        # Knight for both players
        if board[i][0] == 'N' and board[i][1] == str(player):
            x,y = i%8,i//8

            if x >= 2 and y <= 6:
                attacked.append((x-2)+(y+1)*8)
            if x >= 1 and y <= 5:
                attacked.append((x-1)+(y+2)*8)

            if x <= 6 and y <= 5:
                attacked.append((x+1)+(y+2)*8)
            if x <= 5 and y <= 6:
                attacked.append((x+2)+(y+1)*8)

            if x <= 5 and y >= 1:
                attacked.append((x+2)+(y-1)*8)
            if x <= 6 and y >= 2:
                attacked.append((x+1)+(y-2)*8)

            if x >= 1 and y >= 2:
                attacked.append((x-1)+(y-2)*8)
            if x >= 2 and y >= 1:
                attacked.append((x-2)+(y-1)*8)

        if board[i][0] == 'K' and board[i][1] == str(player):
            x,y = i%8,i//8

            if x >= 1 and y <= 6:
                attacked.append((x-1)+(y+1)*8)
            if y <= 6:
                attacked.append(x+(y+1)*8)
            if x <= 6 and y <= 6:
                attacked.append((x+1)+(y+1)*8)
            if x <= 6:
                    attacked.append((x+1)+y*8)
            if x <= 6 and y >= 1:
                attacked.append((x+1)+(y-1)*8)
            if y >= 1:
                attacked.append(x+(y-1)*8)
            if x >= 1 and y >= 1:
                attacked.append((x-1)+(y-1)*8)
            if x >= 1:
                attacked.append((x-1)+y*8)

    return attacked

def select_piece(location):
    """Attempts to select the piece at location"""

    global selected,moves,captures

    # Notes:
    # this function is so complicated because it finds where the newly selected piece can move and capture

    # Remove illegal selections
    if game_board[location] == None or game_board[location][1] != str(turn):
        return

    selected = location
    moves = []
    captures = []

    # Pawn for player 1
    if game_board[selected] == 'P1':
        if game_board[selected+8] == None:
            moves.append(selected+8)
            if selected//8 == 1 and game_board[selected+16] == None:
                moves.append(selected+16)
        if selected%8 != 0 and ((game_board[selected+7] != None and game_board[selected+7][1] == '2') or \
                                (game_board[selected-1] == 'P2' and en_passent == selected-1)):
            captures.append(selected+7)
        if selected%8 != 7 and ((game_board[selected+9] != None and game_board[selected+9][1] == '2') or \
                                (game_board[selected+1] == 'P2' and en_passent == selected+1)):
            captures.append(selected+9)

    # Pawn for player 2
    if game_board[selected] == 'P2':
        if game_board[selected-8] == None:
            moves.append(selected-8)
            if selected//8 == 6 and game_board[selected-16] == None:
                moves.append(selected-16)
        if selected%8 != 7 and ((game_board[selected-7] != None and game_board[selected-7][1] == '1') or \
                                (game_board[selected+1] == 'P1' and en_passent == selected+1)):
            captures.append(selected-7)
        if selected%8 != 0 and ((game_board[selected-9] != None and game_board[selected-9][1] == '1') or \
                                (game_board[selected-1] == 'P1' and en_passent == selected-1)):
            captures.append(selected-9)

    # Rook and half of Queen for both players
    if game_board[selected][0] in 'RQ':
        x,y = selected%8,selected//8

        for i in range(x+1,8,1):
            if game_board[i+y*8] == None:   # Check if no blocking piece
                moves.append(i+y*8)
            elif game_board[i+y*8][1] != str(turn): # Check if is attacking
                captures.append(i+y*8)
                break
            else:
                break

        for i in range(x-1,-1,-1):
            if game_board[i+y*8] == None:
                moves.append(i+y*8)
            elif game_board[i+y*8][1] != str(turn):
                captures.append(i+y*8)
                break
            else:
                break

        for i in range(y+1,8,1):
            if game_board[x+i*8] == None:
                moves.append(x+i*8)
            elif game_board[x+i*8][1] != str(turn):
                captures.append(x+i*8)
                break
            else:
                break

        for i in range(y-1,-1,-1):
            if game_board[x+i*8] == None:
                moves.append(x+i*8)
            elif game_board[x+i*8][1] != str(turn):
                captures.append(x+i*8)
                break
            else:
                break

    # Bishop and other half of Queen for both players
    if game_board[selected][0] in 'BQ':

        i = selected+7
        while (i-7)%8 != 0 and (i-7)//8 != 7:   # Check if valid move
            if game_board[i] == None:   # Check if no blocking piece
                moves.append(i)
            elif game_board[i][1] != str(turn): # Check if is attacking
                captures.append(i)
                break
            else:
                break
            i += 7

        i = selected+9
        while (i-9)%8 != 7 and (i-9)//8 != 7:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(turn):
                captures.append(i)
                break
            else:
                break
            i += 9

        i = selected-7
        while (i+7)%8 != 7 and (i+7)//8 != 0:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(turn):
                captures.append(i)
                break
            else:
                break
            i -= 7

        i = selected-9
        while (i+9)%8 != 0 and (i+9)//8 != 0:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(turn):
                captures.append(i)
                break
            else:
                break
            i -= 9

    # Knight for both players
    if game_board[selected][0] == 'N':
        x,y = selected%8,selected//8

        if x >= 2 and y <= 6:   # Check if valid move
            if game_board[(x-2)+(y+1)*8] == None:   # Check if no blocking piece
                moves.append((x-2)+(y+1)*8)
            elif game_board[(x-2)+(y+1)*8][1] != str(turn): # Check if is attacking
                captures.append((x-2)+(y+1)*8)
        if x >= 1 and y <= 5:
            if game_board[(x-1)+(y+2)*8] == None:
                moves.append((x-1)+(y+2)*8)
            elif game_board[(x-1)+(y+2)*8][1] != str(turn):
                captures.append((x-1)+(y+2)*8)

        if x <= 6 and y <= 5:
            if game_board[(x+1)+(y+2)*8] == None:
                moves.append((x+1)+(y+2)*8)
            elif game_board[(x+1)+(y+2)*8][1] != str(turn):
                captures.append((x+1)+(y+2)*8)
        if x <= 5 and y <= 6:
            if game_board[(x+2)+(y+1)*8] == None:
                moves.append((x+2)+(y+1)*8)
            elif game_board[(x+2)+(y+1)*8][1] != str(turn):
                captures.append((x+2)+(y+1)*8)

        if x <= 5 and y >= 1:
            if game_board[(x+2)+(y-1)*8] == None:
                moves.append((x+2)+(y-1)*8)
            elif game_board[(x+2)+(y-1)*8][1] != str(turn):
                captures.append((x+2)+(y-1)*8)
        if x <= 6 and y >= 2:
            if game_board[(x+1)+(y-2)*8] == None:
                moves.append((x+1)+(y-2)*8)
            elif game_board[(x+1)+(y-2)*8][1] != str(turn):
                captures.append((x+1)+(y-2)*8)

        if x >= 1 and y >= 2:
            if game_board[(x-1)+(y-2)*8] == None:
                moves.append((x-1)+(y-2)*8)
            elif game_board[(x-1)+(y-2)*8][1] != str(turn):
                captures.append((x-1)+(y-2)*8)
        if x >= 2 and y >= 1:
            if game_board[(x-2)+(y-1)*8] == None:
                moves.append((x-2)+(y-1)*8)
            elif game_board[(x-2)+(y-1)*8][1] != str(turn):
                captures.append((x-2)+(y-1)*8)

    # King for both players
    if game_board[selected][0] == 'K':
        x,y = selected%8,selected//8
        attacked = attacked_spaces(1+turn%2,game_board)

        if selected == 3 and wcastle%2 == 0 and \
           game_board[1] == None and game_board[2] == None and\
           not 1 in attacked and not 2 in attacked and not 3 in attacked:
            moves.append(1)
        if selected == 3 and -1 < wcastle < 2 and \
           game_board[4] == None and game_board[5] == None and game_board[6] == None and\
           not 3 in attacked and not 4 in attacked and not 5 in attacked:
            moves.append(5)

        if selected == 59 and bcastle%2 == 0 and \
           game_board[58] == None and game_board[57] == None and\
           not 57 in attacked and not 58 in attacked and not 59 in attacked:
            moves.append(57)
        if selected == 59 and -1 < bcastle < 2 and \
           game_board[60] == None and game_board[61] == None and game_board[62] == None and\
           not 59 in attacked and not 60 in attacked and not 61 in attacked:
            moves.append(61)

        if x >= 1 and y <= 6: # Check if valid move
            if game_board[(x-1)+(y+1)*8] == None:   # Check if no blocking piece
                moves.append((x-1)+(y+1)*8)
            elif game_board[(x-1)+(y+1)*8][1] != str(turn): # Check if is attacking
                captures.append((x-1)+(y+1)*8)
        if y <= 6:
            if game_board[x+(y+1)*8] == None:
                moves.append(x+(y+1)*8)
            elif game_board[x+(y+1)*8][1] != str(turn):
                captures.append(x+(y+1)*8)
        if x <= 6 and y <= 6:
            if game_board[(x+1)+(y+1)*8] == None:
                moves.append((x+1)+(y+1)*8)
            elif game_board[(x+1)+(y+1)*8][1] != str(turn):
                captures.append((x+1)+(y+1)*8)
        if x <= 6:
            if game_board[(x+1)+y*8] == None:
                moves.append((x+1)+y*8)
            elif game_board[(x+1)+y*8][1] != str(turn):
                captures.append((x+1)+y*8)
        if x <= 6 and y >= 1:
            if game_board[(x+1)+(y-1)*8] == None:
                moves.append((x+1)+(y-1)*8)
            elif game_board[(x+1)+(y-1)*8][1] != str(turn):
                captures.append((x+1)+(y-1)*8)
        if y >= 1:
            if game_board[x+(y-1)*8] == None:
                moves.append(x+(y-1)*8)
            elif game_board[x+(y-1)*8][1] != str(turn):
                captures.append(x+(y-1)*8)
        if x >= 1 and y >= 1:
            if game_board[(x-1)+(y-1)*8] == None:
                moves.append((x-1)+(y-1)*8)
            elif game_board[(x-1)+(y-1)*8][1] != str(turn):
                captures.append((x-1)+(y-1)*8)
        if x >= 1:
            if game_board[(x-1)+y*8] == None:
                moves.append((x-1)+y*8)
            elif game_board[(x-1)+y*8][1] != str(turn):
                captures.append((x-1)+y*8)

    # Find the player's king
    for i in range(64):
        if game_board[i] != None and game_board[i][0] == 'K' and game_board[i][1] == str(turn):
            break

    # See if a move allows the king to be taken
    t_moves = list(moves)
    for j in t_moves:
        t_game = list(game_board)
        t_game[j] = t_game[selected]
        t_game[selected] = None
        if game_board[selected][0] == 'K':
            i = j
        if i in attacked_spaces(1+turn%2,t_game):
            moves.remove(j)

    # See if a capture allows the king to be taken
    t_captures = list(captures)
    for j in t_captures:
        t_game = list(game_board)
        t_game[j] = t_game[selected]
        t_game[selected] = None
        if game_board[selected][0] == 'K':
            i = j
        if i in attacked_spaces(1+turn%2,t_game):
            captures.remove(j)

def deselect_piece():
    """Deselects the selected piece"""

    global captures,moves,selected

    if selected != None:
        captures = []
        moves = []
        selected = None

def move_piece(destination):
    """Moves the selected piece"""

    global game_board, en_passent, wcastle, bcastle, wcaptured, bcaptured


    if game_board[selected][0] == 'P':
        # En-passent rule activation
        if abs(destination-selected) in (7,9) and en_passent != None and abs(en_passent-destination) == 8:
            game_board[en_passent] = None

        # En-passent rule initiation
        en_passent = None
        if abs(destination-selected) == 16:
            en_passent = destination

        # Open the menu to select promotion
        if destination < 8 and turn == 2:
            open_menu(bpromote_menu)
        if destination > 55 and turn == 1:
            open_menu(wpromote_menu)

    # Deny castling to moved rooks
    if game_board[selected] == 'R1':
        if selected == 0:
            if wcastle == 2: wcastle = -1
            else:            wcastle = 1
        elif selected == 7:
            if wcastle == 1: wcastle = -1
            else:            wcastle = 2
    if game_board[selected] == 'R2':
        if selected == 56:
            if bcastle == 2: bcastle = -1
            else:            bcastle = 1
        elif selected == 63:
            if bcastle == 1: bcastle = -1
            else:            bcastle = 2

    # Activate castling move
    if game_board[selected][0] == 'K' and abs(destination-selected) == 2:
        if destination == 1:
            game_board[2] = 'R1'
            game_board[0] = None
        elif destination == 5:
            game_board[4] = 'R1'
            game_board[7] = None
        elif destination == 61:
            game_board[60] = 'R2'
            game_board[63] = None
        elif destination == 57:
            game_board[58] = 'R2'
            game_board[56] = None

    # Deny castling to moved king
    if game_board[selected] == 'K1':
        wcastle = -1
    if game_board[selected] == 'K2':
        bcastle = -1

    # Add captured piece to list of captured pieces
    if destination in captures:
        if turn == 1:
            if game_board[destination] == None:
                wcaptured.append("P")
            else:
                wcaptured.append(game_board[destination][0])
            wcaptured = sorted(wcaptured,key = lambda x: "PBNRQ".find(x))
        else:
            if game_board[destination] == None:
                bcaptured.append("P")
            else:
                bcaptured.append(game_board[destination][0])
            bcaptured = sorted(bcaptured,key = lambda x: "PBNRQ".find(x))

    game_board[destination] = game_board[selected]
    game_board[selected] = None











class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def setup_game(self, positions, figures):
        """Puts all of the pieces on board"""

        

        turn = 1
        wcastle = 0
        bcastle = 0
        wcaptured = []
        bcaptured = []
        
        for i in range(64):
            game_board[i] = None
                
        for i in range(len(positions)):
            temp1 = positions[i]
            position = temp1[0]-1+(8-temp1[1])*8
            s = figures[i]
            s+=str(temp1[2])
            game_board[position]= s
            
           # print  game_board[5]
            



        
        
    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"/home/student/Desktop/primer1/puzzz2.jpg")

        button = Tkinter.Button(self,text=u"...",
                                command=self.OnButtonClick1)
        button.grid(column=1,row=0)        
        
        button = Tkinter.Button(self,text=u"Click me !",
                                command=self.OnButtonClick2)
        button.grid(column=2,row=0)
        
        button = Tkinter.Button(self,text=u"Click me !",
                                command=self.OnButtonClick3)
        button.grid(column=3,row=1)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"/home/student/Desktop/primer1/puzzz2.jpg")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnButtonClick1(self):
        filename = askopenfilename()
        self.labelVariable.set( filename+" (You clicked the button)" )
        self.entryVariable.set(filename)
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
    def OnButtonClick2(self):

        filepath = self.entryVariable.get()
        img = ImageTk.PhotoImage(Image.open(filepath).resize((200,200)))
        #self.labelVariable.set(img)
        
        w = Label(self, image=img)
        w.photo = img
        w.pack(side = "bottom", fill = "both", expand = "yes")

        w.grid(column=0,row=1,columnspan=2, rowspan=2,sticky='EW')
        positions, figures = chessboard.main(filepath)
        self.setup_game(positions, figures)
        #print positions
        #print figures

       # display_image(img)

    
    def OnButtonClick3(self):
        print game_board[5]
        select_piece(5)
        print moves
        print captures
        
    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('my application')
    app.mainloop()