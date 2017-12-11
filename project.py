###basic rule: dealer must draw on 16 and stand on 17###

#cards: just get random choice
#card values:it is up to each individual player if an ace is worth 1 or 11. 
#face cards are 10 and any other card is its pip value.

#dealer
#player (get user's name)
player_name = raw_input("What's your name: ").capitalize()
game_continue = False
dealer_turn = False
frame_line = " "+ "-" * 35

import random
cards = {"A":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}

#receive two cards: for example
#dealer's cards show as */9 (total:9) -->second card face down(hidden by any icon like *)
#player's cards show as 10/5 (total:15)

def card_giving():
    player_card = random.choice(cards.keys()) 
    return player_card

#calculate total score of received cards. "A" counted as "1"
def score_cal(received_cards, total = 0):
    for card_key in received_cards:
        total += cards[card_key]
    return total

#if contains "A", count as 11
def score_cal_aeleven(player_card):
    if "A" not in player_card:
        return score_cal(player_card)
    else:
        return 10 + score_cal(player_card)

#check if it's a count of 21 in two cards
def natural_check(total):
    if total == 21:
        return True
    else:
        return False
        
def bust_check(total):
    if total > 21:
        return True
    else:
        return False

############game main part###############
dealer_card = []
player_card = []

#serving cards at the beginning
for card in range(2):
    dealer_card.append(card_giving())
    player_card.append(card_giving())

dealer_score = score_cal(dealer_card)
player_score = score_cal(player_card)
#dealer's first card should be faced down
dealer_hidden_card = cards[dealer_card[0]]

dealer_score2 = score_cal_aeleven(dealer_card)
player_score2 = score_cal_aeleven(player_card)

def current_stat():
    #if cards contain "A", show two totals
    if "A" in dealer_card[1:]:
        print "Dealer's cards:{}, total:{} or {}".format((["@"] + dealer_card[1:]), (dealer_score - dealer_hidden_card), (dealer_score2 - dealer_hidden_card))
    else:
        print "Dealer's cards:{}, total:{}".format((["@"] + dealer_card[1:]), (dealer_score - dealer_hidden_card))
    
    if "A" in player_card:
        print "{}'s cards:{}, total:{} or {}".format(player_name, player_card, player_score, player_score2)
    else:
        print "{}'s cards:{}, total:{}".format(player_name, player_card, player_score)

current_stat()

####check if blackjack###
#check if both got blackjack(very rare case)
if (natural_check(dealer_score) or natural_check(dealer_score2)) and (natural_check(player_score) or natural_check(player_score2)):
    print "OMG! Both of you and dealer got BlackJack!"
    #game_continue = False
#check if dealer got blackjack
elif natural_check(dealer_score) or natural_check(dealer_score2):
    print "Dealer has Black Jack!!!"
    print "You lose!"
    #game_continue = False
#checki if player got blackjack
elif natural_check(player_score) or natural_check(player_score2):
    print "WOW! Black Jack!!!"
    print "You win!"
    #game_continue = False

else:
    game_continue = True


#player can decide to Hit/Stand
#when player decided to stand -> dealer's turn-> compare the sums -> determine lose or win
#when player decided to hit -> add one card -> calculate the sum
  #if over 21: goes bust ->player loses        
  #if equal to 21: blackjack! -> dealer's turn -> if dealer has no black jack, player wins         
  #if under 21: player can decide to Hit/ Stand --> 
  #----hit: continue the loop
  #----stand:  dealer's turn -> compare the sums -> determine lose or win

while game_continue:
    player_decision = raw_input("You want to stand or hit? [s/h]\n>").lower() 
    if player_decision == "h":
        #add one cand to player's cards
        player_card.append(card_giving())
        
        #update the card total score
        dealer_score = score_cal(dealer_card)
        player_score = score_cal(player_card)
        dealer_score2 = score_cal_aeleven(dealer_card)
        player_score2 = score_cal_aeleven(player_card)
        
        print frame_line
        current_stat()
        print frame_line
        
        if natural_check(player_score) or natural_check(player_score2):
            print "Black Jack!"
            break
        elif bust_check(player_score) or bust_check(player_score2):
            print "I'm sorry! You bust!!"
            break
            
    elif player_decision == "s":
        break


  

###(additional feature if possible:) ###
#card restriction: the standard 52-card pack is used
#betting: player given chips by default (like $100?) and able to play with bets
#card: instead of just showing numbers, visually making it look more like cards