# Mini-project #6 - Blackjack

import simplegui
import random

# load logo img from WEB
BJ_LOGO = simplegui.load_image("https://dl.dropbox.com/s/v2oeg00en42o7gh/blackjack_logo.png?dl=0")

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False											# indicates the game state
outcome = []											# list of prompts for player
score = 0												# beginer score

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):							
        if (suit in SUITS) and (rank in RANKS):		#check if suit&rank in deck	
            self.suit = suit						
            self.rank = rank						
        else:										#if not: 
            self.suit = None						#assign value 'None'
            self.rank = None						#assign value 'None'
            print "Invalid card: ", suit, rank		#prints caution

    def __str__(self):
        return self.suit + self.rank				#prints pair 'suit&rank' letter

    def get_suit(self):								#gets suit for 'Hand' class
        return self.suit

    def get_rank(self):								#gets rank for 'Hand' class
        return self.rank

    def draw(self, canvas, pos):					#draws the card in carent possition 'pos'
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, 
               [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []									# create Hand object (list) to collect cards
        
    def __str__(self):									# prints hand in the console            
        prnt = 'Hand contains:'
        for i in range(len(self.hand)):
            prnt += ' ' + str (self.hand[i])
        return prnt
    
    def add_card(self, card):
        self.hand.append(card)							# add a card object to a hand list

    def get_value(self):
        # count aces as 1, if the hand has an ace,
        # then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.value = value_base = 0						#initiates the value variables
        ranks_list = [] 								#list of hand's card rank, for check quontity of 'aces'
        for i in range(len(self.hand)):					#iterates through hand cards list
            rank = Card.get_rank(self.hand[i])			#gets card rank using 'Card' class
            ranks_list += rank 							#adds rank to local list object
            value_base += VALUES[rank]            		#computs values of card using its rank
            if not 'A' in ranks_list:			
                self.value = value_base			
            else:
                if value_base + 10 <= 21:
                    self.value = value_base + 10
                else:
                    self.value = value_base
        return self.value

    def draw(self, canvas, pos):					#draws the cards on hand
#        for i in range(len(self.hand)):
#            self.hand[i].draw(canvas, [pos[0] + i*CARD_SIZE[0]+5, pos[1] + CARD_SIZE[1]])   
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 20
        
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]	                
    
    def shuffle(self):
        # shuffle the deck
        return random.shuffle(self.deck)
        
    def deal_card(self):
        # deal a card object from the deck
        while len (self.deck) > 0:
            return self.deck.pop()	
    
    def __str__(self):								# return a string representing the deck						            
        prnt = 'Deck contains'
        for i in range(len(self.deck)):
            prnt += ' '+str (self.deck[i])
        return prnt

def deal():											#'dael' button handler
    global outcome, in_play, player_hand, dealer_hand, score,color

    if in_play:										#penalty for the game break
        score -=1
        in_play = False
        outcome = ["You've given up!", "New deal?"]	
    else:    
        deck = Deck ()
        player_hand = Hand ()
        dealer_hand = Hand ()
        color = random.choice([1, 3])				#shuffles color of the back side deck
        deck.shuffle ()								#shuffles cards in deck
        player = deck.deal_card()					#deal the card
        player_hand.add_card(player)				#adds card to hand
        dealer = deck.deal_card()					#deal the card
        dealer_hand.add_card(dealer)				#adds card to hand
        player = deck.deal_card()
        player_hand.add_card(player)
        dealer = deck.deal_card()
        dealer_hand.add_card(dealer)
        in_play = True								#assign game state 
        outcome = ['', 'Hit or stand?']				#prompt 
        
def hit():											#'hit' button handler
    global in_play, score, outcome

    deck = Deck ()
    deck.shuffle ()
    # if the hand is in play, hit the player
    if in_play:										#checks is game still in play
        player = deck.deal_card()					#deals one card
        player_hand.add_card(player)        		#adds card to hand
        if player_hand.get_value() > 21: 
            # if busted, assign a message to outcome, update in_play and score
            in_play = False
            score -=1
            outcome = ['You have busted', "New deal?"]
                
def stand():										#'stand' button handler
    global score, outcome, in_play
    deck = Deck ()
    deck.shuffle ()
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    
    if in_play:
        while dealer_hand.get_value() <17:
            dealer = deck.deal_card()
            dealer_hand.add_card(dealer)
        if dealer_hand.get_value() <= 21:
            if dealer_hand.get_value() >= player_hand.get_value(): 
                score -=1
                in_play = False
                outcome = ['You lost!', "New deal?"]
            else:
                score +=1
                in_play = False
                outcome = ['You win!', "New deal?"]
        else:
            score +=1
            in_play = False
            outcome = outcome = ['You win!', "New deal?"]
    else:
        outcome = ['Sorry, game over!', "New deal?"]

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    player_hand.draw(canvas, [55, 400])				#posissions of dwawing player hand		
    dealer_hand.draw(canvas, [55, 196])				#posissions of dwawing dealer hand
                                                    #draws title "Blackjack" on the canvas
    canvas.draw_text('Black Jack', (290, 100), 26, "Black", "sans-serif")
    
    if in_play:										#hides first dealer card
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0]*color, 
                        CARD_BACK_CENTER[1]], CARD_BACK_SIZE, 
                        [54+CARD_BACK_CENTER[0], 196+CARD_BACK_CENTER[1]], CARD_SIZE)
        dealer_val = ""								#if in play hides the hand value
        player_val = ""
    else: 											#shows the hand value
        dealer_val = ': ('+str(dealer_hand.get_value())+')'
        player_val = ': ('+str(player_hand.get_value())+')'
                                                    #draws the game logo
    canvas.draw_image(BJ_LOGO, [300, 147], [600, 294], [300, 90], [300, 147])    
    canvas.draw_text("Dealer"+dealer_val, (56, 180), 26, "Black", "sans-serif")
    canvas.draw_text(str(), (56, 180), 26, "Black", "sans-serif")    
    canvas.draw_text("Player"+player_val, (56, 380), 26, "Black", "sans-serif")
    canvas.draw_text("Score", (480, 180), 26, "Black", "sans-serif")
    canvas.draw_text(str(score), (500, 256), 60, "Black", "sans-serif")
    canvas.draw_text(outcome[0], (300-(len(outcome[0])*22)/2, 344), 50, "Yellow", "sans-serif")
    canvas.draw_text(outcome[1], (300-(len(outcome[1])*13)/2, 540), 26, "White", "sans-serif")
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
