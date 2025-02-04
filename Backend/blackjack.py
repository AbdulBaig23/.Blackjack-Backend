import random
import time

card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10,
               'A': 11}


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


def modified_hitL(players_hand, dealers_hand, deck, bet, chips):
    players_hand.append(deal_card(deck))
    time.sleep(1)
    print(f"Player pulls {players_hand[-1]}")
    time.sleep(1)
    display_hand("Player", players_hand)
    total = calculate_hand_value(players_hand)

    if total == 21:
        return "stand"

    if calculate_hand_value(players_hand) > 21:
        time.sleep(1)
        print(f"Player busts on {players_hand}")
        time.sleep(1)
        display_hand("Dealer", dealers_hand)
        chips -= bet
        # check_chips(chips)
        return "bust"


def modified_hitR(players_hand, deck, bet, chips):
    players_hand.append(deal_card(deck))
    time.sleep(1)
    print(f"Player pulls {players_hand[-1]}")
    time.sleep(1)
    display_hand("Player", players_hand)
    total = calculate_hand_value(players_hand)

    if total == 21:
        return "stand"

    if calculate_hand_value(players_hand) > 21:
        time.sleep(1)
        print(f"Player busts on {players_hand}")
        time.sleep(1)
        # display_hand("Dealer", dealers_hand)
        chips -= bet
        # check_chips(chips)
        return "bust"


def hit(players_hand, dealers_hand, deck, bet, chips):
    players_hand.append(deal_card(deck))
    time.sleep(1)
    print(f"Player pulls {players_hand[-1]}")
    time.sleep(1)
    display_hand("Player", players_hand)
    total = calculate_hand_value(players_hand)

    if total == 21:
        return "stand"

    if calculate_hand_value(players_hand) > 21:
        time.sleep(1)
        print(f"Player busts, you lose!")
        time.sleep(1)
        display_hand("Dealer", dealers_hand)
        chips -= bet
        check_chips(chips)
        return "bust"
    return


def double_down(players_hand, dealers_hand, bet, chips, deck):
    if chips < bet * 2:
        print(f"You only have {chips} which is not enough to double down")
    else:
        bet *= 2
        players_hand.append(deal_card(deck))
        time.sleep(1)
        print(f"Player pulls {players_hand[-1]}")
        time.sleep(1)
        display_hand("Player", players_hand)

        if calculate_hand_value(players_hand) > 21:
            time.sleep(1)
            print(f"Player busts, you lose!")
            time.sleep(1)
            display_hand("Dealer", dealers_hand)
            chips -= bet
            check_chips(chips)
        return "double"

def hand_is_bust(hand):
    if calculate_hand_value(hand) > 21:
        return True

def split(players_hand, dealers_hand, bet, chips, deck):
    right_bet = bet
    left_bet = bet
    print("splitting")
    time.sleep(1)
    new_hand1 = [players_hand[0]]
    new_hand2 = [players_hand[1]]
    new_hand1.append(deal_card(deck))
    new_hand2.append(deal_card(deck))
    print(f"Hitting both hands...")
    time.sleep(1)
    print(f"Player pulls a {new_hand1[1]} on the right hand")
    time.sleep(1)
    print(f"PLayer pulls a {new_hand2[1]} on the left hand")
    time.sleep(1)
    print(f"The hand on the left contains {new_hand2[0]} and {new_hand2[1]} total: {calculate_hand_value(new_hand2)}"
          f"\t The hand on the right contains {new_hand1[0]} and {new_hand1[1]} total: {calculate_hand_value(new_hand1)}")

    while True:
        if len(new_hand1) == 2:
            choice = input("Would you like to hit, stand or double on the right hand? (h/s/d)").lower()
            if choice == "h":
                result = modified_hitR(new_hand1, deck, bet, chips)
                if result in ["stand", "bust"]:
                    break

            elif choice == "d":
                result = double_down(new_hand1, dealers_hand, bet, chips, deck)
                right_bet = 2 * bet
                if result == "double":
                    break

            elif choice == "s":
                break

            else:
                print("Invalid Input. Please enter either a 's' to stand or a 'h' to hit")

        else:
            choice = input("Would you like to hit, or stand on the right hand? (h/s)").lower()

            if choice == "h":
                result = modified_hitR(new_hand1, deck, bet, chips)
                if result in ["stand", "bust"]:
                    break

            elif choice == "s":
                break

            else:
                print("Invalid Input. Please enter either a 's' to stand or a 'h' to hit")

    while True:
        if len(new_hand2) == 2:
            choice = input("Would you like to hit, stand or double on the left hand? (h/s/d)").lower()

            if choice == "h":
                result = modified_hitL(new_hand2, dealers_hand, deck, bet, chips)
                if result in ["stand", "bust"]:
                    break


            elif choice == "d":
                result = double_down(new_hand2, dealers_hand, bet, chips, deck)
                left_bet = 2 * bet
                if result == "double":
                    break


            elif choice == "s":
                break

            else:
                print("Invalid Input. Please enter either a 's' to stand or a 'h' to hit")

        else:
            choice = input("Would you like to hit, or stand on the left hand? (h/s)").lower()

            if choice == "h":
                result = modified_hitL(new_hand2, dealers_hand, deck, bet, chips)
                if result in ["stand", "bust"]:
                    break


            elif choice == "s":
                break

            else:
                print("Invalid Input. Please enter either a 's' to stand or a 'h' to hit")

    print("Both hands are finished. Dealer will now play.")
    return "dealer_turn", new_hand2, new_hand1, left_bet, right_bet  # Signal for the dealer to play


def blackjack():
    chips = 1000
    while chips > 0:
        split_bool = False
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
                    break  # break for bet

            deck = create_deck()
            players_hand = ["2", "2"]  # deal_card(deck), deal_card(deck)
            dealers_hand = [deal_card(deck), deal_card(deck)]

            display_hand("Player", players_hand)
            print(f"Dealers is showing an {dealers_hand[0]}, Value ({card_values[dealers_hand[0]]})")

            time.sleep(1)

            if any(card in ['A', 'K', 'Q', 'J', "10"] for card in dealers_hand) or any(
                    card in ['A', 'K', 'Q', 'J', "10"] for card in players_hand):
                if blackjack_in_hand(players_hand):
                    if blackjack_in_hand(dealers_hand):
                        print("Both player and dealer have blackjack. It's a tie!")
                    else:
                        print("Player has blackjack! Player wins!")
                        print(f"Dealer had {dealers_hand} Value: {calculate_hand_value(dealers_hand)}")
                        chips += (1.5 * bet)
                    break  # break for blackjack detected

                elif blackjack_in_hand(dealers_hand):
                    print("Dealer has blackjack! Dealer wins!")
                    print(f"Dealer has {dealers_hand}")
                    chips -= bet
                    check_chips(chips)
                    break  # break for blackjack detected

                time.sleep(1)
                print("No blackjack detected. Continuing with the game...")

            while True:
                if card_values[players_hand[0]] == card_values[players_hand[1]]:
                    choice = input("Would you like to hit, stand, split, or double down?? (h/s/ss/d)").lower()
                    if choice == "ss":
                        split_bool = True
                        result, left_hand, right_hand, left_bet, right_bet = split(players_hand, dealers_hand, bet,
                                                                                   chips, deck)
                        if result == "dealer_turn":  # If both hands finished, dealer plays
                            break

                    elif choice == "h":
                        result = hit(players_hand, dealers_hand, deck, bet, chips)
                        if result in ["bust", "stand"]:
                            break

                    elif choice == "d":
                        result = double_down(players_hand, dealers_hand, bet, chips, deck)
                        if result == "double":
                            break

                    elif choice == "s":
                        break

                    else:
                        print("Invalid Input. Please enter either a 's' to stand or a 'h' to hit")



                elif len(players_hand) == 2:
                    choice = input("Would you like to hit, stand or double? (h/s/d)").lower()

                    if choice == "h":
                        result = hit(players_hand, dealers_hand, deck, bet, chips)
                        if result in ["bust", "stand"]:
                            break

                    elif choice == "d":
                        result = double_down(players_hand, dealers_hand, bet, chips, deck)
                        if result == "double":
                            break

                    elif choice == "s":
                        break

                    else:
                        print("Invalid Input. Please enter either a 's' to stand or a 'h' to hit")


                else:
                    choice = input("Would you like to hit, or stand? (h/s)").lower()

                    if choice == "h":
                        result = hit(players_hand, dealers_hand, deck, bet, chips)
                        if result in ["bust", "stand"]:
                            break

                    elif choice == "s":
                        break

                    else:
                        print("Invalid Input. Please enter either a 's' to stand or a 'h' to hit")

            if calculate_hand_value(players_hand) <= 21 and split_bool == False:
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
                        print(
                            f"Players cards {', '.join(players_hand)}, total value is {calculate_hand_value(players_hand)}")
                        time.sleep(1)
                        print(
                            f"Dealers cards {', '.join(dealers_hand)}, total value is {calculate_hand_value(dealers_hand)}")
                        time.sleep(1)
                        break
                        # return

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

            elif split_bool == True and calculate_hand_value(left_hand) <= 21 or calculate_hand_value(right_hand) <= 21:

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
                    if hand_is_bust(left_hand):
                        chips += right_bet
                    elif hand_is_bust(right_hand):
                        chips += left_bet
                    else:
                        chips += left_bet + right_bet
                    print("Dealer busts! You win!")
                    chips += bet
                    time.sleep(1)
                    print(f"Players cards {', '.join(right_hand)}, total value is {calculate_hand_value(right_hand)}"
                            f"\t Players cards {', '.join(left_hand)}, total value is {calculate_hand_value(left_hand)}")

                    time.sleep(1)
                    print(
                        f"Dealers cards {', '.join(dealers_hand)}, total value is {calculate_hand_value(dealers_hand)}")
                    time.sleep(1)
                    break
                        # return

                else:
                    left_hand_total = calculate_hand_value(left_hand)
                    right_hand_total = calculate_hand_value(right_hand)
                    dealer_total = calculate_hand_value(dealers_hand)

                    print(
                        f"Final player left hand value {left_hand_total} \tFinal player right hand value {right_hand_total}")
                    time.sleep(1)
                    print(f"Final dealer hand value {dealer_total}")
                    time.sleep(1)

                    if left_hand_total < dealer_total and right_hand_total < dealer_total:
                        print(f"The Dealers total: {dealer_total} is higher both your hands {left_hand_total} and "
                              f"{right_hand_total}. Both lose!")
                        chips -= right_bet
                        chips -= left_bet
                        check_chips(chips)

                    elif left_hand_total > dealer_total > right_hand_total:
                        print(
                            f"The Dealers total: {dealer_total} is higher than one of your hands. You win on the Left Hand")
                        chips += left_bet
                        chips -= right_bet
                        check_chips(chips)

                    elif left_hand_total < dealer_total < right_hand_total:
                        print(
                            f"The Dealers total: {dealer_total} is higher than one of your hands. You win on the Right Hand")
                        chips += right_bet
                        chips -= left_bet
                    elif left_hand_total > dealer_total and right_hand_total > dealer_total:
                        print(f"Both your hands beat the dealers hand.The Dealers total: {dealer_total} You win!")
                        chips += (left_bet + right_bet)
                        check_chips(chips)
                    elif left_hand_total > dealer_total and right_hand_total == dealer_total:
                        print(f"The Dealers total: {dealer_total} You win on the left hand and push on the right!")
                        chips += left_bet
                        check_chips(chips)
                    elif left_hand_total == dealer_total and right_hand_total > dealer_total:
                        print(f"The Dealers total: {dealer_total} You win on the right hand and push on the left!")
                        chips += right_bet
                        check_chips(chips)
                    elif left_hand_total < dealer_total and right_hand_total == dealer_total:
                        print(f"The Dealers total: {dealer_total} You lose on the left hand and push on the right!")
                        chips -= left_bet
                        check_chips(chips)
                    elif left_hand_total == dealer_total and right_hand_total < dealer_total:
                        print(f"The Dealers total: {dealer_total} You lose on the right hand and push on the left!")
                        chips -= right_bet
                        check_chips(chips)
                    else:
                        print("Both hands are equal, Its a push!")


if __name__ == "__main__":
    blackjack()
