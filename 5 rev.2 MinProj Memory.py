# implementation of card game - Memory

import simplegui
import random
CARD_FACE = ["Red", "Blue", "Yellow", "Lime", "White", "Orange", "Fuchsia","Aqua"]
CARD_BACK = simplegui.load_image("http://clipartzebraz.com//cliparts/silly-clip-art/cliparti1_silly-clip-art_04.jpg")

# helper function to initialize globals
def new_game():
    global turns, exposed, deck, state				#implements global variables
    turns = 0  										#pair counter
    label.set_text("Turns = "+str(turns))			#draws the reset turns score
    state = 0										#exposed cards counter
    deck = range(8)*2								#simulates the two decks of cards
    random.shuffle(deck)							#shuffles decks
    exposed = [False]*16							#initiates the list "closed/exposed deck"

# define event handlers
def mouseclick(pos):
    global state, exposed, turns, card1, card2		#implements global variables
    idx = pos[0]//50                   				#determine index clicked card
    if exposed[idx] == False:						#compares, is chosen card already exposed
        if state == 0:								#defines "first turn" actions
            exposed[idx] = True						#makes chosen card exposed
            state = 1								#counts the exposed cards
            card1 = idx								#assigns index to the exposed card1
        elif state == 1:							#defines "second turn" actions
            exposed[idx] = True						#exposes next card
            state = 2								#counts the exposed cards
            turns += 1								#counts the turns
            label.set_text("Turns = "+str(turns))	#draws turns score 
            card2 = idx								#assigns index to the exposed card2
        else:
            if deck[card1] != deck[card2]:			#matches the card1 & card2
                exposed[card1] = False				#flips unpair card1
                exposed[card2] = False				#flips unpair card2
            exposed[idx] = True						#exposed next card
            state = 1								#counts the exposed cards
            card1 = idx								#assigns exposed card index
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card in range(len(deck)):				
        canvas.draw_text(str(deck[card]), 			#draws the deck numbers 
                         [5+card*50, 80], 
                         80, CARD_FACE[deck[card]], 'serif')
        canvas.draw_line([card*50, 0], 				#draws the lines between cards
                         [card*50, 100], 1, 'Blue')
        if exposed[card] == False:
            canvas.draw_image(CARD_BACK,
                              (399//2, 225), 
                              (399, 450), 
                              (card*50+25, 50), 
                              (50, 100))
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)					#draws "Reset" button
label = frame.add_label("Turns = 0")				#draws "0" turn score

# register event handlers
frame.set_mouseclick_handler(mouseclick)			
frame.set_draw_handler(draw)						

# get things rolling
new_game()										#starts the game
frame.start()									#starts the grafics 
