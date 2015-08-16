# Rock-paper-scissors-lizard-Spock template
def number_to_name(number):
    if number == 0:
        number = "rock"
    elif number == 1:
        number = "Spock"
    elif number == 2:
        number = "paper"
    elif number == 3:
        number = "lizard"
    elif number == 4:
        number = "scissors"
    else: 
        print "The computer has rioted and changed the rules of game"
    return number

def name_to_number(name):
    if name == "rock":
        name = 0     
    elif name == "Spock":
        name = 1
    elif name == "paper":
        name = 2
    elif name == "lizard":
        name = 3
    elif name == "scissors":
        name = 4
    else: 
        print "Error, your choise does not match any of the five correct input"
        quit()
    return name

def rpsls(player_choice): 
    print 
    player_choice = raw_input ("Make your choice entering either rock, paper, Spock, lizard or scissors:")
    print "Player chooses:", player_choice
    player_choice=name_to_number(player_choice)
    import random
    comp_number = random.randrange(0,5)
    comp_number = number_to_name(comp_number)
    print "Computer chooses:", comp_number
    quit ()
    
