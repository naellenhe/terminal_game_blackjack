#v7 code review

###basic rule: dealer must draw on 16 and stand on 17###

#cards: get random choice of cards
##card values:
#it is up to each individual player if an ace is worth 1 or 11. 
#face cards are 10 and any other card is its pip value.

##2 plaers:
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
#by default, give player $100
player_chip = 100
round_count = 0


import random
cards = {"A":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}

#card serving: choose a card randomly from list "cards"
def card_giving():
    player_card = random.choice(cards.keys()) 
    return player_card

#calculate total score of received cards. in this function "A" counted as "1"
#take player/dealer's card list as argument
def score_cal(received_cards, total = 0):
    for card_key in received_cards:
        total += cards[card_key]
    return total

#same as above.second condition if contains "A", count as 11
def score_cal_aeleven(player_card):
    if "A" not in player_card:
        return score_cal(player_card)
    else:
    # player_card.count("A")
        return 10 + score_cal(player_card)


#check if it's a count of 21(a.k.a blackjack) of first two cards
def natural_check(total):
    if total == 21:
        return True
    else:
        return False

#if cards total value exceed 21, then judge it as "bust"        
def bust_check(total):
    if total > 21:
        return True
    else:
        return False


######previoud code(for record only)###############
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
######previoud code(for record only)###############



#v5 fearture added: change the apprearance of dealer's face down card 
def print_card(player_card):
    global show_card
    player_card_amount = len(player_card)
    print_line_order = 1
    
    #if it's dealer's card, first item will be "@" (face-down card)
    if player_card[0] =="@":
        for dline, line, cline in zip(dlines, lines, clines):
            #second print line contains numbers. if it's "10"(2 digit), use a different format to align with other cards
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
    #player's card
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


####################previous code######################
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
    #dealer's first card should face down. here use "@" to mark that card.
    dealer_card_copy = ["@"] + dealer_card[1:]
    
    #if "A" in cards, print two cases that A is counted as 1 and 11 respectively
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
    print


### Dealer's turn! basic rule: dealer must draw on 16 and stand on 17####
def dealer_play():
    global dealer_score
    global dealer_score2
    global judge
    global who_win
    if 21 > dealer_score2 >= 17 :
        winner_check(player_score_final, max(dealer_score,dealer_score2))
        # game_continue = False
        
    #16 >= dealer_score
    else:
        while dealer_score <= 16 or dealer_score2 <= 16:
            dealer_card.append(card_giving())
            dealer_score = score_cal(dealer_card)
            dealer_score2 = score_cal_aeleven(dealer_card)
            
            if natural_check(dealer_score) or natural_check(dealer_score2):
                print "Dealer has 21!"
                # print "You lose!"
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
                winner_check(player_score_final, dealer_score)
                judge = False
                break
            
            else:
                #if none of above cases happens, start judging who is the winner
                judge = True
                
        #when judge turned on to "True", call winner_check to judge the winner        
        if judge == True:
            #if player_score2(bigger number than player_score) bust, judge with player_score
            winner_check(player_score_final, dealer_score)

#if none of the pleayer or dealer got blackjack or bust, judge who is the winner        
def winner_check(player_score, dealer_score):
    global who_win
    if player_score > dealer_score:
        print "Congrats!!!"
        who_win = player_name
        
    elif player_score < dealer_score:
        print "Sorry You lose"
        who_win = "Dealer"
        
    else:
        print "******TIE******"
        who_win = "TIE"
    # game_continue = False     


#############################  functions above  ########################################
#############################  main code part below  ###################################

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
    
    
    #clines list means closing frame lines
    #random choice of emoticon: v3 feature added
    emoticon = random.choice([":)", "<3", ":p", ":]", ":)", ":D", ":>", ":P", "=D", ":D", ":b", "BJ"])
    cline1 = "--- "
    cline2 = "   |"
    cline3 = "   |"
    cline4 = "   |"
    cline5 = " {}|".format(emoticon)
    cline6 = "--- "
    clines = [cline1, cline2, cline3, cline4, cline5, cline6]
    
    ######################### game first part: card seving  #######################
    #count how many rounds and print out in final result message
    round_count += 1
    #blackjack reset
    black_jack = False 
    
    #player place a bet
    print "Hey {}! Now you have ${}".format(player_name, player_chip)
    place_bet = raw_input("How much do you want to bet? \n>$")
    
    #check if it's all valid number or within available bet amount
    while not place_bet.isdigit() or not (player_chip >= int(place_bet) > 0):
        place_bet = raw_input("Not a valid number or Not enough chips.\nPlease place a bet again.\n>$")
    
    #after checking the validity of "place_bet" input , convert to int type
    place_bet = int(place_bet)
    
    
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
    
    
    #dealer's first card should be faced down and not counted in the sum when print out
    dealer_hidden_card = cards[dealer_card[0]]
    
    #store another variable, if the cards contain "A", plus 10 value, if not, stay as it is
    dealer_score2 = score_cal_aeleven(dealer_card)
    player_score2 = score_cal_aeleven(player_card)
    
    #when player decied to "Stand" or when judging who's the winner, use the player's final score(the "A" counting as 1 or 11 issue)
    player_score_final = 0
    
    #print the current card set    
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
        black_jack = True
        who_win = player_name
    
    else:
        game_continue = True
    
    ######################### game first part: card seving  #######################
    
    
    #player can decide to Hit/Stand
    #when player decided to stand -> dealer's turn-> compare the sums -> determine lose or win
    #when player decided to hit -> add one card -> calculate the sum
      #if over 21: goes bust ->player loses        
      #if equal to 21: blackjack! -> dealer's turn -> if dealer has no black jack, player wins         
      #if under 21: player can decide to Hit/ Stand --> 
      #----hit: continue the loop
      #----stand:  dealer's turn -> compare the sums -> determine lose or win
    
    player_score_final = 0   
    
    #game begins (user interface)
    #after first serving, player can deicide next step, to hit or stand
    while game_continue:
        
        player_decision = raw_input("You want to stand or hit? [s/h]\n>").lower() 
        
        if player_decision == "h":
            #add one cand to player's cards
            player_card.append(card_giving())
            
            #update the card total score when hitting new card
            # dealer_score = score_cal(dealer_card)
            player_score = score_cal(player_card)
            # dealer_score2 = score_cal_aeleven(dealer_card)
            player_score2 = score_cal_aeleven(player_card)
            
            current_stat(player_card, dealer_card)
    
            if natural_check(player_score) or natural_check(player_score2):
                print "You got 21!"
                # who_win = player_name
                # dealer_play()
                player_score_final = 21
                dealer_turn = True
                dealer_play()
                game_continue = False
                
            elif bust_check(player_score) and bust_check(player_score2):
                print "I'm sorry! You bust!!"
                who_win = "Dealer"
                game_continue = False
                
        elif player_decision == "s":
            #if player_score2(counts A as 11) is not over 21, use it as the final score because it's the bigger number
            #if player_score2(counts A as 11) is alreay over 21, use player_score as the final score
            if 21 > player_score2:
                    player_score_final = player_score2
            else:
                player_score_final = player_score
            
            dealer_score = score_cal(dealer_card)
            dealer_score2 = score_cal_aeleven(dealer_card)
            dealer_turn = True
            dealer_play()
            game_continue = False  
            
        else:
            print "!---Not a valid command. Input [s] to stand; [h] to hit---!"
            
    #betting result $$$$$$$$$$$$$$$$$$
    #multiplying "1.5" only when player has blackjack(first 2 served cards)
    if who_win == player_name:
        if black_jack == True:
            player_chip += place_bet * 1.5
            print "You win ${}!".format(place_bet * 1.5)
        else:
            player_chip += place_bet
            print "You win ${}!".format(place_bet)
        
    elif who_win == "Dealer":
        player_chip -= place_bet
        print "You lose ${}!".format(place_bet)        
    
    
    ######################### game result ############################
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
    print "               Final result               "
    print "##########################################"

    # print "Winner is......{}!".format(who_win)
    # print frame_line
    # print "| Dealer's cards:{}, total:{}".format(dealer_card, dealer_score2)
    # print "| {}'s cards:{}, total:{}".format(player_name, player_card, player_score)
    # print frame_line
    final_stat(player_card, dealer_card)
    print "##########################################"
    print "  Round {}    Winner: {}    ($)($){}".format(round_count, who_win, player_chip)
    print "##########################################"
    
    #if player has no more money, game over :/
    if player_chip <= 0:
        print "Sorry you don't have enough money. Go back to work!"
        print "See you next time!"
        continue_to_play = False
        break
    
    #ask player if not continue, end the while loop
    continue_to_play_command = raw_input("Do you want to continue to play? [y/n]\n>").lower()
    if continue_to_play_command == "n":
        continue_to_play = False
        print "Have a nice day! {}!".format(player_name)
        
    elif continue_to_play_command == "y":
        print "Great!\n .......Starting a new game..........\n"
        pass
    
    else:
        print "I guess you don't want to stop!"
    
    ######################### game result ############################
    
    


###(additional feature if possible:) ###
#card restriction: the standard 52-card pack is used
#betting: player given chips by default (like $100?) and able to play with bets
#cards appearance: instead of just showing numbers, visually making it look more like cards
