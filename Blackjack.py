#One-Player Blackjack with a Dealer - Tristan Williams
from random import sample
from time import sleep

def blackjack(name='Mr. Bond',new=True):
    ##Welcome
    graphic()
    print 
    print 'Welcome ' + (new==False)*'back ' + 'to Blackjack, %s.' % name
    #First round gives option to read the rules
    while new:
        rule = raw_input('Would you like to read the rules? Y/N: ')
        if rule.upper() == 'Y':
            rules()
            break
        elif rule.upper() == 'N':
            print "Then let's play!"
            print
            break
        else:
            print "---Please enter 'Y' or 'N'---"
    chips = 100
    cont = 'Y'
    print 'You start ' + (new==False)*'again ' +'with 100 chips.'

    ##Build Deck
    deck = builddeck()
    
    ##Play Blackjack
    while cont.upper() != 'N':
        while True:

            ##Place Bet
            print 'Place your bet. It must be an integer between 1 and %i.' \
                  % chips
            #Restrict bets to integer format
            while True:
                try:
                    bet = int(raw_input('Your bet: '))
                    if (bet >= 1) and (bet <= chips):
                        print '\nYou bet',bet,'chip(s).'
                        break
                    else: print 'That is not a valid bet.'
                except ValueError:
                    print 'That is not a valid bet.'

            ##Deal Cards
            playerhand = []
            dealerhand = []
            deal(playerhand,deck)
            deal(dealerhand,deck)
            deal(playerhand,deck)
            deal(dealerhand,deck)
            print 'Dealer shows:',dealerhand[1]
            print 'You have',playerhand,'worth %i.' % max(score(playerhand))

            ##Option for insurance
            insurancebet = 0
            dealerblackjack = False
            if dealerhand[1] == 'Ace' and 3*bet/2 <= chips:
                insurancebet = (bet+1)/2
                while True:
                    print 'You can buy insurance for %i.' %insurancebet
                    insurance = raw_input('Would you like to buy it? Y/N: ')
                    if insurance.upper() == 'Y':
                        chips -= insurancebet
                        if max(score(dealerhand))==21:
                            print 'Dealer reveals:',dealerhand[0]
                            print 'Dealer has blackjack.'
                            dealerscore = 'blackjack'
                            dealerblackjack = True
                            print
                            print 'Your insurance wins you %s chips.' \
                                  % 2*insurancebet
                            chips += 2*insurancebet
                            print
                        else: 
                            print 'Dealer does not have blackjack.\n'
                        break
                    elif insurance.upper() == 'N':
                        break
                    else: print "---Please enter 'Y' or 'N'---"
                    
            ##PlayerTurn
            if max(score(playerhand)) == 21:
                print 'Blackjack!'
                print
                sleep(0.5)
                bet = bet*3/2
                surrender = False
                playerscore = 'blackjack'
            elif not dealerblackjack:
                playerhand,playerscore,deck,bet,surrender = \
                        playerturn(playerhand,deck,bet,chips,dealerblackjack)

                #Break for single surrenders or busts.
                if surrender == True:
                    chips -= bet
                    break
                elif playerscore == 0:
                    chips -= bet
                    print 
                    break
                print
            else: PlayerScore = 0
            sleep(0.1)

            ##Dealer Turn
            if not dealerblackjack:
                print 'Dealer reveals:',dealerhand[0]
                print 'Dealer has',dealerhand,'worth %i.'\
                      % max(score(dealerhand))
                if max(score(dealerhand)) == 21:
                    print 'Blackjack!'
                    dealerscore = 'blackjack'
                else: dealerhand,dealerscore,deck = dealerturn(dealerhand,deck)
                print
            sleep(0.1)
            
            ##Resolution
            ##First convert everything to lists
            if type(bet) == int:
                playerscore = [playerscore]
                playerhand = [playerhand]
                bet = [bet]
                surrender = [surrender]

            ##Evaluate winnings of each hand
            for i in range(len(playerscore)):
                deck += playerhand[i] #Player cards are put back into the deck
                if surrender[i] == True:
                    print 'You surrendered hand %i for %i chip(s).\n'\
                          % ((i+1),bet[i])
                    chips -= bet[i]
                else:
                    if playerscore[i] == 'blackjack':
                        print 'With your blackjack,'
                    else:
                        print 'With your hand',playerhand[i],'worth %s,'\
                              % playerscore[i]
                    if dealerscore > playerscore[i]:
                        print 'Dealer wins, you lose %i chip(s).\n' % bet[i]
                        chips -= bet[i]
                    elif dealerscore == playerscore[i]:
                        print 'Push, bet is returned.\n'
                    elif dealerscore < playerscore[i]:
                        print 'You win %i chip(s).\n' % bet[i]
                        chips += bet[i]
                            
            break

        #Dealer card put back into deck
        deck += dealerhand
        
        ##Option to Continue
        print 'You have %i chip(s), %s.' % (chips,name)
        if chips == 0:
            sleep(1.5)
            cont = 'N'
        elif chips > 0:
            while True:
                cont = raw_input('Continue? Y/N: ')
                if cont.upper() == 'Y' or cont.upper() == 'N': break
                else: print "---Please enter 'Y' or 'N'---"
        print
        
    ##Salutation
    print "You ended with %s chip(s)." % chips
    if chips == 0:
        sadgraphic()
        print "Dial 1-800-GAMBLER for assistance with a gambling problem."
    elif chips < 100:
        print "At least you're not bankrupt."
    elif chips == 100:
        print "That was... exciting."
    elif chips > 100 and chips < 1000:
        print "You've beaten the odds. Well done. But you could do better...."
    if chips >= 1000:
        print
        for i in range(50):
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print
        print chips,"chips! Great job! Now, we're gonna"
        print "need you to answer some questions...."
    print
    print "Thanks for playing!"

def deal(hand,deck):
    card = sample(deck,1)[0]
    hand.append(card)
    deck.remove(card)

def score(hand):
    score = [0]

    #Different Scores are contained in a list, incremented using lambda calculus
    for i in range(len(hand)):
        if type(hand[i])==int:
            score = map(lambda x: x+hand[i],score)

        #Aces have two possible values
        elif hand[i] == 'Ace':
            soft = map(lambda x: x+1,score)
            score = map(lambda x:x+11,score)
            score += soft
        
        #Anything else must be worth 10
        else: score = map(lambda x:x+10,score)

    #Busts are set to zero
    for i in range(len(score)):
        if score[i] > 21: score[i] = 0

    return score

def playerturn(hand,deck,bet,chips,dealerblackjack):
    surrender = False #Binary for surrender
    ##Player actions
    ##Split comes first because it has to recurse if used.
    while True:
        if len(hand) == 2 and (hand[0]==hand[1] or \
                                 max(score(hand))==20) and 2*bet <= chips:
            while True:
                split = raw_input('Would you like to split your hand? Y/N: ')
                if split.upper() == 'Y':
                    deal(hand,deck)
                    deal(hand,deck)
                    hand1 = [hand[0],hand[2]]
                    hand2 = [hand[1],hand[3]]
                    bet1 = bet
                    bet2 = bet

                    ##Split aces draw one more card and then end
                    if hand[0] == 'Ace':
                        score1 = max(score(hand1))
                        score2 = max(score(hand2))
                        print '\nYou have',hand1,'and',hand2,'worth %i and %i.' % (score1,score2)

                    ##Playing hand 1
                    else:
                        print '\nYou have',hand1,'worth %i.' % max(score(hand1))
                        if max(score(hand1)) != 21:
                            hand1,score1,deck,bet1,surrender1 = \
                            playerturn(hand1,deck,bet1,chips,dealerblackjack)
                        else:
                            score1 = 21
                            surrender1 = False
                    ##Playing hand 2
                        print '\nYou have',hand2,'worth %i.' % max(score(hand2))
                        if max(score(hand2)) != 21:
                            if type(bet1)== list:
                                prebet = sum(bet1)
                            else: prebet = bet1
                            hand2,score2,deck,bet2,surrender2 = \
                            playerturn(hand2,deck,bet2,chips-prebet,\
                            dealerblackjack)
                        else:
                            score2 = 21
                            surrender2 = False

                    #Converting new hand results to lists        
                    if type(score1) == int:
                        score1 = [score1]
                        bet1 = [bet1]
                        surrender1 = [surrender1]
                    if type(score2) == int:
                        score2 = [score2]
                        bet2 = [bet2]
                        surrender2 = [surrender2]
                    scores = score1 + score2
                    bet = bet1 + bet2
                    surrender = surrender1 + surrender2

                    #Setting up hands so that we do not return a list of lists
                    if len(score1) > 1 and len(score2) > 1:
                        hand = hand1 + hand2
                    elif len(score1) == 1 and len(score2) > 1:
                        hand = [hand1] + hand2
                    elif len(score1) > 1 and len(score2) == 1:
                        hand = hand1 + [hand2]
                    else: hand = [hand1,hand2]
                    return hand,scores,deck,bet,surrender
                elif split.upper() == 'N': break
                else: print "---Please enter 'Y' or 'N'---"

        ##Actions past splitting
        if 2*bet <= chips:
            turn = raw_input('Would you like to [h]it, [s]tand, '\
                                '[d]ouble down, or su[r]render? ')
        else: turn = raw_input('Would you like to [h]it, [s]tand, '\
                               'or su[r]render? ')
        
        ##Double Down
        if turn.lower() == 'double down' or turn.lower() == 'd':
            #Only allowed if it can be afforded
            if 2*bet > chips:
                print "You don't have the chips for that."
            else:
                bet *= 2
                deal(hand,deck)
                print 'You double your bet and draw:',hand[-1]
                if max(score(hand)) != 0:
                    print 'You have',hand,'worth %i.' % max(score(hand))
                break
        ##Surrender
        elif turn.lower() == 'surrender' or turn.lower() == 'r':
            if dealerblackjack:
                print "Dealer has blackjack, surrender is not allowed."
                return hand,max(score(hand)),deck,bet,surrender
            else:
                surrender = True
                #Need to return the ceiling of half the bet
                #Python automatically floors division of ints
                bet -= bet/2
                print 'You surrender your cards for half of your bet.\n'
                break

        ##Hit
        elif turn.lower() == 'hit' or turn.lower() == 'h':
            deal(hand,deck)
            print 'You draw:',hand[-1]
            if max(score(hand)) != 0:
                print 'You have',hand,'worth %i.' % max(score(hand))
            #After first hit, can now only hit or stand
            while max(score(hand)) > 0 and max(score(hand)) < 21:
                turn = raw_input('Would you like to [h]it or [s]tand? ')
                if turn.lower() == 'hit' or turn.lower() == 'h':
                    deal(hand,deck)
                    print 'You draw:',hand[-1]
                    if max(score(hand)) != 0:
                        print 'You have',hand,'worth %i.' % max(score(hand))
                elif turn.lower() == 'stand' or turn.lower() == 's':
                    break
                else: print "---Please enter 'hit' or 'stand'---"
            break

        ##Stand
        elif turn.lower() == 'stand' or turn.lower() == 's':
            print 'You stay at %i.' % max(score(hand))
            break
        else:
            if chips >= 2*bet:
                print "---Please enter '[h]it', '[s]tand'," \
                        "'[d]ouble down', or 'su[r]render'---"
            else: print "---Please enter '[h]it', '[s]tand',"\
                          "or 'su[r]render'---"

    ##Turn conclusion
    if max(score(hand)) == 0:
        print 'You busted.'
    elif max(score(hand)) == 21: print 'You stay at 21.'
    return hand,max(score(hand)),deck,bet,surrender

                         
def dealerturn(hand,deck):
    #Dealer draws until 17 or higher
    while (max(score(hand)) != 0) and (max(score(hand)) < 17):
        deal(hand,deck)
        print 'Dealer draws:',hand[-1]
        print 'Dealer has',hand
    if max(score(hand)) == 0:
       print 'Dealer busts.'
    elif max(score(hand)) == 21: print 'Dealer has 21.'
    else: print 'Dealer stays at %i.' % max(score(hand))
    return hand,max(score(hand)),deck

def builddeck(decks = 1):
    deck = range(2,11)
    faces = ['Jack','Queen','King','Ace']
    deck += faces
    deck *= 4 * decks
    deck.sort()
    return(deck)
    
def rules():
    print "The goal is to get your hand closer to 21"
    print "than the dealer without going over."
    print
    print "Each turn, you must place a nonnegative"
    print "integer bet no higher than your current"
    print "chip count. On your turn, you have the"
    print "option to 'hit', drawing another card from"
    print "the deck. If your total is still under 21,"
    print "you may continue to 'hit' and draw cards."
    print "Jacks, queens, and kings are each worth 10"
    print "points, and an ace may be worth 1 or 11."
    print "Instead of hitting, you also have the option"
    print "to 'stand' and doing so will end your turn."
    print
    raw_input("Press 'Enter' to continue")
    print
    print "In addition, you have three other moves that"
    print "may be available on your turn:"
    print "1) If you 'double down', your bet is doubled,"
    print "you draw one more card, and then you have to"
    print "stand. You may only do this if you have"
    print "enough chips to afford it."
    print "2) If you 'surrender' your hand, you receive"
    print "half of your bet back and end your turn"
    print "immediately."
    print
    raw_input("Press 'Enter' to continue")
    print
    print "3) Lastly, if you start with a pair of cards"
    print "or any two 10-point cards, you may 'split'"
    print "them. The two split cards then form their"
    print "own hands, which are each dealt another card."
    print "These two new hands are played consecutively,"
    print "each with a bet equal to the original. If "
    print "they again meet the split requirements, you"
    print "may continue splitting as long as you can"
    print "afford it. However, if one splits aces,"
    print "because of their likelihood for blackjack,"
    print "those two new hands must stand."
    print
    print "On the dealer's turn, the dealer hits until"
    print "their total is 17 or higher and then stands."
    print "The dealer must stand on soft 17, called "
    print "'soft' because it has an ace that could take"
    print "a lower value."
    print
    raw_input("Press 'Enter' to continue")
    print
    print "'Blackjack' is defined as and ace and a"
    print "10-point card, and may only happen on the"
    print "initial deal. Blackjack pay 3 to 2, and is"
    print "considered to be higher than 21 made any other"
    print "way. 21's that happen on a split are not"
    print "considered blackjacks."
    print
    print "Finally, before you start your turn, the dealer"
    print "reveals the last card they were dealt. If the"
    print "dealer shows an ace, you have the option to buy"
    print "insurance. Insurance bets are equal to 1/2 of"
    print "the original bet value and pay 2 to 1. If"
    print "insurance is bought, the dealer reveals "
    print "immediately if they have blackjack."
    print
    raw_input("Press 'Enter' to continue")
    print
    print "Let's play!"

def graphic():
    print '---------------------------------------'
    print '--@@@@--@------@@@---@@@---@--@--------'
    print '--@---@-@-----@---@-@---@--@-@---------'
    print '--@@@@--@-----@@@@@-@------@@----------'
    print '--@---@-@-----@---@-@---@--@-@---------'
    print '--@@@@--@@@@@-@---@--@@@---@--@--------'
    print '---------------------------------------'
    print '------------@@@@@--@@@---@@@--@--@--@--'
    print '--------------@---@---@-@---@-@-@---@--'
    print '--------------@---@@@@@-@-----@@----@--'
    print '----------@---@---@---@-@---@-@-@------'
    print '-----------@@@----@---@--@@@--@--@--@--'
    print '---------------------------------------'

def sadgraphic():
    print
    print '---------------------------------------'
    print '--@@@@@@@@@@----@@@---@@@--@---@-@@@@@-'
    print '-@----------@--@---@-@---@-@@-@@-@-----'
    print '@---@@---@@--@-@-----@@@@@-@-@-@-@@@---'
    print '@---@@---@@--@-@--@@-@---@-@---@-@-----'
    print '@------------@-@---@-@---@-@---@-@-----'
    print '@------------@--@@@--@---@-@---@-@@@@@-'
    print '@----@@@@@---@-------------------------'
    print '@---@-----@--@--@@@--@---@-@@@@@-@@@@--'
    print '-@----------@--@---@-@---@-@-----@---@-'
    print '--@@@@@@@@@@---@---@-@---@-@@@---@@@@--'
    print '---------------@---@-@---@-@-----@---@-'
    print '--@-@-@-@-@-@--@---@--@-@--@-----@---@-'                                    
    print '-@-@-@-@-@-@-@--@@@----@---@@@@@-@---@-'
    print '---------------------------------------'

def startblackjack():
    while True:
        answer = raw_input('Do you want to play blackjack? Y/N: ')
        if answer.upper() =='N': break
        elif answer.upper()=='Y':
            name = raw_input('What is your name? ')
            name = name.strip()
            if name == '':
                name = 'Mr. Bond'
            print
            blackjack(name)
            print
            break
        else: print "---Please enter 'Y' or 'N'---"
    while True:
        answer = raw_input('Again? Y/N: ')
        if answer.upper() =='N': break
        elif answer.upper()=='Y':
            print
            blackjack(name,False)
            print
        else: print "---Please enter 'Y' or 'N'---"
    
startblackjack()
