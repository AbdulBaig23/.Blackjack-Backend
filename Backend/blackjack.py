import random
import time

card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}





def create_deck():
    deck = []
    for card in card_values.keys():
        deck.extend([card] * 24)
    random.shuffle(deck)
    return deck



def calculate_hand_value(hand):
    value = sum(card_values[card] for card in hand)
    aces = hand.count('A')

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value

def deal_card(deck):
    return deck.pop()

def display_hand(player, hand):
    print(f"{player}'s hand: {', '.join(hand)} Value: ({calculate_hand_value(hand)})")

def blackjack_in_hand(hand):
    if 'A' in hand and any(card in ['10', 'J', 'Q', 'K'] for card in hand) and len(hand) == 2:
        return True
    return False

def check_chips(chips):
    if chips < 1:
        print("You ran out of chips, better luck next time!")
        exit()


def blackjack():
    chips = 1000
    while chips > 0:
        while True:
            while True:
                bet = input(f"You have {chips} chips, how much would you like to bet on this hand?")
                if not bet.isnumeric():
                    print("Please enter a valid bet")
                elif int(bet) < 1:
                    print("Your bet is less than 1, please bet again")
                elif int(bet) > chips:
                    print("Your bet is over your chip value, please bet again")
                else:
                    bet = int(bet)
                    break #break for bet


            deck = create_deck()
            players_hand = [deal_card(deck), deal_card(deck)]
            dealers_hand = [deal_card(deck), deal_card(deck)]

            display_hand("Player", players_hand)
            print(f"Dealers is showing an {dealers_hand[0]}, Value ({card_values[dealers_hand[0]]})")

            time.sleep(1)

            if any(card in ['A', 'K', 'Q', 'J', "10"] for card in dealers_hand) or any(card in ['A', 'K', 'Q', 'J', "10"] for card in players_hand):
                if blackjack_in_hand(players_hand):
                    if blackjack_in_hand(dealers_hand):
                        print("Both player and dealer have blackjack. It's a tie!")
                    else:
                        print("Player has blackjack! Player wins!")
                        print(f"Dealer had {dealers_hand} Value: {calculate_hand_value(dealers_hand)}")
                        chips += (1.5 * bet)
                    break # break for blackjack detected

                elif blackjack_in_hand(dealers_hand):
                    print("Dealer has blackjack! Dealer wins!")
                    print(f"Dealer has {dealers_hand}")
                    chips -= bet
                    check_chips(chips)
                    break # break for blackjack detected

                time.sleep(1)
                print("No blackjack detected. Continuing with the game...")



            while True:
                choice = input("Would you like to hit or stand? (h/s)").lower()
                if choice == "h":
                    players_hand.append(deal_card(deck))
                    time.sleep(1)
                    print(f"Player pulls {players_hand[-1]}")
                    time.sleep(1)
                    display_hand("Player", players_hand)
                    total = calculate_hand_value(players_hand)

                    if total == 21:
                        break #break for input

                    if calculate_hand_value(players_hand) > 21:
                        time.sleep(1)
                        print(f"Player busts, you lose!")
                        time.sleep(1)
                        display_hand("Dealer", dealers_hand)
                        chips -= bet
                        check_chips(chips)
                        break


                elif choice == "s":
                    break

                else:
                    print("Invalid Input. Please enter either a 's' to stand or a 'h' to hit")


            if calculate_hand_value(players_hand) <= 21:
                time.sleep(1)
                display_hand("Dealer", dealers_hand)
                time.sleep(2)

                while calculate_hand_value(dealers_hand) < 17:
                    print("Dealer hits")
                    time.sleep(1.5)
                    dealers_hand.append(deal_card(deck))
                    print("Dealer pulls a " + str([dealers_hand[-1]]))
                    time.sleep(1)
                    display_hand("Dealer", dealers_hand)
                    time.sleep(1)

                    if calculate_hand_value(dealers_hand) > 21:
                        print("Dealer busts! You win!")
                        chips += bet
                        time.sleep(1)
                        print(f"Players cards {', '.join(players_hand)}, total value is {calculate_hand_value(players_hand)}")
                        time.sleep(1)
                        print(f"Dealers cards {', '.join(dealers_hand)}, total value is {calculate_hand_value(dealers_hand)}")
                        time.sleep(1)
                        break
                        #return

                else:
                    player_total = calculate_hand_value(players_hand)
                    dealer_total = calculate_hand_value(dealers_hand)

                    print(f"Final player hand value {player_total}")
                    time.sleep(1)
                    print(f"Final dealer hand value {dealer_total}")
                    time.sleep(1)

                    if dealer_total > player_total:
                        print("Dealer has the higher hand, Dealer wins!")
                        chips -= bet
                        check_chips(chips)
                    elif dealer_total < player_total:
                        print("Player has the higher hand, Player wins!")
                        chips += bet
                    else:
                        print("The hands are equal, Its a push!")




if __name__ == "__main__":
    blackjack()



