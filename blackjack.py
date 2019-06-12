import random
Playing = True
suits = ('diamonds','club','Hearts','Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}
class Card:
	def __init__(self,suit,rank):
		self.suit = suit
		self.rank = rank
	def __str__(self):
		return 'the card is ' + self.rank + ' of ' + self.suit
class Deck:
	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit,rank))
	def __str__(self):
		return 'This is a Deck'
	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		dcard = self.deck.pop()
		return dcard

#The deck has been built. 
#receiving the card

class Hand:
	def __init__(self):
		self.cards = []
		self.value = 0
		self.aces = 0
	def add_card(self,card):
		self.cards.append(card)
		self.value += values[card.rank]
		if card.rank == 'Ace':
			self.aces +=1
	def adjust_aces(self):
		while self.value > 21 and self.aces != 0:
			self.value -= 10
			self.aces -= 1

# keeping track of bet

class Chips:
	def __init__(self,total=100):
		self.total = total

		self.bet = 0
	def win_bet(self):
		self.total += self.bet
	def lose_bet(self):
		self.total -=self.bet


def take_bet(chips):
	while True:
		try:
			chips.bet=int(input('How much would you like to bet?'))
		except ValueError:
			print('This has to be a integer')
		else:
			if chips.bet > chips.total:
				print('Overdraw')
			else:
				break
def hit(deck,hand):
	hand.add_card(deck.deal())
	hand.adjust_aces()

def hit_or_stand(deck,hand):
	global Playing
	while True:
		ans = input('Would you like to hit or stand?')
		if ans.lower()[0] == 'h':
			hit(deck,hand)
		elif ans.lower()[0] == 's':
			Playing = False
		else:
			print('Unexpected answer, try again')
			continue
		break 
	
def show_some(player,dealer):
	print('players hand', *player.cards)
	print('dealers hand but first card hidden', dealer.cards[1])		

def show_all(player,dealer):
	print('dealers hand: ', *dealer.cards)
	print(dealer.value)
	print('players hand:', *player.cards)
	print(player.value)

def player_busts(player,dealer,chips):
	print('Player busts!')
	chips.lose_bet()

def player_wins(player,dealer, chips):
	print('player wins!')
	chips.win_bet()

def dealer_busts(player,dealer,chips):
	print('dealer busts!')
	chips.win_bet()

def dealer_wins(player,dealer, chips):
	print('dealer wins!')
	chips.lose_bet()

def push(player,dealer):
	print('is a tie')
player_chips = Chips()
while True:
	#create and shuffle deck
	deck = Deck()
	deck.shuffle()
	#distribute to hand
	player_hand = Hand()
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())
	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())
	# set up chips
	
	#put you bet
	take_bet(player_chips)
	#show cards
	show_some(player_hand,dealer_hand)

	while Playing:
		hit_or_stand(deck,player_hand)
		show_some(player_hand,dealer_hand)

		if player_hand.value > 21:
			player_busts(player_hand,dealer_hand,player_chips)
			break
	if player_hand.value <= 21:
		
		while dealer_hand.value < player_hand.value:
			hit(deck, dealer_hand)
		show_all(player_hand,dealer_hand)
		if dealer_hand.value > 21:
			dealer_busts(player_hand,dealer_hand,player_chips)		
		elif dealer_hand.value > player_hand.value:
			dealer_wins(player_hand,dealer_hand,player_chips)
		elif dealer_hand.value < player_hand.value:
			player_wins(player_hand,dealer_hand,player_chips)
		else:
			push(dealer_hand,player_hand)

	#one round finished, show chips
	print('you have', player_chips.total)
	x=player_chips.total
	# ask for another round

	new_game= input('Would you like to play another game? y or n')
	if new_game[0].lower() == 'y':
		Playing = True
		continue
	else:
		print('Bye')
		break