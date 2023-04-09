###########################################################
#  Computer Project #10
#  Algorithm
#    Define functions to initialize program, display program, and all other functions using only local variables
#    Declare all constants and variables needed
#    Prompt user to input an option
#    loop while the user choice is not 'Q'
#       re-prompt user for correct input
#       If User choice is TT
#          Call the tableau to tableau function and do operstions on it
#          output the display
#       if user choice is TF
#          Call the tableau to foundation function and check if user won
#       If user option is WT
#           Call the waste to tableau function and display board
#       If user option is WF
#           Call the waste to foundation funtion and display the board
#       If user option is SW
#           Call the stock to waste function and diplay the board
#      If user option is R
#           Initialize the game again to restart it and display board
#       If user option is  H display menu
# If user option is Q
#
#           If use
#               Quit program
###########################################################
from cards import Card, Deck

MENU = '''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    TT s d: Move card from end of Tableau pile s to end of pile d.
    TF s d: Move card from end of Tableau pile s to Foundation d.
    WT d: Move card from Waste to Tableau pile d.
    WF d: Move card from Waste to Foundation pile d.
    SW : Move card from Stock to Waste.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''


def initialize():
    '''Builds the tableau, stock, foundation and waste(talon) by instantiating the Deck class. This function takes no arguments and returns the tableau, stock, foundation and waste
    '''
    my_deck = Deck()  # instantiates the Deck class
    foundation = [[], [], [], []]
    tableau = [[], [], [], [], [], [], []]
    # Fills a 7 x 7 table with None
    for list_ in tableau:
        for item in range(7):
            list_.append(None)

    for row, _lst in enumerate(tableau):
        for column, element in enumerate(_lst):
            if column < row:
                continue
            elif column >= row:
                # Deals a card into each column
                tableau[row][column] = my_deck.deal()

    tableau_ = []

    for card_tuple in zip(*tableau):
        tableau_.append(list(card_tuple))

    ultimate_tableau = [[card for card in row if card != None] for row in tableau_]
    # Flips last card face up and adds to the ultimate_tableau and turns all other cards face down
    for r, list_ in enumerate(ultimate_tableau):
        for c, element in enumerate(list_):
            if c != (len(list_) - 1):
                ultimate_tableau[r][c].flip_card()
    stock = my_deck
    waste = [stock.deal()]

    return ultimate_tableau, stock, foundation, waste


def display(tableau, stock, foundation, waste):
    """ display the game setup """
    stock_top_card = "empty"
    found_top_cards = ["empty", "empty", "empty", "empty"]
    waste_top_card = "empty"
    if len(waste):
        waste_top_card = waste[-1]
    if len(stock):
        stock_top_card = "XX"  # stock[-1]
    for i in range(4):
        if len(foundation[i]):
            found_top_cards[i] = foundation[i][-1]
    print()
    print("{:5s} {:5s} \t\t\t\t\t {}".format("stock", "waste", "foundation"))
    print("\t\t\t\t     ", end='')
    for i in range(4):
        print(" {:5d} ".format(i + 1), end='')
    print()
    print("{:5s} {:5s} \t\t\t\t".format(str(stock_top_card), str(waste_top_card)), end="")
    for i in found_top_cards:
        print(" {:5s} ".format(str(i)), end="")
    print()
    print()
    print()
    print()
    print("\t\t\t\t\t{}".format("tableau"))
    print("\t\t ", end='')
    for i in range(7):
        print(" {:5d} ".format(i + 1), end='')
    print()
    # calculate length of longest tableau column
    max_length = max([len(stack) for stack in tableau])
    for i in range(max_length):
        print("\t\t    ", end='')
        for tab_list in tableau:
            # print card if it exists, else print blank
            try:
                print(" {:5s} ".format(str(tab_list[i])), end='')
            except IndexError:
                print(" {:5s} ".format(''), end='')
        print()
    print()


def stock_to_waste(stock, waste):
    '''Moves card from the stock to waste. Takes stock and waste as arguments and returns a boolean which checks if move from stock to waste is possible'''
    try:
        # Checks to see if the stock is empty
        if not stock.is_empty():
            s = stock.deal()
            if not s.is_face_up():
                s.flip_card()
            waste.append(s)
            return True
        else:
            return False
    except IndexError:
        return False


def color_check(card):
    black_c = [1, 4]
    red_c = [2, 3]
    if card.suit() in black_c:
        return 'B'

    return 'R'


def waste_to_tableau(waste, tableau, t_num):
    '''Moves card from the waste to the tableau. Takes waste(list), tableau and user number as arguments and returns a boolean which checks if move from waste to tableau is possible'''
    try:
        if waste:
            # Accesses the last card in the waste list
            s_card = waste[-1]
            if tableau[t_num]:
                dest_card = tableau[t_num][-1]
                # Uses my built function to check for the color of the card
                if (s_card.rank() + 1 == dest_card.rank()) and color_check(s_card) != color_check(dest_card):
                    s_card = waste.pop()
                    # Flip card face up in case card is not face up
                    if not s_card.is_face_up():
                        s_card.flip_card()
                    tableau[t_num].append(s_card)
                    return True
            else:
                # Add King to tableau column if column is empty
                if s_card.rank() == 13:
                    s_card = waste.pop()

                    if not s_card.is_face_up():
                        s_card.flip_card()
                    tableau[t_num].append(s_card)
                    return True
        return False
    except IndexError:
        return False


def waste_to_foundation(waste, foundation, f_num):
    '''Moves card from the waste to the function. Takes waste(list) foundation and user number as arguments and returns a boolean which checks if move from waste to foundation is possible'''
    try:
        if waste:
            s_card = waste[-1]
            if foundation[f_num]:
                dest_card = foundation[f_num][-1]

                if (s_card.rank() - 1 == dest_card.rank()) and s_card.suit() == dest_card.suit():
                    s_card = waste.pop()

                    if not s_card.is_face_up():
                        s_card.flip_card()
                    foundation[f_num].append(s_card)
                    return True
            else:
                # Adds the Ace as the first card in the foundation
                if s_card.rank() == 1:  # is Ace
                    s_card = waste.pop()
                    # Turns card face up
                    if not s_card.is_face_up():
                        s_card.flip_card()
                    foundation[f_num].append(s_card)
                    return True
        return False
    except IndexError:
        return False


def tableau_to_foundation(tableau, foundation, t_num, f_num):
    '''Moves card from the tableau to the foundation(list). Takes foundation(list) tableau and 2 user numbers as arguments and returns a boolean which checks if move from tableau to foundation is possible'''
    try:
        if tableau[t_num]:
            s_card = tableau[t_num][-1]
            if foundation[f_num]:
                dest_card = foundation[f_num][-1]

                if (s_card.rank() - 1 == dest_card.rank()) and s_card.suit() == dest_card.suit():
                    s_card = tableau[t_num].pop()

                    if not s_card.is_face_up():
                        s_card.flip_card()
                    foundation[f_num].append(s_card)

                    if tableau[t_num] and not tableau[t_num][-1].is_face_up():
                        tableau[t_num][-1].flip_card()

                    return True
            else:
                if s_card.rank() == 1:  # is Ace
                    s_card = tableau[t_num].pop()

                    if not s_card.is_face_up():
                        s_card.flip_card()
                    foundation[f_num].append(s_card)

                    if tableau[t_num] and not tableau[t_num][-1].is_face_up():
                        tableau[t_num][-1].flip_card()

                    return True
        return False
    except IndexError:
        return False


def tableau_to_tableau(tableau, t_num1, t_num2):
    '''Moves card from the tableau to the tableau. Takes tableau , and 2 user numbers as arguments and returns a boolean which checks if move from tableau to tableau is possible'''
    try:
        if tableau[t_num1]:
            # Acesses sources card and destination cards
            s_card = tableau[t_num1][-1]
            if tableau[t_num2]:
                dest_card = tableau[t_num2][-1]

                if (s_card.rank() == dest_card.rank() - 1) and color_check(s_card) != color_check(dest_card):
                    s_card = tableau[t_num1].pop()

                    if not s_card.is_face_up():
                        s_card.flip_card()
                    tableau[t_num2].append(s_card)

                    if tableau[t_num1] and not tableau[t_num1][-1].is_face_up():
                        tableau[t_num1][-1].flip_card()

                    return True
            else:
                # Adds King to empty columns in tableau
                if s_card.rank() == 13:
                    s_card = tableau[t_num1].pop()

                    if not s_card.is_face_up():
                        s_card.flip_card()
                    tableau[t_num2].append(s_card)

                    if tableau[t_num1] and not tableau[t_num1][-1].is_face_up():
                        tableau[t_num1][-1].flip_card()

                    return True

        return False
    except:
        return False


def check_win(stock, waste, foundation, tableau):
    '''Checks if foundation is full and tableau and stock is empty to declare if user won the game. Takes stock, waste, foundation and tableau as arguments and returns a boolean'''
    new_foundation = [c for r in foundation for c in r]
    new_tableau = [c for r in tableau for c in r]
    return stock.is_empty() and (not waste) and (len(new_tableau) == 0) and (len(new_foundation) == 52)


def parse_option(in_str):
    '''Prompt the user for an option and check that the input has the
           form requested in the menu, printing an error message, if not.
           Return:
        TT s d: Move card from end of Tableau pile s to end of pile d.
        TF s d: Move card from end of Tableau pile s to Foundation d.
        WT d: Move card from Waste to Tableau pile d.
        WF d: Move card from Waste to Foundation pile d.
        SW : Move card from Stock to Waste.
        R: Restart the game (after shuffling)
        H: Display this menu of choices
        Q: Quit the game
        '''
    option_list = in_str.strip().split()

    opt_char = option_list[0][0].upper()

    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]

    if opt_char == 'S' and len(option_list) == 1:
        if option_list[0].upper() == 'SW':
            return ['SW']

    if opt_char == 'W' and len(option_list) == 2:
        if option_list[0].upper() == 'WT' or option_list[0].upper() == 'WF':
            dest = option_list[1]
            if dest.isdigit():
                dest = int(dest)
                if option_list[0].upper() == 'WT' and (dest < 1 or dest > 7):
                    print("\nError in Destination")
                    return None
                if option_list[0].upper() == 'WF' and (dest < 1 or dest > 4):
                    print("\nError in Destination")
                    return None
                opt_str = option_list[0].strip().upper()
                return [opt_str, dest]

    if opt_char == 'T' and len(option_list) == 3 and option_list[1].isdigit() \
            and option_list[2].isdigit():
        opt_str = option_list[0].strip().upper()
        if opt_str in ['TT', 'TF']:
            source = int(option_list[1])
            dest = int(option_list[2])
            # check for valid source values
            if opt_str in ['TT', 'TF'] and (source < 1 or source > 7):
                print("\nError in Source.")
                return None
            # elif opt_str == 'MFT' and (source < 0 or source > 3):
            # print("Error in Source.")
            # return None
            # source values are valid
            # check for valid destination values
            if (opt_str == 'TT' and (dest < 1 or dest > 7)) \
                    or (opt_str == 'TF' and (dest < 1 or dest > 4)):
                print("\nError in Destination")
                return None
            return [opt_str, source, dest]

    print("\nError in option:", in_str)
    return None  # none of the above


def main():
    print(MENU)
    # Declares various variables and displays the tableau and other paramenters
    tableau, stock, foundation, waste = initialize()
    display(tableau, stock, foundation, waste)
    # Takes user input for options
    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
    user_input = parse_option(user_input)

    while user_input == None:
        # Prompts user till valid option is entered
        display(tableau, stock, foundation, waste)
        user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
        user_input = parse_option(user_input)

    while user_input != ['Q']:
        if user_input[0] == 'TT':
            # Gets the index position for the columns in the tableau
            user_num1 = (user_input[1] - 1)
            user_num2 = (user_input[2] - 1)
            move_completed = tableau_to_tableau(tableau, user_num1, user_num2)
            if move_completed:
                display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)
        elif user_input[0] == 'TF':
            # takes user inputs and locates index positions in the tableau
            user_num1 = (user_input[1] - 1)
            user_num2 = (user_input[2] - 1)
            move_completed = tableau_to_foundation(tableau, foundation, user_num1, user_num2)
            if move_completed:
                user_win = check_win(stock, waste, foundation, tableau)
                if user_win:
                    print("You won")
                    display(tableau, stock, foundation, waste)
                    break
                else:
                    display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)
        elif user_input[0] == 'WT':
            user_num = (user_input[1] - 1)
            transfer_completed = waste_to_tableau(waste, tableau, user_num)
            if transfer_completed:
                display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)
        elif user_input[0] == 'WF':
            user_num = (user_input[1] - 1)
            transfer_completed = waste_to_foundation(waste, foundation, user_num)
            if transfer_completed:
                user_win = check_win(stock, waste, foundation, tableau)
                if user_win:
                    # Check if user won the game and leave the program
                    print("You won!")
                    display(tableau, stock, foundation, waste)
                    break
                else:
                    display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)
        elif user_input[0] == 'SW':
            move_success = stock_to_waste(stock, waste)
            if move_success:
                display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)
        elif user_input[0] == 'R':
            tableau, stock, foundation, waste = initialize()
            print(MENU)
            display(tableau, stock, foundation, waste)
        elif user_input[0] == 'H':
            print(MENU)

        user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
        user_input = parse_option(user_input)

        while user_input == None:
            display(tableau, stock, foundation, waste)
            user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
            user_input = parse_option(user_input)


if __name__ == '__main__':
    main()
