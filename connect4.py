
import random

def check_move(board, turn, col, pop): #check validity of move. turn refers to player turn/computer turn
    if not 0<=col<=6: return False
    elif pop != True and pop!=False: return False
    if pop == True: #player wants to pop at col
            #check bottom of column not empty so can pop
            if board[col] == 0: #column is empty, nothing to pop
                return False
            else: #column contains a disc, so can pop
                if board[col] == turn:
                    return True # can pop own disc
                else:
                    return False #cannot pop other disc
                
    else: # pop is false, so put chip
            #check top row of column not empty so can put
        row = (len(board)//7)-1 #row index, -1 because index starts at 0
        if board[col+(row*7)] == 0: #topmost in the column is empty
            return True
        else:
            return False

def apply_move(board, turn, col, pop): #assume  move is valid, ie. inputs are correct
    # board is board, turn is player, col is column, pop is remove or no
    row = (len(board)//7 - 1) #highest row index
    boardtemp = board[:] #copies the board and does actions on copied board
    if pop == True:
        for i in range(row):
            boardtemp[col+(i*7)] = boardtemp[col+(7*(i+1))] #moves all values in column by 1 down
        boardtemp[col+(7*row)] = 0 #highest value in column becomes empty/zero
        return boardtemp
                        
    else: #pop is false, put disc
        for i in range(row+1): #will take all row indexes
            if boardtemp[col+(i*7)] == 0:
                boardtemp[col+(i*7)] = turn
                break
        return boardtemp

def check_victory(board, who_played): #used after a turn. whoplayed = whose turn it was last, 1 or 2
    #return 0 if no one win yet, 1 is player1, 2 is player2 or pc
    player1win = 0 #wil be changed to 1 if win
    player2win = 0 #will be changed to 1 if win 
   
    def checkvictory_horizontal(board,player): #player represents who to check
        for x in range(len(board)//7): #x is the row index
            count = 0
            for i in range(x*7,(x+1)*7): #checks each row separately
                if board[i] != player:   #if not player, stop counting, reset counter
                    count = 0
                else:
                    count+=1  #only countss if board[i] is = player
                    if count >3: #checks everytime after adding if count reaches 4 or more
                        break
            if count >3:
                return True #if 4 in a row found, player  win condition satified, return true
                break   #no need to test other rows
        return False 
       
    #vertical 
    def checkvictory_vertical(board,player): #board is thelist, player = 1 or 2, represents who to check
        for i in range(7): # checks 0 to 6 which is column index
            count = 0
            for x in range(len(board)//7): #lists the row indexs
                if board[i+(x*7)] != player: #if not player, reset count
                    count = 0
                else:
                    count += 1    
                    if count >3: #after adding check if count equal or more than 4
                        break
            if count >3:
                return True #player satisfies win condition
                break
        return False #player does not satisfy win condition
    
   
    def checkvictory_diagonal(board,player,direction): #player is the player to be checked,  if 6 top left, if 8 top right
    
        count = 0
        rowMax = len(board) #number of elements in list, can use in range to get all row indexes
        for i in range(rowMax): #goes through all values in the list
            count = 0
            for x in range(i,rowMax,direction): #x will take all values towards top left/right direction      
                if board[x] != player:
                    count = 0
                else:
                    count += 1 #if board[i]==player then count add 1
                    if count > 3: #if 4 or more in the diagonal equal to player
                        break
                    
                if direction == 6:
                    checkextreme = x%7
                else:
                    checkextreme = (x+1)%7
                    
                if checkextreme == 0: #check if board[x] is in either leftmost/rightmost column
                    break #already at rightmost column, any further addition will not be in a diagonal line
            if count > 3:
                 return True #diagonal 4 or more accomplished
                 break #no need test others
            
        return False #if no match for every value 
    
    #finalchecks
    if checkvictory_horizontal(board,1) or checkvictory_vertical(board, 1) or checkvictory_diagonal(board, 1, 6) or checkvictory_diagonal(board, 1, 8):
        player1win = 1
    if checkvictory_horizontal(board,2) or checkvictory_vertical(board, 2) or checkvictory_diagonal(board, 2, 6) or checkvictory_diagonal(board, 2, 8):
        player2win = 1
        
    #conclusion checks  
    if player1win == 1 and player2win == 1:
        if who_played == 1:
            return 2 #player 2 wins
        else:
            return 1
    elif player1win == 1:
        return 1
    elif player2win == 1:
        return 2
    else:
        return 0        
   

def computer_move(board, turn, level): # turn is player, pc will be player 2, level is either 1 or 2
    if turn ==1:
        oppTurn = 2
    else:
        oppTurn = 1

    def level1(): #level 1 computer, fully random
     randCol = random.randint(0,6) #pick a random column
     if board[randCol] ==0 or board[randCol] == oppTurn : #cannot pop, either nothing in column or opponent piece
         if board[randCol+((len(board)//7-1)*7)] ==0: #can place chip
             return randCol,False #will place at column
         else: #cannot pop, cannot place chip
             return level1() #retry another random integer
     else: #can pop
         if board[randCol+((len(board)//7-1)*7)] ==0: #can place chip
             popOrNo = random.randint(1,2) #decide if placechip or pop chip
             if popOrNo == 1:
                 return randCol,True
             else:
                 return randCol,True
         else: #cannot place chip
             return randCol,True
     

        
    
    def horizontal_wincon(board,player): #player represents who to check, for any horizontal 3 in a row, returns winning move if available
                    main = 0 #number of rows not empty, counted from bottom up
                    for x in range(0,len(board), 7): #finds main based on board
                        count = 0
                        
                        for a in range(x,x+7):       
                            if board[a] == 0:
                                count +=1
                        if count == 7: #full row of 0
                            break
                        else:
                            main += 1
                            
                    for x in range(main): #x is the row index, until row == main where any row further up including main is empty
                        count = 0
                        threeinrow = 0
                        countdownList = [] #will hold index X between oXoo, where if X=o then win
                        countdown = 100 #define countdown, value doesnt matter
                        
                        for i in range(x*7,(x+1)*7): #i is position index, checked row by row

                            if board[i] != player:   #if not player, stop counting, reset counter
                                countdown-=1
                                count = 0
                                if countdown == 1:
                                    countdownList.append(i) #hold 
                                    
                                elif countdown == 0: #if in the diagonal, 2 or more mismatch, clear countdownList 
                                    countdownList = []
                                    threeinrow = 0
                            else:
                                count+=1  #only countss if board[i] is = player
                                countdown = 2 # when find a match, start a countdown
                                threeinrow += 1
                                if count == 3: #checks everytime after adding if count reach 3
                                    
                                    if i//7 == (i+1)//7 and board[i+1]== 0: #check if i+1 is in same row as i and if i+1 is empty
                                            
                                            if 0<i+1<=6: #check if in bottommost row
                                                return (i+1)%7,False #returns column and pop=false
                                            elif board[i+1-7]!=0:#if not row 0 ,check space below i+1 is filled(so our piece will be where we want it) 
                                                return (i+1)%7,False #win by putting disc in
                                    
                                    elif ((i+4)//7 != i//7) and   board[i+4]==player and board[(i+4)%7] == player: #check if pop in col before the 3 in row will give win, ensure i+4 not in same row as i AND that the bottomost in column is your disc 
                                        return (i+4)%7,True #return column and pop=True
                                    elif (i+8)//7 == (i//7)+1 and board[i+8]==player and board[(i+8)%7] == player: #check if pop column after 3 in row will win, ensure i+8 is exactly 1 row above i and not 2 or more AND that the bottomost in column is your disc 
                                        return (i+8)%7,True #return column and pop=True
                                
                                elif threeinrow == 3: #if count!=3 then only check threeinrow
                                    if countdownList[0]//7 == 0: #if on bottom row, cannot pop for win, only place
                                        if board[countdownList[0]] == 0: #if the space is empty
                                            return (countdownList[0]),False # return column, pop = False
                                    else: #if not on bottom list
                                        if board[countdownList[0]] == 0 and board[(countdownList[0]-7)]!=0: #check if space empty, directly below space occupied
                                            return (countdownList[0]%7),False
                                        elif board[countdownList[0]+7] ==player and board[(countdownList[0]%7)] == player: #check pop conditions: 1 above is player, and bottommost is player
                                            return (countdownList[0]%7), True
           
        #vertical  
    def vertical_wincon(board,player): #player = 1 or 2,represents who to check; for a vertical 3 in a row column, returns winning move if available
    
        for i in range(7): # i takes values 0 to 6 which is column index                      
            count = 0              
            for x in range(len(board)// 7):
                if 0<=i+(x*7)-7<len(board) and board[i+(x*7)-7]==0: #if space below it is 0, dont need check space
                    break
    
                if board[i+(x*7)] != player: #if not player, reset count
                    count = 0
                else:
                    count += 1    
                    if count == 3: #after adding check if count equal 3
                        if i+(x*7)+7 < len(board) and board[i+(x*7)+7]==0: #row above exists and is empty
                            return i%7,False #return column and pop=false

                
        
       
    def diagonal_wincon(board,player,direction): #player is the player to be checked, direction if 6 ==top left, if 8 ==top right, poptarget=player if checking self, poptarget= opponent if looking to sabotage
            main = 0 #number of rows not empty, counted from bottom up
            count = 0
            rowMax = len(board) #number of elements in list, can use in range to get all row indexes
            count = 0
            for x in range(0,len(board), 7):        
                for a in range(x,x+7):       
                    if board[a] == 0:
                        count +=1
                if count == 7: #full row of 0
    
                    break
                else:
                        main += 1      
            if len(board)-main <=3: #too few lengths for a connect 4
                return
            #since all diagonals start from an edge in the board, we can split into 3 and go diagonally from the edges. This (for i in range) takes all diagonals along the bottom
            for i in range(7): #goes through all column index
                count = 0
                threeinrow = 0
                countdownList = []
                countdown = 100 #define countdown, value doesnt matter
                
                


                   
                for x in range(i,main*7,direction): #x will take all values towards top left/right direction, main limits x from checking rows of zeroes                       
                    
                    if board[x] != player:
                        countdown -= 1
                        count = 0
                        if countdown == 1:
                            countdownList.append(x) #hold value
                            
                        elif countdown == 0: #if in the diagonal, 2 or more mismatch, clear countdownList 
                            countdownList = []
                            threeinrow = 0
                    else: #if board[x] == player
                        count += 1 
                        countdown = 2 # when find a match, start a countdown
                        threeinrow += 1
                        if count == 3: #if 3 in a row, theck diagonal up and diagonal down (either topright and  bottomleft OR topleft and bottomright)
                            if x+direction < len(board): #ensure within range (directionx3 for diagonally down as x is the highest point in the 3 in row diagonal, so to get to new diagonal, minus 3x direction)
                                if (x+direction) // 7 == (x//7)+1: #check that diagonally up exists
                                    
                                    if board[x+direction] == 0 and board[x+direction-7] != 0: #ensure we can place disc on x+direction
                                        return (x+direction)%7,False #return col, pop=false
                                    elif x+direction+7 < len(board) and board[x+direction+7]==player and board[(x+direction)%7]==player: #check if we can win via pop
                                        return (x+direction)%7,True #return col, pop=True
                                    
                            if 0<= x-(3*direction):
                                if (x-(3*direction)) //7 == (x//7)-3: #check it is diagonally down
                                    if x-(3*direction)-7 >= 0 and board[x-(3*direction)-7]!=0 and board[x-(3*direction)]==0: #ensure can put on index (x-3*direction)
                                        return (x-(3*direction))%7,False #return column, pop= false
                                    
                                    elif 0 <= (x-(3*direction)) <= 6 and board[(x-(3*direction))] == 0: #if (x-(3*direction)) is at bottom row and is empty:
                                        return (x-(3*direction)),False
                                    
                                    elif (((x-(3*direction))+7)//7) == ((x//7) -2 )and board[(x-(3*direction))+7] == player and board[(x-(3*direction))%7]==player: #check if pop will give victory
                                        return (x-(3*direction))%7,True#return column,pop=True

                        elif threeinrow == 3: # winning diagonal exists but lacks that 1 space in the middle
                            
                            if (countdownList[0]+7)<len(board) and board[countdownList[0]+7 ] == player and board[countdownList[0]%7]==player :
                                return countdownList[0]%7,True #pop the column in position index == countdownList[0] 
                            elif (countdownList[0]-7)>=0 and board[(countdownList[0]-7)]!=0 and board[countdownList[0]]==0:
                                return countdownList[0]%7,False #place in column containing position index countdownList[0]
                            
                       
                    if direction == 6: #6 is to the top left direciton
                        checkextreme = x%7 #check if in leftmost column
                    else: #direction ==8, to the top right direction
                        checkextreme = (x+1)%7 #check if in rightmost column
                        
                    if checkextreme == 0: #check if board[x] is in either leftmost/rightmost column
                        
                        break #already at left/rightmost column, can stop inner loop, continue with outer loop to the next i value
            
            #starts diagonal from the left edge, only needed if checking to the right diagonal
            if direction == 8:
  
                        
                for i in range(7,main*7,7):  #position indexes starting from left edge, limited by main which tells us which row onwards is all zeroes
                    count = 0
                    threeinrow = 0
                    countdownList = []
                    countdown = 100 #define countdown, value doesnt matter
                    
                    
                    
                    
                    for x in range(i,rowMax,direction): #x will take all values towards top left/right direction      

                        if board[x] != player:
                            countdown -= 1
                            count = 0
                            if countdown == 1:
                                countdownList.append(x) #hold value
                                
                            elif countdown == 0: #if in the diagonal, 2 or more mismatch, clear countdownList 
                                countdownList = []
                                threeinrow = 0
                        else: #if board[x] == player
                            count += 1 
                            countdown = 2 # when find a match, start a countdown
                            threeinrow += 1
                            if count == 3: #if 3 in a row, theck diagonal up and diagonal down (either topright and  bottomleft OR topleft and bottomright)
                                if x+direction < len(board): #ensure within range (directionx3 for diagonally down as x is the highest point in the 3 in row diagonal, so to get to new diagonal, minus 3x direction)
                                    if (x+direction) // 7 == (x//7)+1: #check that diagonally up exists
                                        
                                        if board[x+direction] == 0 and board[x+direction-7] != 0: #ensure we can place disc on x+direction
                                            return (x+direction)%7,False #return col, pop=false
                                        elif x+direction+7 < len(board) and board[x+direction+7]==player and board[(x+direction)%7]==player: #check if we can win via pop
                                            return (x+direction)%7,True #return col, pop=True
                                        
                                if 0<= x-(3*direction):
                                    if (x-(3*direction)) //7 == (x//7)-3: #check it is diagonally down
                                        if x-(3*direction)-7 >= 0 and board[x-(3*direction)-7]!=0 and board[x-(3*direction)]==0: #ensure can put on index (x-3*direction)
                                            return (x-(3*direction))%7,False #return column, pop= false
                                        
                                        elif 0 <= (x-(3*direction)) <= 6 and board[(x-(3*direction))] == 0: #if (x-(3*direction)) is at bottom row and is empty:
                                            return (x-(3*direction)),False
                                        
                                        elif (((x-(3*direction))+7)//7) == ((x//7) -2 )and board[(x-(3*direction))+7] == player and board[(x-(3*direction))%7]==player: #check if pop will give victory
                                            return (x-(3*direction))%7,True#return column,pop=True
    
                            elif threeinrow == 3: # winning diagonal exists but lacks that 1 space in the middle
                                
                                if (countdownList[0]+7)<len(board) and board[countdownList[0]+7 ] == player and board[countdownList[0]%7]==player :
                                    return countdownList[0]%7,True #pop the column in position index == countdownList[0] 
                                elif (countdownList[0]-7)>=0 and board[(countdownList[0]-7)]!=0 and board[countdownList[0]]==0:
                                    return countdownList[0]%7,False #place in column containing position index countdownList[0]
                                
                           
                        if direction == 6: #6 is to the top left direciton
                            checkextreme = x%7 #check if in leftmost column
                        else: #direction ==8, to the top right direction
                            checkextreme = (x+1)%7 #check if in rightmost column
                            
                        if checkextreme == 0: #check if board[x] is in either leftmost/rightmost column
                            
                            break #already at left/rightmost column, can stop inner loop, continue with outer loop to the next i value
            
            #starts diagonals from right edge, only need if checking to the left diagonal
            if direction == 6:
               
                for i in range(13,main*7,7):  #position indexes starting from right edge, limited by main which tells us which row onwards is all zeroes
                    count = 0
                    threeinrow = 0
                    countdownList = []
                    countdown = 100 #define countdown, value doesnt matter
                    for x in range(i,rowMax,direction): #x will take all values towards top left/right direction      
                        
                        
                        
                        if board[x] != player:
                            countdown -= 1
                            count = 0
                            if countdown == 1:
                                countdownList.append(x) #hold value
                                
                            elif countdown == 0: #if in the diagonal, 2 or more mismatch, clear countdownList 
                                countdownList = []
                                threeinrow = 0
                        else: #if board[x] == player
                            count += 1 
                            countdown = 2 # when find a match, start a countdown
                            threeinrow += 1
                            if count == 3: #if 3 in a row, theck diagonal up and diagonal down (either topright and  bottomleft OR topleft and bottomright)
                                if x+direction < len(board): #ensure within range (directionx3 for diagonally down as x is the highest point in the 3 in row diagonal, so to get to new diagonal, minus 3x direction)
                                    if (x+direction) // 7 == (x//7)+1: #check that diagonally up exists
                                        
                                        if board[x+direction] == 0 and board[x+direction-7] != 0: #ensure we can place disc on x+direction
                                            return (x+direction)%7,False #return col, pop=false
                                        elif x+direction+7 < len(board) and board[x+direction+7]==player and board[(x+direction)%7]==player: #check if we can win via pop
                                            return (x+direction)%7,True #return col, pop=True
                                        
                                if 0<= x-(3*direction):
                                    if (x-(3*direction)) //7 == (x//7)-3: #check it is diagonally down
                                        if x-(3*direction)-7 >= 0 and board[x-(3*direction)-7]!=0 and board[x-(3*direction)]==0: #ensure can put on index (x-3*direction)
                                            return (x-(3*direction))%7,False #return column, pop= false
                                        
                                        elif 0 <= (x-(3*direction)) <= 6 and board[(x-(3*direction))] == 0: #if (x-(3*direction)) is at bottom row and is empty:
                                            return (x-(3*direction)),False
                                        
                                        elif (((x-(3*direction))+7)//7) == ((x//7) -2 )and board[(x-(3*direction))+7] == player and board[(x-(3*direction))%7]==player: #check if pop will give victory
                                            return (x-(3*direction))%7,True#return column,pop=True
    
                            elif threeinrow == 3: # winning diagonal exists but lacks that 1 space in the middle
                                
                                if (countdownList[0]+7)<len(board) and board[countdownList[0]+7 ] == player and board[countdownList[0]%7]==player :
                                    return countdownList[0]%7,True #pop the column in position index == countdownList[0] 
                                elif (countdownList[0]-7)>=0 and board[(countdownList[0]-7)]!=0 and board[countdownList[0]]==0:
                                    return countdownList[0]%7,False #place in column containing position index countdownList[0]
                                
                           
                        if direction == 6: #6 is to the top left direciton
                            checkextreme = x%7 #check if in leftmost column
                        else: #direction ==8, to the top right direction
                            checkextreme = (x+1)%7 #check if in rightmost column
                            
                        if checkextreme == 0: #check if board[x] is in either leftmost/rightmost column
                            
                            break #already at left/rightmost column, can stop inner loop, continue with outer loop to the next i value
                            

                
    def level2(): #level 2 computer, if see opp/self 3 in row & can put to block/win, will confirm do so                
        #if can win in 1 move, do said move
        if horizontal_wincon (board, turn) != None or vertical_wincon(board, turn)!= None or diagonal_wincon(board, turn, 6) != None or  diagonal_wincon(board, turn, 8) != None:
            return horizontal_wincon (board, turn) or vertical_wincon(board, turn) or diagonal_wincon(board, turn, 6) or  diagonal_wincon(board, turn, 8)
                
        
        #if cannot win, then check if can sabotage opponent moves
        elif horizontal_wincon(board,oppTurn) != None and horizontal_wincon(board,oppTurn)[1] == False: #opp can place a chip to win via horizontal connect4                      
           return horizontal_wincon(board,oppTurn)
        elif vertical_wincon(board, oppTurn) != None and vertical_wincon(board,oppTurn)[1] == False: #opp can place chip to ger vertical connect 4    
           return vertical_wincon(board, oppTurn)
        elif diagonal_wincon(board, oppTurn, 6) != None and diagonal_wincon(board, oppTurn, 6)[1] == False:        
           return diagonal_wincon(board, oppTurn, 6)
        elif diagonal_wincon(board, oppTurn, 8) != None and diagonal_wincon(board, oppTurn, 8)[1] ==False: 
            return diagonal_wincon(board, oppTurn, 8)
            
        #if not then do random move
        else:
            
            level1()
    
    if level == 1:
        return level1()
    elif level == 2:
        
        return level2()

def display_board(board):
    row = len(board)//7-1 
    print("Board:")
    for i in range(row,-1,-1): #print from last to first, as first 7 elements are bottommost row
        if i >-1:
            print(board[i*7:(i+1)*7]) 
            
def menu():
    print("Welcome to a game of Connect 4: Pop Out edition!")
    player_choice = 0 
     
    while player_choice != 1 and player_choice != 2: #player's choice whether to play with another person or with computer
        try: #ensures that player can only enter valid inputs
            player_choice = int(input("Enter 1 to play against another player, or 2 to play against a computer:"))
            
        except:
            print()
            print('Please input either 1 or 2')
    
    if player_choice == 1:
        print()
        print('You have chosen to play against another player')
    else:
        print()
        print('You have chosen to play against a computer')
        print()
        level = 0
        while level != 1 and level!= 2:  #selecting difficulty level of computer
            try: #prevents invalid inputs
                level= int(input('Select your difficulty level: Level 1 (easy) or 2(normal)?'))
            except:
                print()
                print('Please enter a valid number,1 or 2')
                
    
    if player_choice == 2:
        print()
        print('You will start first and be player 1')
        print('The computer will be player 2')
    else:
        print()
        print('Player 1 will start first')
        
    row = 0 
    while row <= 0:
        try: #allow user to customise row size, only valid inputs taken
            row = int(input('How many rows do you want the game board to be? Please enter a positive integer more than 0:'))
        except:
            print("Invalid input.")
            
    #initialise the board
    board = []
    for i in range(row*7):
        board.append(0)
    
    print("Board:")
    display_board(board)
    
    winnerfound = 0
    
    
    
    
    
    while winnerfound != 1 and winnerfound != 2: #while victor not found, 1 if player1 wins, 2 if player2 wins
        turn = 1 #player 1's turn
        pop = 10
        col = 10
        print()
        print('Player 1\'s Turn')
        while check_move(board, turn, col, pop) == False:
            
            while not 0<=col<=6: #user input on column to put
                try:
                   col = int(input('Which column (0 - 6) do you pick:'))
                except:
                   print('Please enter a valid input')
                   
            while pop!=0 and pop != 1: #user input on pop or not
                try:
                    pop = int(input('Do you want to pop a disc or place a disc? Enter 1 if pop, enter 0 if placing:'))
                except:
                    print('Please enter a valid input')
            if check_move(board, turn, col, pop) == True:
                break
            else:
                print('Error! You can only pop out your own disc! You also cant pop if you have no discs!')
                pop = 10
                col = 10
        board = apply_move(board, turn, col, pop)
        
        display_board(board)
        if check_victory(board, turn) ==1 :
            winnerfound = 1
            break
        elif check_victory(board, turn)== 2:
            winnerfound = 2
            break
            
        turn = 2
        print()
        print("Player 2's Turn:")
        if player_choice == 1:#player2 turn
            pop = 10
            col = 10
            while check_move(board, turn, col, pop) == False:
                
                while not 0<=col<=6: #user input on column to put
                    try:
                       col = int(input('Which column (0 - 6) do you pick:'))
                    except:
                       print('Please enter a valid input')
                       
                while pop!=0 and pop != 1: #user input on pop or not
                    try:
                        pop = int(input('Do you want to pop a disc or place a disc? Enter 1 if pop, enter 0 if placing:'))
                    except:
                        print('Please enter a valid input')
                if check_move(board, turn, col, pop) == True:
                    break
                else:
                    print('Error! You can only pop out your own disc! You also cant pop if you have no discs!')
                    pop = 10
                    col = 10
            
        elif player_choice == 2: #computer turn
            pop = 10
            col = 10
            if level == 1:
                while True:
                    
                    if computer_move(board, turn, level) != None: #if there is a valid move
                        col = computer_move(board, turn, level)[0]
                        pop = computer_move(board, turn, level)[1]
                        if check_move(board,turn,col,pop) == True: #exit the checkmove cycle
                            break
                    else:
                        pop =10 #reset pop and colvalues
                        col=10
            else: #level 2
                while True:
                    if type(computer_move(board, turn, level)) == tuple: #if there is a valid move
                        col = computer_move(board, 2, level)[0]
                        pop = computer_move(board, 2, level)[1]
                        if check_move(board, 2, col, pop) == True:
                            break
                    else:
                        col = computer_move(board, turn, 1)[0]
                        pop = computer_move(board, turn, 1)[1]
                        break
        
        board = apply_move(board, turn, col, pop)
        display_board(board)
        if check_victory(board, turn) ==1 :
            winnerfound = 1
            break
        elif check_victory(board, turn)== 2:
            winnerfound = 2
            break
    
    
    
    print("Victory!")
    if player_choice ==1:
        print("Player",winnerfound,"is the winner!")
    elif winnerfound ==1:
        print('You are the winner!')
    else:
        print('Computer has won!')
        
    print("The game has ended")
    print("Goodbye")




if __name__ == "__main__":
    menu()




    
