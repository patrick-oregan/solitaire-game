"""
MATH20621 - Coursework 3
Student name: Patrick O'Regan
"""

def display_state(s, *, clear=False):
    """
    Display the state s

    If 'clear' is set to True, erase previous displayed states
   """
    def colored(r, g, b, text):
        rb,gb,bb=(r+2)/3,(g+2)/3,(b+2)/3
        rd,gd,bd=(r)/1.5,(g)/1.5,(b)/1.5
        return f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m"

    def inverse(text):
        rb,gb,bb=.2,.2,.2
        rd,gd,bd=.8,.8,.8
        return f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m"

    colours = [(1.0, 0.349, 0.369),
               (1.0, 0.573, 0.298),
               (1.0, 0.792, 0.227),
               (0.773, 0.792, 0.188),
               (0.541, 0.788, 0.149),
               (0.322, 0.651, 0.459),
               (0.098, 0.509, 0.769),
               (0.259, 0.404, 0.675),
               (0.416, 0.298, 0.576)]

    n_columns = len(s['stacks'])
    if clear:
        print(chr(27) + "[2J")

    print('\n')
    row = 0
    numrows = max(len(stack) for stack in s['stacks'])
    for row in range(numrows-1,-1,-1):
        for i in range(n_columns):
            num_in_col = len(s['stacks'][i])
            if num_in_col > row:
                val = s['stacks'][i][row]
                if num_in_col == row+1 and s['blocked'][i]:
                    print(inverse(' '+str(val)+' '),end=' ')
                else:
                    if s['complete'][i]:
                        print(colored(*colours[val-1],'   '),end=' ')
                    else:
                        print(colored(*colours[val-1],' '+str(val)+' '),end=' ')
            else:
                print('    ',end='')
        print()
    print(' A   B   C   D   E   F')

def initial_state():
    import random 
    """
    Returns a dictionairy corresponding to the game state at the start of a new 
    game. The cards should be randomly shuffled, allocated six to each stack, and no stack 
    should be marked complete or blocked.
    """
    # Initialising the state 
    state = {}
    state['blocked'] = [False, False, False, False, False, False]
    state['complete'] = [False, False, False, False, False, False]
    state['stacks'] = [[], 
                        [],
                        [],
                        [],
                        [],
                        []]
    
    numbers = [i for i in range(1, 10)] * 4   # generating the 36 cards, 4 lots of numbers 1-9
    random.shuffle(numbers)   # randomising the order of the numbers
    
    # Assigning these random numbers into 6 stacks 
    for i in range (6):
        while len(state['stacks'][i]) < 6:   # fills the stack until it has 6 numbers in it
            state['stacks'][i].append(numbers[0])  
            numbers.remove(numbers[0])   # removes the number that was added to the sets 
    return state  

def parse_move(input_str):
    """
    Takes the user input string such as ("AD4") and the function interprets this as moving 4 
    cards from A (i.e. 0) to D (i.e. 3). If no integer is followed by AD then assume 1. 
    It returns this as a tuple of e.g. (0, 3, 4)
    """ 
    # Q7 Resetting the game: 
    if input_str == 'R' or input_str == 'r':
        return 0
    
    # Q8 Undoing moves:
    if input_str == 'U' or input_str == 'u':
        return -1
    
    # Q6 Error catching:   
    # Raise Error if the length of the string inputted is not 2 or 3 
    if len(input_str) != 2 and len(input_str) != 3:
        raise ValueError
        
    # Raise Error if the there is a third character that is not a positive integer
    if len(input_str) == 3: 
        if input_str[2].isnumeric() == False or input_str[2] == "0":
            raise ValueError
            
    # Raise Error if the first 2 characters are not letters
    if input_str[0].isalpha() == False or input_str[1].isalpha() == False:
        raise ValueError
        
    # Raise Error if either of these letters are not within A-F
    if input_str[0] not in "ABCDEF" or input_str[1] not in "ABCDEF":
        raise ValueError

    # Code that converts letters A-F to numbers 0-5 respectively
    letter_to_index = {letter: index for index, letter in enumerate("ABCDEF")} 
    # Interpretting the user input and converting the first 2 characters from letter to number 
    source_stack = letter_to_index[input_str[0]]
    destination_stack = letter_to_index[input_str[1]]
    
    # Checks the size of input_str. If it is 3 then number of cards moved has been 
    # defined by the user, otherwise default is 1
    number_of_cards = int(input_str[2] if len(input_str) == 3 else 1)
    # Defining our move tuple that we want to output
    move = (source_stack, destination_stack, number_of_cards)
    return move

def validate_move(state, move):
    """
    Validates the move - returns true if the move 'move' can be applied to a game in state 
    'state'. This function involves all the logic for checking whether a move is valid, 
    including all the rules as stated on Blackboard. Also check for moves that are nonsensical
    """
    a = state['stacks'][move[0]]   # the source stack 
    b = state['stacks'][move[1]]   # the destination stack
    c = a[len(a) - move[2]:len(a)]   # the cards that are moving
    d = b[len(b) - 1] if b != [] else 0   # the value of the top of the destination stack
        
    # Checks that the size of source_stack is not < number_of_cards
    if len(state['stacks'][move[0]]) < move[2]:
        return False

    # Checks that the source_stack is not complete
    if state['complete'][move[0]] == True:
        return False
    
    # Checks that the user has entered 2 different letters
    if move[0] == move[1]:
        return False 

    # Checks that destination_stack is not block nor complete 
    if state['blocked'][move[1]] == True or state['complete'][move[1]] == True:
        return False
    
    # If moving from a blocked stack, must be a valid move
    if state['blocked'][move[0]] == True:
        if d == 0:   # Any move to an empty stack is valid (assuming the cards moving are consecutive)
            pass
        elif len(c) != 1 or c[0] != d - 1:
            return False
        
    # Rule that a 9 must move to an empty stack or be a blocking move 
    if c[0] == 9:
        if len(c) == 1:
            pass
        elif len(b) != 0:
            return False
    
    # This code checks that the cards in c are consecutive. If len(c) = 1 then this includes 
    # moving single cards and blocking moves, both which are valid
    if len(c) > 1:
        for z in range (len(c) - 1):
            if c[z] - 1 != c[z + 1]:
                return False
        # Any move to an empty stack is valid (assuming the cards moving are consecutive)
        if d == 0:   
            pass
        # c[0] i.e. the 'bottom' of the set of cards you are moving must be one less than the top 
        # of the destination stack - otherwise, returns False
        elif c[0] != d - 1:   
            return False
    return True

def apply_move(state, move):
    """
    Takes a valid game state 'state' and move tuple 'move'. The function doesn't return anything  
    but modifies in-place the 'state' parameter passed to it to apply the move described by the
    'move' tuple. You can assume that state is a valid game state and that move is a valid move
    that could be played in this state. This function should update the blocked and complete 
    fields of the game state state, as well as the stacks.
    """ 
    a = state['stacks'][move[0]]   # the source stack 
    b = state['stacks'][move[1]]   # the destination stack
    c = a[len(a) - move[2]:len(a)]   # the cards that are moving
    d = b[len(b) - 1] if b != [] else 0   # the value of the top of the destination stack
    
    # Defining a block move and therefore stack
    if len(c) == 1:
        if b == []:
            pass
        # This is saying if the single card that is moving, is not 1 less than the card it is moving
        # to, and the destination stack is not empty, then this destination stack is now blocked
        elif c[0] != d - 1 and d != 0:  
            state['blocked'][move[1]] = True
            
    b += c   # this adds the cards that are moving to the destination stack 
    a = a[:(len(a) - move[2])]   # a is stored as the new source stack so,
    state['stacks'][move[0]] = a   # we have to update the source stack to be a 
    
    # Unblocking the previously blocked stack
    if state['blocked'][move[0]] == True:
        state['blocked'][move[0]] = False
        
    # Defining a complete stack
    if b == [9, 8, 7, 6, 5, 4, 3, 2, 1]:
        state['complete'][move[1]] = True

def game_won(state):
    """ 
    Takes a valid game state and returns True if the game has been won (that is, all cards are in 
    a completed stack) and False otherwise.
    """ 
    return sum(state['complete']) >= 4

def play_game():
    """ 
    """ 
    # When we start the game,
    board = initial_state()
    moves = {}   # creating our empty dictionary of the moves made 
    try:
        while True: 
            # Display the current game state
            display_state(board, clear=False)

            # Read input from the user.
            # (Do not alter this line, even in questions 6, 7, 8.)

            # Continues to ask the user for an input until their move doesn't raise a ValueError
            while True:
                try:
                    # Read input from the user.
                    # (Do not alter this line, even in questions 6, 7, 8.)
                    move_str = input()
                    
                    # Parse the text typed by the user and convert it to a move
                    move = parse_move(move_str)
                    
                    break  # Exit the loop if parse_move succeeds
                except ValueError:
                    print("Invalid move. Please try again.")   # ask the user to enter a valid move
    
            if move == 0:
                board = initial_state()
                moves.clear()  # clear move history after reset
                continue  # restart the game loop
                
            if move == -1:   
                if len(moves) == 0:   # when there are no moves left to undo
                    print("The board is back to it's original state, you cannot undo any more moves")
                    pass
                
                else:
                    # this while loops goes through the keys of the dictionary and selects the last item 
                    i = 0
                    while i in moves.keys():
                        i += 1
                    last_move = moves.pop(i-1)   # returns and removes the last item in the dictionary
                    
                    # defining our undo_move by swapping the destination and source stack 
                    undo_move = (last_move[1], last_move[0], last_move[2])
                    apply_move(board, undo_move)   # now, undoing our most recent move 
                    
                    board['blocked'][last_move[0]] = last_move[3]   # updating the blocked status of the source stack
                    board['complete'][last_move[0]] = last_move[4]   # updating the complete status of the source stack
                    board['complete'][last_move[1]] = last_move[5]   # updating the complete status of the destination stack
                    
            # If the move was valid...
            elif validate_move(board, move):
                # defining our new variables from the move tuple 
                source = move[0] 
                destination = move[1]
                no_cards = move[2]
                
                # defining our new variables from the blocked and complete status of the previous move
                source_b = board['blocked'][source]
                source_c = board['complete'][source]
                dest_c = board['complete'][destination]
                
                # this while loops goes through the keys of the dictionary and selects the last item 
                i = 0
                while i in moves.keys():
                    i += 1
                
                # We now add a new list to our dictionary containing all these variables we have defined 
                moves.update({i: [source, destination, no_cards, source_b, source_c, dest_c]})
                apply_move(board, move) # ... alter the board  
                
            # If we've won, end the game
            if game_won(board):
                break

    except KeyboardInterrupt: # If the user presses Ctrl-C, quit
        pass

play_game()

