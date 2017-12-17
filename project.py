#v6 new feature added: player given chips $100 by default and able to place a bet
#v7 code clean up
#v8 print format revision. welcome messege added
#v9 file write-in feature added. set new final score variable
#v10 score module import
#v11 code review
#v12 option of doubling down added
#v13 using a whole deck of cards(52 cards), and each card only served once
#v14 code review

###basic rule: dealer must draw on 16 and stand on 17###

#cards: get random choice of cards
##card values:
#it is up to each individual player if an ace is worth 1 or 11. 
#face cards are 10 and any other card is its pip value.

game_continue = False
# hit_num = 0
# frame_line = " "+ "-" * (40 + hit_num)
# judge = False
who_win = ""
#ask user if they want to continue to play
continue_to_play = True
#by default, give player $100
# player_chip = 100
round_count = 0
#v8 new added. make it look like the dealer's speaking
message_format ="\n... ((  Dealer says ))  "

#v8 welcome messege added
print """
     --------------------------
    |  Welcome to CASINO 2020  |
    |      Are you ready?      |
     --------------------------
"""



##2 plaers:
#dealer
#player (get user's name)
player_name = raw_input("What's your name: ").title()

#v10 score module import
import score
if player_name in score.record.keys():
    print message_format + "Welcome back! {}!".format(player_name)
    player_chip = score.record[player_name]
    if player_chip <= 0:
        print "\tWe are giving you $100 as a welcome back gift!"
        player_chip = 100
else:
    print message_format + "Welcome! New friend!"
    player_chip = 100
    filehandler = open("score.py","a")
    filehandler.write("\nrecord['{}'] = 100".format(player_name))
    filehandler.close()

import random


#recording
myfile = open("record.txt", "a")
myfile.write("Player: {}\n".format(player_name))
myfile.close()

#card serving: choose a card randomly from list "cards"
def card_giving():
    served_card = random.choice(cards_for_serving.keys())
    #v13 once used, delete from the cards dict so it won't repeat
    del cards_for_serving[served_card]
    return served_card

#calculate total score of received cards. in this function "A" counted as "1"
#take player/dealer's card list as argument
def score_cal(received_cards, score = 0):
    for card_key in received_cards:
        score += cards[card_key]
    return score

#same as above.second condition if contains "A", count as 11
def score_cal_aeleven(received_cards):
    if check_ace_contain(received_cards):
        return 10 + score_cal(received_cards)
    else:
        return score_cal(received_cards)        

#13 check if ace contains, if so return True
def check_ace_contain(received_cards):
    for card in received_cards:
        #if found "A" in any card's second character (card content: symbol + number)
        if "A" in card[1:]:
            return True
            # break  #<-memo: once returned one value, for loop stops (unlike print)
    else:
        return False


#check if it's a count of 21(a.k.a blackjack) of first two cards
def natural_check(score):
    if score == 21:
        return True
    else:
        return False

#if cards total value exceed 21, then judge it as "bust"        
def bust_check(score):
    if score > 21:
        return True
    else:
        return False


#v13 when printing cards, show the symbols
def show_card_symbol(symbol):
    #card symbols
    #white
    # spade = u"\u2664".encode('utf-8')
    # heart = u"\u2661".encode('utf-8')
    # diamond = u"\u2662".encode('utf-8')
    # club= u"\u2667".encode('utf-8')
    #black
    spade = u"\u2660".encode('utf-8')
    heart = u"\u2665".encode('utf-8')
    diamond = u"\u2666".encode('utf-8')
    club= u"\u2663".encode('utf-8')
    
    if symbol == "s":
        return spade
    elif symbol == "h":
        return heart
    elif symbol == "d":
        return diamond
    elif symbol == "c":
        return club
    else:
        return " "

#v5 fearture added: change the apprearance of dealer's face down card 
def print_card(player_card):
    player_card_amount = len(player_card)
    print_line_order = 1
    
    #if it's dealer's card, first item will be "@" (face-down card)
    if player_card[0] =="@":
        for dline, line, cline in zip(dlines, lines, clines):
            #second print line contains numbers. if it's "10"(2 digit), use a different format to align with other cards
            if print_line_order == 2:
                second_line = ""
                for card in player_card[1:]:
                    if card[1:] == "10":
                        second_line += "|{} ".format(card[1:])
                    else:
                        second_line += "| {} ".format(card[1:])
                print dline + second_line + cline
                
            #v13 print card symbol
            elif print_line_order == 3:
                third_line = ""
                for card in player_card[1:]:
                        third_line += "| {} ".format(show_card_symbol(card[:1]))
                print dline + third_line + cline                
                
            else:
                print dline + line * (player_card_amount - 1) + cline
            print_line_order += 1
    #player's card
    else:
        for line, cline in zip(lines, clines):
            if print_line_order == 2:
                for card in player_card:
                    if card[1:] == "10":
                        line = "|{}".format(card[1:])
                        print line,
                    else:
                        line = "| {}".format(card[1:])
                        print line,
                print cline + "\t"
                
            elif print_line_order == 3:
                third_line = ""
                for card in player_card:
                        third_line += "| {} ".format(show_card_symbol(card[:1]))
                print third_line + cline        
                
            else:
                print line * player_card_amount + cline
            print_line_order += 1


def current_stat(player_card, dealer_card):
    #dealer's first card should face down. here use "@" to mark that card.
    dealer_card_copy = ["@"] + dealer_card[1:]
    
    #if "A" in cards, print two cases that A is counted as 1 and 11 respectively
    if check_ace_contain(dealer_card_copy):
        print "Dealer's cards:"
        print_card(dealer_card_copy)
        print "score:{} or {}".format((dealer_score - dealer_hidden_card), (dealer_score2 - dealer_hidden_card))
    else:
        print "Dealer's cards:" 
        print_card(dealer_card_copy)
        print "score:{}".format(dealer_score - dealer_hidden_card)
    
    print 
    
    if check_ace_contain(player_card):
        print "{}'s cards:".format(player_name)
        print_card(player_card)
        print "score:{} or {}".format(player_score, player_score2)
    else:
        print "{}'s cards:".format(player_name)
        print_card(player_card)
        print "score:{}".format(player_score)

### Dealer's turn! basic rule: dealer must draw on 16 and stand on 17####
def dealer_play():
    global dealer_score
    global dealer_score2
    global dealer_score_final
    global who_win
    judge = False
    
    if 21 > dealer_score2 >= 17 :
        winner_check(player_score_final, dealer_score2)
        dealer_score_final = dealer_score2
        # game_continue = False
        
    #16 >= dealer_score
    else:
        while dealer_score <= 16 or dealer_score2 <= 16:
            dealer_card.append(card_giving())
            dealer_score = score_cal(dealer_card)
            dealer_score2 = score_cal_aeleven(dealer_card)
            
            if natural_check(dealer_score) or natural_check(dealer_score2):
                print message_format + "Dealer's score got 21"
                # if player_score_final == 21:
                #     who_win = "TIE"
                # else:
                #     who_win = "Dealer"
                judge = False
                dealer_score_final = 21
                winner_check(player_score_final, dealer_score_final)
                break
                
            elif bust_check(dealer_score):
                print message_format + "Dealer busts!!"
                print message_format + "You are so lucky!"
                who_win = player_name
                judge = False
                dealer_score_final = dealer_score
                break
            
            elif 21 > dealer_score2 >= 17:
                dealer_score_final = dealer_score2
                winner_check(player_score_final, dealer_score_final)
                judge = False
                break
            
            else:
                #if none of above cases happens, start judging who is the winner
                judge = True
                
        #when judge turned on to "True", call winner_check to judge the winner        
        if judge == True:
            dealer_score_final = dealer_score
            winner_check(player_score_final, dealer_score_final)

def final_stat(player_card, dealer_card):
    print
    print "Dealer's cards:" 
    print_card(dealer_card)
    print "score:{}".format(dealer_score_final)

    # print "__________________________________________"
    print
    
    print "{}'s cards:".format(player_name)
    print_card(player_card)
    print "score:{}".format(player_score_final)



#if none of the pleayer or dealer got blackjack or bust, judge who is the winner        
def winner_check(player_score, dealer_score):
    global who_win
    if player_score > dealer_score:
        print message_format + "Congrats!!! Yay! \(^.^)/"
        who_win = player_name
        
    elif player_score < dealer_score:
        print message_format + "Sorry You lose  <(._.)>"
        who_win = "Dealer"
        
    else:
        print message_format + "TIE! Nice play! d-(^_^)-b"
        who_win = "TIE"
    # game_continue = False     

############################ for checking purpose ##############################
#show remaining cards
def cards_serving_machine(player_card, dealer_card):
        cards_remaining_list = cards_whole_pack[:]
        cards_remaining_list = [card for card in cards_remaining_list if card not in (player_card + dealer_card)]

        for suit in "shdc":
            print_card([card for card in cards_remaining_list if card[0] == suit])

#show the whole pack of cards
cards_whole_pack = [
    'sA', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 'sJ', 'sQ', 'sK', 
    'hA', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'hJ', 'hQ', 'hK', 
    'dA', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'dJ', 'dQ', 'dK', 
    'cA', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'cJ', 'cQ', 'cK'
    ]


#############################  functions above  ########################################
#############################  main code part below  ###################################

while continue_to_play == True:
    
    #v13 card symber: s for spades, h for hearts, d for diamonds, c for clubss
    cards = {"sA":1,"s2":2,"s3":3,"s4":4,"s5":5,"s6":6,"s7":7,"s8":8,"s9":9,"s10":10,"sJ":10,"sQ":10,"sK":10,
             "hA":1,"h2":2,"h3":3,"h4":4,"h5":5,"h6":6,"h7":7,"h8":8,"h9":9,"h10":10,"hJ":10,"hQ":10,"hK":10,
             "dA":1,"d2":2,"d3":3,"d4":4,"d5":5,"d6":6,"d7":7,"d8":8,"d9":9,"d10":10,"dJ":10,"dQ":10,"dK":10,
             "cA":1,"c2":2,"c3":3,"c4":4,"c5":5,"c6":6,"c7":7,"c8":8,"c9":9,"c10":10,"cJ":10,"cQ":10,"cK":10,
            }
    #v13 copy the cards dict for serving/removing served cards
    cards_for_serving = cards.copy()
    
    #cards appearance: instead of just showing numbers, making it look more like cards visually
    line1 = " ---"
    line2 = "|   "
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
    emoticon = random.choice([":)", ":p", ":]", ":)", ":D", ":>", ":P", "=D", ":D", ":b"])
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
    #v12 option for doubling down
    double_down_option = False

    # want_to_see_cards_in_machine = raw_input("We are serving standard 52 cards! No repeat! ")
    # if want_to_see_cards_in_machine == "check":
    #     cards_serving_machine([], [])


    #player place a bet
    print message_format + "Now you have ${}".format(player_chip)
    place_bet = raw_input("\tHow much do you want to bet? \nBet($) >")
    
    #check if it's all valid number or within available bet amount
    while not place_bet.isdigit() or not (player_chip >= int(place_bet) > 0):
        place_bet = raw_input("Not a valid number or Not enough chips.\nPlease place a bet again.\n>$")
    
    #after checking the validity of "place_bet" input , convert to int type
    place_bet = int(place_bet)
    
    
    #receive two cards: for example
    #dealer's cards show as */9 (total:9) -->second card face down(hidden by any icon like *)
    #player's cards show as 10/5 (total:15)

    #below variables reset every new game:
    dealer_card = []
    player_card = []
    
    #serving two cards at the beginning
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
    dealer_score_final = 0
    player_score_final = 0
    
    #print the current card set   
    print message_format + "Cards serving\n" 
    current_stat(player_card, dealer_card)
    
    
    ####check if blackjack###
    #check if both got blackjack(very rare case)
    if (natural_check(dealer_score) or natural_check(dealer_score2)) and (natural_check(player_score) or natural_check(player_score2)):
        print message_format + "OMG!\n\tBoth of you and dealer got BlackJack!"
        who_win ="TIE"
        dealer_score_final = 21
        player_score_final = 21
    
    #check if dealer got blackjack.
    elif natural_check(dealer_score) or natural_check(dealer_score2):
        print message_format + "Dealer has Black Jack!!!"
        print message_format + "You lose!"
        who_win = "Dealer"
        dealer_score_final = 21
        player_score_final = player_score2
    
    #checki if player got blackjack
    elif natural_check(player_score) or natural_check(player_score2):
        print message_format + "WOW! Black Jack!!!"
        print message_format + "You win!"
        black_jack = True
        who_win = player_name
        dealer_score_final = dealer_score2
        player_score_final = 21
    
    else:
        game_continue = True
        if (9 <= player_score <= 11) and (player_chip >= place_bet * 2):
            double_down_option = True
        
    
    ######################### game first part: card seving  #######################
    
    
    #player can decide to Hit/Stand
    #when player decided to stand -> dealer's turn-> compare the sums -> determine lose or win
    #when player decided to hit -> add one card -> calculate the sum
      #if over 21: goes bust ->player loses        
      #if equal to 21: blackjack! -> dealer's turn -> if dealer has no black jack, player wins         
      #if under 21: player can decide to Hit/ Stand --> 
      #----hit: continue the loop
      #----stand:  dealer's turn -> compare the sums -> determine lose or win
    #Another option open to the player is doubling his bet when the original two cards dealt total 9, 10, or 11. 
    #When the player's turn comes, he places a bet equal to the original bet, and the dealer gives him just one card.
    
    
    

    #game begins (user interface)
    #after first serving, player can deicide next step, to hit or stand
    while game_continue:
        
        #v12 option of doubling down added.
        #it's an addtional option when player's original two cards dealt total 9, 10, or 11
        if double_down_option:
            player_decision = raw_input("""
========================================== 
                [s]tand 
    options:    [h]it 
                [d]ouble down 
========================================== \n>""").lower()
        else:
            player_decision = raw_input("""
========================================= 
    options:    [s]tand                  
                [h]it                    
=========================================\n>""").lower() 
        
        
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
                print message_format + "Your score got 21"
                player_score_final = 21
                # dealer_turn = True
                dealer_play()
                final_stat(player_card, dealer_card)
                game_continue = False
                
            elif bust_check(player_score) and bust_check(player_score2):
                print message_format + "I'm sorry! You bust!!"
                who_win = "Dealer"
                game_continue = False
                dealer_score_final = dealer_score2
                player_score_final = player_score
                final_stat(player_card, dealer_card)
                
        elif player_decision == "s":
            #if player_score2(counts A as 11) is not over 21, use it as the final score because it's the biggest number
            #if player_score2(counts A as 11) is alreay over 21, use player_score as the final score
            if 21 > player_score2:
                    player_score_final = player_score2
            else:
                player_score_final = player_score
            
            dealer_score = score_cal(dealer_card)
            dealer_score2 = score_cal_aeleven(dealer_card)
            # dealer_turn = True
            dealer_play()
            final_stat(player_card, dealer_card)
            game_continue = False  
        
        elif player_decision == "d":
            place_bet = place_bet * 2
            print "You've doubled your bet to ${}".format(place_bet)
            player_card.append(card_giving())
            
            #update the score of player's cards
            player_score = score_cal(player_card)
            player_score2 = score_cal_aeleven(player_card)
            
            if player_score <= player_score2 <= 21:
                player_score_final = player_score2
            else:
                player_score_final = player_score
                
            dealer_play()
            final_stat(player_card, dealer_card)
            game_continue = False  
            
        else:
            print "!---Not a valid command. Select again---!"
            
    #betting result
    #multiplying "1.5" only when player has blackjack(first 2 served cards)
    from math import ceil
    if who_win == player_name:
        if black_jack == True:
            player_chip += place_bet * 1.5
            player_chip = int(ceil(player_chip)) 
            print message_format + "You won ${}!".format(int(ceil(place_bet*1.5)))
        else:
            player_chip += place_bet
            print message_format + "You won ${}!".format(place_bet)
        
    elif who_win == "Dealer":
        player_chip -= place_bet
        print message_format + "You lost ${}!".format(place_bet)        
    
    
    ######################### game result ############################
    # def final_stat(player_card, dealer_card):
    #     if "A" in dealer_card:
    #         print "Dealer's cards:"
    #         print_card(dealer_card)
    #         print "total:{} or {}".format(dealer_score, dealer_score2)
    #     else:
    #         print "Dealer's cards:" 
    #         print_card(dealer_card)
    #         print "total:{}".format(dealer_score)
        
    #     # print "__________________________________________"
    #     print
        
    #     if "A" in player_card:
    #         print "{}'s cards:".format(player_name)
    #         print_card(player_card)
    #         print "total:{} or {}".format(player_score, player_score2)
    #     else:
    #         print "{}'s cards:".format(player_name)
    #         print_card(player_card)
    #         print "total:{}".format(player_score)

    
    print    
    see_result = raw_input("Press enter to see the result of this round.\n")    
    
    print
    print "##########################################"
    print "###########   Final result    ############"
    print "##########################################"
    # print "Winner is......{}!".format(who_win)
    # print frame_line
    # print "| Dealer's cards:{}, total:{}".format(dealer_card, dealer_score2)
    # print "| {}'s cards:{}, total:{}".format(player_name, player_card, player_score)
    # print frame_line
    final_stat(player_card, dealer_card)
    print "##########################################"
    if who_win == player_name:
        result = "WIN!"
    elif who_win == "Dealer":
        result = "LOSE"
    else:
        result = who_win
    print "  Round {}    Result: {}    ($)($){}".format(round_count, result, player_chip)
    print "##########################################"
    
    
    #recording
    myfile = open("record.txt", "a")
    myfile.write("Round {:<4}Bet ($){:<5}Result: {:<10}Remaining ($){:<6}\n".format(round_count, place_bet, result, player_chip))
    myfile.write("  Dealer {} ({})    \n  {} {} ({})\n\n".format(dealer_card, dealer_score_final, player_name, player_card, player_score_final))    
    myfile.close()
    
    
    #if player has no more money, game over :/
    if player_chip <= 0:
        print message_format
        print "\tSorry you don't have enough money." 
        print "\tGo back to work!"
        # print "\tSee you next time!"
        # print " ---------------------------------------- "
        # print "|   Sorry you don't have enough money.   |"
        # print "|   Go back to work!                     |"
        # print "|   See you next time!                   |"
        # print " ---------------------------------------- "
        continue_to_play = False
        break
    
    #ask player if not continue, end the while loop
    continue_to_play_command = raw_input("Do you want to continue to play? [y/n]\n>").lower()
    if continue_to_play_command == "n":
        continue_to_play = False
        print "Have a nice day! {}!".format(player_name)
        
    elif continue_to_play_command == "y":
        print message_format, "Great!"
        print """
     --------------------------
    |  Starting a new game...  |
    |      Are you ready?      |
     --------------------------"""
        pass
    
    else:
        print "I guess you don't want to stop!"
    ######################### game result ############################

#recording
myfile = open("record.txt", "a")
myfile.write("----------------------- new ------------------------\n")
myfile.close()


#v10 save final score 
filehandler = open("score.py","a")
filehandler.write("\nrecord['{}'] = {}".format(player_name, player_chip))
filehandler.close()









###(additional feature if possible:) ###
#card restriction: the standard 52-card pack is used
#betting: player given chips by default (like $100?) and able to play with bets
#cards appearance: instead of just showing numbers, visually making it look more like cards




