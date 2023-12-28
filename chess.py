#2P chess with no En-passant and checking
import pandas as pd

#dictionary
free = '.'

board = [[free for y in range(8)] for x in range(8)]

whitemove = "White plays. Enter move:"
blackmove = "Black plays. Enter move:"
illegalmove = "Illegal move!"

def moves(input, i):
    output = -1
    if input[i] == "a":
        output = 0
    if input[i] == "b":
        output = 1
    if input[i] == "c":
        output = 2
    if input[i] == "d":
        output = 3
    if input[i] == "e":
        output = 4
    if input[i] == "f":
        output = 5
    if input[i] == "g":
        output = 6
    if input[i] == "h":
        output = 7
    return output

#setup
board[7][0] = 'r'
board[7][7] = 'r'
board[7][2] = 'b'
board[7][5] = 'b'
board[0][0] = 'R'
board[0][7] = 'R'
board[0][2] = 'B'
board[0][5] = 'B'
board[7][3] = 'q'
board[7][4] = 'k'
board[0][3] = 'Q'
board[0][4] = 'K'
board[7][1] = 'n'
board[7][6] = 'n'
board[0][1] = 'N'
board[0][6] = 'N'
for i in range(8):
    board[6][i] = 'p'
    board[1][i] = 'P'
blackpieces = ['B','R','Q','K','N','P']
whitepieces = ['b','r','q','k','n','p']

def printboard():
  df = pd.DataFrame(board,columns=list('ABCDEFGH'),index=list('87654321'))
  print(df)
printboard()

gamerunning = True
turn = 0 #even is white to move
while gamerunning:
    
    legalmove = True
    if turn % 2 == 0:
        print(whitemove)
    else:
        print(blackmove)
    #enter moves as a 4-tuple, e.g. c5d2
    userinput = input()

    #check for and convert valid tuples
    if len(userinput) != 4:
      print(illegalmove)
      legalmove = False
      continue
        
    x = int(moves(userinput,0))
    w = 8-int(userinput[1])
    z = int(moves(userinput,2))
    y = 8-int(userinput[3])
    if x < 0 or w < 0 or z < 0 or y < 0:
      legalmove = False
    if x == z and w == y:
      legalmove = False
     
    #check for legal moves based on type
      
    #can't pick up nothing
    if board[w][x] == free:
      legalmove = False
    #can't pick up someone else's piece, can't target your own piece
    if turn%2 == 0: #for white
      if board[w][x] in blackpieces:
        legalmove = False
      if board[y][z] in whitepieces:
        legalmove = False
    if turn%2 == 1: #for black
      if board[w][x] in whitepieces:
        legalmove = False
      if board[y][z] in blackpieces:
        legalmove = False
    
    #queen needs to be checked first
    horizontal = False
    diagonal = False
    if board[w][x].lower() == 'q':
        if w == y or x == z:
            horizontal = True
        if (w-y)*(w-y) == (z-x)*(z-x):
            diagonal = True
        if horizontal == False and diagonal == False:
            legalmove = False
        
    if board[w][x].lower() == 'r' or horizontal == True: #rook or queen
      if w != y and x != z:
        legalmove = False
      if w < y:
        for i in range(1,y-w):
          if board[w+i][x] != free:
            legalmove = False
      if y < w:
        for i in range(1,w-y):
          if board[y+i][x] != free:
            legalmove = False
      if x < z:
        for i in range(1,z-x):
          if board[w][x+i] != free:
            legalmove = False
      if z < x:
        for i in range(1,x-z):
          if board[w][z+i] != free:
            legalmove = False

    #knight
    if board[w][x].lower() == 'n':
        if not (((w-y)*(w-y)==4 and (x-z)*(x-z)==1) or ((w-y)*(w-y)==1 and (x-z)*(x-z)==4)):
            legalmove = False
    
    if board[w][x].lower() == 'b' or diagonal == True: #bishop or queen
        if (w-y)*(w-y) != (x-z)*(x-z):
            legalmove = False
        if w < y:
            if x < z:
                for i in range(1, y-w):
                    if board[w+i][x+i] != free:
                        legalmove = False
            if z < x:
                for i in range(1, y-w):
                    if board[w+i][z+i] != free:
                        legalmove = False
        if w > y:
            if x < z:
                for i in range(1, y-w):
                    if board[y+i][x+i] != free:
                        legalmove = False
            if z < x:
                for i in range(1, y-w):
                    if board[y+i][z+i] != free:
                        legalmove = False

    #pawn white
    if board[w][x] == 'p':
        if w <= y:
            legalmove = False
        if (x-z)*(x-z) > 1:
            legalmove = False
        if w != 6 and w-y > 1:
            legalmove = False
        if w-y > 2:
            legalmove = False
        if w-y == 2 and x != z:
            legalmove = False
        if w-y == 1 and (x-z)*(x-z) == 1:
            if board[y][z] == free:
                legalmove = False
        if w-y == 1 and x==z:
            if board[y][z] != free:
                legalmove = False
        if w-y == 2:
            if board[y][z] != free or board[y+1][z] != free:
                legalmove = False

    #pawn black
    if board[w][x] == 'P':
        if w >= y:
            legalmove = False
        if (x-z)*(x-z) > 1:
            legalmove = False
        if w != 1 and y-w > 1:
            legalmove = False
        if y-w > 2:
            legalmove = False
        if y-w == 2 and x != z:
            legalmove = False
        if y-w == 1 and (x-z)*(x-z) == 1:
            if board[y][z] == free:
                legalmove = False
        if y-w == 1 and x==z:
            if board[y][z] != free:
                legalmove = False
        if y-w == 2:
            if board[w+1][z] != free or board[w+2][z] != free:
                legalmove = False
        
    #king, and castling
    if board[w][x].lower() == 'k':
        if (w-y)*(w-y) > 1 or (x-z)*(x-z) > 1:
            legalmove = False
    if board[w][x] == 'k':
        if w == 7 and x == 4 and y == 7 and z == 6: #white king side
            if board[7][7] == 'r':
                if board[7][5] == free and board[7][6] == free:
                    board[7][5] = 'r'
                    board[7][7] = free
                    legalmove = True
        if w == 7 and x == 4 and y == 7 and z == 2: #white queen side
            if board[7][0] == 'r':
                if board[7][1] == free and board[7][2] == free and board[7][3] == free:
                    board[7][3] = 'r'
                    board[7][0] = free
                    legalmove = True
    if board[w][x] == 'K':
        if w == 0 and x == 4 and y == 0 and z == 6: #black king side
            if board[0][7] == 'R':
                if board[0][5] == free and board[0][6] == free:
                    board[0][5] = 'R'
                    board[0][7] = free
                    legalmove = True
        if w == 0 and x == 4 and y == 0 and z == 2: #black queen side
            if board[0][0] == 'R':
                if board[0][1] == free and board[0][2] == free and board[0][3] == free:
                    board[0][0] = free
                    board[0][3] = 'R'  
                    legalmove = True
              
    #execute the move , or not
    if legalmove == False:
        print(illegalmove)
    if legalmove == True:    
        board[y][z] = board[w][x]
        board[w][x] = free
        printboard()
        turn += 1
        
    #promotion
    for i in range(8):
        if board[0][i] == 'p':
            pro = ''
            while pro == '':
                pro = input("What would you like to promote to? q, b, r, or n?")
                if pro.lower() == 'n':
                    board[0][i] = 'n'
                elif pro.lower() == 'b':
                    board[0][i] = 'b'
                elif pro.lower() == 'r':
                    board[0][i] = 'r'
                elif pro.lower() == 'q':
                    board[0][i] = 'q'
                else:
                    x = ''
            printboard()
    for i in range(8):
        if board[7][i] == 'P':
            pro = ''
            while pro == '':
                pro = input("What would you like to promote to? Q, B, R, or N?")
                if pro.lower() == 'n':
                    board[7][i] = 'N'
                elif pro.lower() == 'b':
                    board[7][i] = 'B'
                elif pro.lower() == 'r':
                    board[7][i] = 'R'
                elif pro.lower() == 'q':
                    board[7][i] = 'Q'
                else:
                    x = ''
            printboard()
    
    king = 0
    KING = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'k':
                king += 1
            if board[i][j] == 'K':
                KING += 1
    if king == 0:
        print("Black wins!")
        gamerunning = False
        continue
    if KING == 0:
        print("White wins!")
        gamerunning = False
        continue