###basic rule: dealer must draw on 16 and stand on 17###

#cards: just get random choice
#card values:it is up to each individual player if an ace is worth 1 or 11. 
#face cards are 10 and any other card is its pip value.

#dealer
#player (get user's name)
player_name = raw_input("What's your name: ").title()
game_continue = False
# hit_num = 0
# frame_line = " "+ "-" * (40 + hit_num)
judge = False
who_win = ""
#ask use if they want to continue to play
continue_to_play = True

import random
cards = {"A":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}


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
        return 10 *player_card.count("A") + score_cal(player_card)

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


#previoud code
#to print out the current cards and sums
# def current_stat():
#     print frame_line
#     #if cards contain "A", show two sums
#     if "A" in dealer_card[1:]:
#         print "| Dealer's cards:{}, total:{} or {}".format((["@"] + dealer_card[1:]), (dealer_score - dealer_hidden_card), (dealer_score2 - dealer_hidden_card))
#     else:
#         print "| Dealer's cards:{}, total:{}".format((["@"] + dealer_card[1:]), (dealer_score - dealer_hidden_card))
#     if "A" in player_card:
#         print "| {}'s cards:{}, total:{} or {}".format(player_name, player_card, player_score, player_score2)
#     else:
#         print "| {}'s cards:{}, total:{}".format(player_name, player_card, player_score)
#     print frame_line


#v5 fearture added: change the apprearance of dealer's face down card 
def print_card(player_card):
    global show_card
    player_card_amount = len(player_card)
    print_line_order = 1
    
    #if it's dealer's card, then first item will be "@"
    if player_card[0] =="@":
        for dline, line, cline in zip(dlines, lines, clines):
            if print_line_order == 2:
                sec_line = ""
                for card in player_card[1:]:
                    if card == "10":
                        show_card = card
                        sec_line += "|{} ".format(show_card)
                    else:
                        show_card = card
                        sec_line += "| {} ".format(show_card)
    
                print dline + sec_line + cline
            else:
                print dline + line * (player_card_amount - 1) + cline
            print_line_order += 1
    else:
        for line, cline in zip(lines, clines):
            if print_line_order == 2:
                for card in player_card:
                    if card == "10":
                        show_card = card
                        line = "|{}".format(show_card)
                        print line,
                    else:
                        show_card = card
                        line = "| {}".format(show_card)
                        print line,
                print cline + "\t"
            else:
                print line * player_card_amount + cline
            print_line_order += 1

#until player decided to Stand, dealer's first card should be faced down
# def hidden_card(dealer_card):
#     global show_card
#     dealer_card_amount = len(dealer_card)
#     print_line_order = 1
#     for line, cline in zip(lines, clines):
#         if print_line_order == 2:
#             for card in dealer_card:
#                 show_card = card
#                 line = "| {}".format(show_card)
#                 print line,
#             print cline + "\t"
#         else:
#             print line * dealer_card_amount + cline
#         print_line_order += 1

def current_stat(player_card, dealer_card):
    
    dealer_card_copy = ["@"] + dealer_card[1:]
    if "A" in dealer_card_copy[1:]:
        print "Dealer's cards:"
        print_card(dealer_card_copy)
        print "total:{} or {}".format((dealer_score - dealer_hidden_card), (dealer_score2 - dealer_hidden_card))
    else:
        print "Dealer's cards:" 
        print_card(dealer_card_copy)
        print "total:{}".format(dealer_score - dealer_hidden_card)
    
    print 
    
    if "A" in player_card:
        print "{}'s cards:".format(player_name)
        print_card(player_card)
        print "total:{} or {}".format(player_score, player_score2)
    else:
        print "{}'s cards:".format(player_name)
        print_card(player_card)
        print "total:{}".format(player_score)

def dealer_play():
    global dealer_score
    global dealer_score2
    global judge
    global who_win
    if 21 > dealer_score2 >= 17 :
        if 21 > player_score2:
                winner_check(player_score2, max(dealer_score,dealer_score2))
        else:
            winner_check(player_score, max(dealer_score,dealer_score2))
        # game_continue = False
        
    #16 >= dealer_score
    else:
        while dealer_score <= 16 or dealer_score2 <= 16:
            dealer_card.append(card_giving())
            dealer_score = score_cal(dealer_card)
            dealer_score2 = score_cal_aeleven(dealer_card)
            
            if natural_check(dealer_score) or natural_check(dealer_score2):
                print "Dealer's Black Jack!"
                print "You lose!"
                who_win = "Dealer"
                # game_continue = False
                judge = False
                break
                
            elif bust_check(dealer_score):
                print "Dealer bust!!"
                print "You are so lucky!"
                who_win = player_name
                # game_continue = False
                judge = False
                break
            
            elif 21 > dealer_score2 >= 17:
                winner_check(player_score, dealer_score2)
                judge = False
                break
            
            else:
                #if none of above cases happens, start judging who is the winner
                judge = True
                
        #when judge turned on to "True", call winner_check to judge the winner        
        if judge == True:
            winner_check(player_score, dealer_score)

#if none of the pleayer or dealer got blackjack or bust, judge who is the winner        
def winner_check(player_score, dealer_score):
    global who_win
    if player_score > dealer_score:
        print "You win!!"
        who_win = player_name
        
    elif player_score < dealer_score:
        print "Sorry You lose"
        who_win = "Dealer"
        
    else:
        print "******TIE******"
        who_win = "TIE"
    # game_continue = False     


while continue_to_play == True:
    #cards appearance: instead of just showing numbers, making it look more like cards visually
    show_card = " " 
    line1 = " ---"
    line2 = "| {}".format(show_card)
    line3 = "|   "
    line4 = "|   "
    line5 = "|   "
    line6 = " ---"
    lines = [line1, line2, line3, line4, line5, line6]
    
#v5 fearture added: change the apprearance of dealer's face down card     
    dline1 = " ---"
    dline2 = "|///"
    dline3 = "|///"
    dline4 = "|///"
    dline5 = "|///"
    dline6 = " ---"
    dlines = [dline1, dline2, dline3, dline4, dline5, dline6]
    
    
    #closing frame lines
    #random choice of emoticon: v3 feature added
    emoticon = random.choice([":)", "<3", ":p", ":]", ":)", ":D", ":>", ":P", "=D", ":D", ":b", "BJ"])
    cline1 = "--- "
    cline2 = "   |"
    cline3 = "   |"
    cline4 = "   |"
    cline5 = " {}|".format(emoticon)
    cline6 = "--- "
    clines = [cline1, cline2, cline3, cline4, cline5, cline6]
    
    #####################game heading part####################
    #receive two cards: for example
    #dealer's cards show as */9 (total:9) -->second card face down(hidden by any icon like *)
    #player's cards show as 10/5 (total:15)
    dealer_card = []
    player_card = []
    
    #serving cards at the beginning
    for card in range(2):
        dealer_card.append(card_giving())
        player_card.append(card_giving())
    
    #calculate the sum of dealer's cards and player's cards respectively
    dealer_score = score_cal(dealer_card)
    player_score = score_cal(player_card)
    
    #dealer's first card should be faced down
    dealer_hidden_card = cards[dealer_card[0]]
    
    #store another variable, if the cards contain "A", plus 10 value, if not, stay as it is
    dealer_score2 = score_cal_aeleven(dealer_card)
    player_score2 = score_cal_aeleven(player_card)
    
        
    current_stat(player_card, dealer_card)
    
    
    ####check if blackjack###
    #check if both got blackjack(very rare case)
    if (natural_check(dealer_score) or natural_check(dealer_score2)) and (natural_check(player_score) or natural_check(player_score2)):
        print "OMG! Both of you and dealer got BlackJack!"
        who_win ="TIE"
    
    #check if dealer got blackjack.
    elif natural_check(dealer_score) or natural_check(dealer_score2):
        print "Dealer has Black Jack!!!"
        print "You lose!"
        who_win = "Dealer"
    
    #checki if player got blackjack
    elif natural_check(player_score) or natural_check(player_score2):
        print "WOW! Black Jack!!!"
        print "You win!"
        who_win = player_name
    
    else:
        game_continue = True
    
    #####################game heading part####################
    
    
    #player can decide to Hit/Stand
    #when player decided to stand -> dealer's turn-> compare the sums -> determine lose or win
    #when player decided to hit -> add one card -> calculate the sum
      #if over 21: goes bust ->player loses        
      #if equal to 21: blackjack! -> dealer's turn -> if dealer has no black jack, player wins         
      #if under 21: player can decide to Hit/ Stand --> 
      #----hit: continue the loop
      #----stand:  dealer's turn -> compare the sums -> determine lose or win
    
       
    
    #game begins
    #after first serving, player can deicide next step, to hit or stand
    while game_continue:
        player_decision = raw_input("You want to stand or hit? [s/h]\n>").lower() 
        if player_decision == "h":
            #add one cand to player's cards
            player_card.append(card_giving())
            
            #update the card total score
            # dealer_score = score_cal(dealer_card)
            player_score = score_cal(player_card)
            # dealer_score2 = score_cal_aeleven(dealer_card)
            player_score2 = score_cal_aeleven(player_card)
            
            current_stat(player_card, dealer_card)
    
            if natural_check(player_score) or natural_check(player_score2):
                print "You got Black Jack!"
                who_win = player_name
                # dealer_play()
                game_continue = False
                
            elif bust_check(player_score) and bust_check(player_score2):
                print "I'm sorry! You bust!!"
                who_win = "Dealer"
                game_continue = False
                
        elif player_decision == "s":
            dealer_score = score_cal(dealer_card)
            dealer_score2 = score_cal_aeleven(dealer_card)
            dealer_turn = True
            dealer_play()
            game_continue = False        
        else:
            print "!!!Not a valid command. Input [s] to stand; [h] to hit!!!"
            
    
    
    
    
    
    #########################game result############################
    def final_stat(player_card, dealer_card):
        if "A" in dealer_card:
            print "Dealer's cards:"
            print_card(dealer_card)
            print "total:{} or {}".format(dealer_score, dealer_score2)
        else:
            print "Dealer's cards:" 
            print_card(dealer_card)
            print "total:{}".format(dealer_score)
        
        # print "__________________________________________"
        print
        
        if "A" in player_card:
            print "{}'s cards:".format(player_name)
            print_card(player_card)
            print "total:{} or {}".format(player_score, player_score2)
        else:
            print "{}'s cards:".format(player_name)
            print_card(player_card)
            print "total:{}".format(player_score)
    
    print
    print "##########################################"
    print "______________Final result________________"
    print "Winner is......{}!".format(who_win)
    # print frame_line
    # print "| Dealer's cards:{}, total:{}".format(dealer_card, dealer_score2)
    # print "| {}'s cards:{}, total:{}".format(player_name, player_card, player_score)
    # print frame_line
    final_stat(player_card, dealer_card)
    print "##########################################"
    
    
    #ask player if not continue, end the while loop
    continue_to_play_command = raw_input("Do you want to continue to play? [y/n]\n>").lower()
    if continue_to_play_command == "n":
        continue_to_play = False
        print "Have a nice day! {}!".format(player_name)
    elif continue_to_play_command == "y":
        print "Great! New game starts..........."
        print 
        pass
    else:
        print "I guess you don't want to stop!"
    


###(additional feature if possible:) ###
#card restriction: the standard 52-card pack is used
#betting: player given chips by default (like $100?) and able to play with bets
#cards appearance: instead of just showing numbers, visually making it look more like cards
