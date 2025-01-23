import numpy as np
import random 
import math
from datetime import datetime

p1_hand = []
p2_hand = []
p1_score = 0
p2_score = 0
p1_c_stack =  []
p1_p_stack = []
p2_c_stack = []
p2_p_stack = []
table = []
dt_string = "report" + datetime.now().strftime("%Y%d%m_%H%M%S") 
report = open("./Report/" + dt_string + ".txt", "w+")


#it returns True if the number passed in input is a prime number, False otherwise 
def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


#this function is used to print the result of each turn 
def write_inside_report(p_hand, p_card):
    if p_hand == p1_hand and p2_hand:
        report.write("Player 1 plays card: {}\n" .format(p_card))
        report.write("Player 1 hand: {}\n" .format(p1_hand))
        report.write("Player 1 stack of prime numbers: {}\n" .format(p1_p_stack))
        report.write("Player 1 stack of composite numbers: {}\n" .format(p1_c_stack))
    else:
        report.write("Player 2 plays card: {}\n" .format(p_card))
        report.write("Player 2 hand: {}\n" .format(p2_hand))
        report.write("Player 2 stack of prime numbers: {}\n" .format(p2_p_stack))
        report.write("Player 2 stack of composite numbers: {}\n" .format(p2_c_stack))
    report.write("Table: {}\n" .format(table))
    return 0


#it checks all possible combinations of the three cards
#it returns True if found one, False otherwise
def check_all_combinations(x, y, z):
    lst = np.sort([x, y, z])
    if lst[0] + lst[1] == lst[2]:
        return True
    if lst[2] - lst[1] == lst[0]:
        return True
    if lst[0] * lst[1] == lst[2]:
        return True
    return False


#this function fills the two stack of the i-th player
def fill_stacks(n:int, cards):
    if n == 1:
        for card in cards:
            if is_prime(card):
                p1_p_stack.append(card)
            else:
                p1_c_stack.append(card)
    else:
        for card in cards:
            if is_prime(card):
                p2_p_stack.append(card)
            else:
                p2_c_stack.append(card)
    return 0
    

#this strategy tries to find a combination among one card in the player's hand 
#and the two on top of other's stacks
def super_aggressive_strategy(player_hand):
    top_stacks = []
    if player_hand == p1_hand:
        if not len(p2_p_stack) or not len(p2_c_stack):
            return -1
        top_stacks = [p2_p_stack[-1], p2_c_stack[-1]]
    else:
        if not len(p1_p_stack) or not len(p1_c_stack):
            return -1
        top_stacks = [p1_p_stack[-1], p1_c_stack[-1]]
    for card in player_hand:
        c_found = check_all_combinations(card, top_stacks[0], top_stacks[1])
        if c_found:
            if player_hand == p1_hand:
                p2_p_stack.remove(top_stacks[0])
                p2_c_stack.remove(top_stacks[1])
                p1_hand.remove(card)
                fill_stacks(1, [top_stacks[0], top_stacks[1], card])
                write_inside_report(p1_hand, card)
            else:
                p1_p_stack.remove(top_stacks[0])
                p1_c_stack.remove(top_stacks[1])
                p2_hand.remove(card)
                fill_stacks(2, [top_stacks[0], top_stacks[1], card])
                write_inside_report(p2_hand, card)
            return 1
    return -1


#this strategy evaluates the possible combinations with a card on the table 
#and the one on top of the other player's prime stack 
def aggressive_prime_strategy(player_hand):
    if player_hand == p1_hand:
        if not len(p2_p_stack) or not len(table):
            return -1
        top_stack = p2_p_stack[-1]
    else:
        if not len(p1_p_stack) or not len(table):
            return -1
        top_stack = p1_p_stack[-1]
    for card1 in player_hand:
        for card2 in table:
            c_found = check_all_combinations(card1, card2, top_stack)
            if c_found:
                table.remove(card2)
                if player_hand == p1_hand:
                    p1_hand.remove(card1)
                    p2_p_stack.remove(top_stack)
                    p1_p_stack.append(top_stack)
                    fill_stacks(1, [card1, card2])
                    write_inside_report(p1_hand, card1)
                else:
                    p2_hand.remove(card1)
                    p1_p_stack.remove(top_stack)
                    p2_p_stack.append(top_stack)
                    fill_stacks(2, [card1, card2])
                    write_inside_report(p2_hand, card1)
                return 1
    return -1


#this strategy evaluates the possible combinations with a card on the table 
#and the one on top of the other player's composite stack 
def aggressive_comp_strategy(player_hand):
    if player_hand == p1_hand:
        if not len(p2_c_stack) or not len(table):
            return -1
        top_stack = p2_c_stack[-1]
    else:
        if not len(p1_c_stack) or not len(table):
            return -1
        top_stack = p1_c_stack[-1]
    for card1 in player_hand:
        for card2 in table:
            c_found = check_all_combinations(card1, card2, top_stack)
            if c_found:
                table.remove(card2)
                if player_hand == p1_hand:
                    p1_hand.remove(card1)
                    p2_c_stack.remove(top_stack)
                    p1_c_stack.append(top_stack)
                    fill_stacks(1, [card1, card2])
                    write_inside_report(p1_hand, card1)
                else:
                    p2_hand.remove(card1)
                    p1_c_stack.remove(top_stack)
                    p2_c_stack.append(top_stack)
                    fill_stacks(2, [card1, card2])
                    write_inside_report(p2_hand, card1)
                return 1
    return -1


#this function evaluates the possible combinations with two cards on the table 
def normal_strategy(player_hand):
    table_pairs = [(a, b) for idx, a in enumerate(table) for b in table[idx + 1:]]
    for card in player_hand:
        for pairs in table_pairs:
            c_found = check_all_combinations(card, pairs[0], pairs[1])
            if c_found:
                table.remove(pairs[0])
                table.remove(pairs[1])
                if player_hand == p1_hand:
                    p1_hand.remove(card)
                    fill_stacks(1, [card, pairs[0], pairs[1]])
                    write_inside_report(p1_hand, card)
                else:
                    p2_hand.remove(card)
                    fill_stacks(2, [card, pairs[0], pairs[1]])
                    write_inside_report(p2_hand, card)
                return 1
    return -1


#it evaluates the possible combinations with a card on the table 
#and the one on top of the their own prime stack 
def defensive_prime_strategy(player_hand):
    if player_hand == p1_hand:
        if not len(p1_p_stack) or not len(table):
            return -1
        top_stack = p1_p_stack[-1]
    else:
        if not len(p2_p_stack) or not len(table):
            return -1
        top_stack = p2_p_stack[-1]
    for card1 in player_hand:
        for card2 in table:
            c_found = check_all_combinations(card1, card2, top_stack)
            if c_found:
                table.remove(card2)
                if player_hand == p1_hand:
                    p1_hand.remove(card1)
                    fill_stacks(1, [card1, card2])
                    write_inside_report(p1_hand, card1)
                else:
                    p2_hand.remove(card1)
                    fill_stacks(2, [card1, card2])
                    write_inside_report(p2_hand, card1)
                return 1
    return -1


#it evaluates the possible combinations with a card on the table 
#and the one on top of the their own composite stack 
def defensive_composite_strategy(player_hand):
    if player_hand == p1_hand:
        if not len(p1_c_stack) or not len(table):
            return -1
        top_stack = p1_c_stack[-1]
    else:
        if not len(p2_c_stack) or not len(table):
            return -1
        top_stack = p2_c_stack[-1]
    for card1 in player_hand:
        for card2 in table:
            c_found = check_all_combinations(card1, card2, top_stack)
            if c_found:
                table.remove(card2)
                if player_hand == p1_hand:
                    p1_hand.remove(card1)
                    fill_stacks(1, [card1, card2])
                    write_inside_report(p1_hand, card1)
                else:
                    p2_hand.remove(card1)
                    fill_stacks(2, [card1, card2])
                    write_inside_report(p2_hand, card1)
                return 1
    return -1


#this strategy tries to find a combination among one card in the player's hand 
#and the two on top of their own stacks
def super_defensive_strategy(player_hand):
    top_stacks = []
    if player_hand == p1_hand:
        if not len(p1_p_stack) or not len(p1_c_stack):
            return -1
        top_stacks = [p1_p_stack[-1], p1_c_stack[-1]]
    else:
        if not len(p2_p_stack) or not len(p2_c_stack):
            return -1
        top_stacks = [p2_p_stack[-1], p2_c_stack[-1]]
    for card in player_hand:
        c_found = check_all_combinations(card, top_stacks[0], top_stacks[1])
        if c_found:
            if player_hand == p1_hand:
                p1_hand.remove(card)
                fill_stacks(1, [card])
                write_inside_report(p1_hand, card)
            else:
                p2_hand.remove(card)
                fill_stacks(2, [card])
                write_inside_report(p2_hand, card)
            return 1
    return -1


#this function manages the situation in which there are not available combination
#(play one random card)
def random_strategy(player_hand):
    pl_card = random.choice(player_hand)
    table.append(player_hand.pop(player_hand.index(pl_card)))
    if player_hand == p1_hand:
        write_inside_report(p1_hand, pl_card)
    else:
        write_inside_report(p2_hand, pl_card)
    return 0


#it computes the final score for each player
def final_result():
    p1_val = (2 * len(p1_p_stack)) + (len(p1_c_stack))
    p2_val = (2 * len(p2_p_stack)) + (len(p2_c_stack))
    return [p1_val, p2_val]


#initialization 
round = 1
set_of_cards = np.arange(2, 26)
random.shuffle(set_of_cards)
p1_hand = np.sort(set_of_cards[0:12])
p2_hand = np.sort(set_of_cards[12:])
p1_hand = p1_hand.tolist()
p2_hand = p2_hand.tolist()
#select the first player 
if p2_hand[0] == 2:
    tmp = p1_hand
    p1_hand = p2_hand
    p2_hand = tmp
report.write("Primi Composti. 1 vs 1 version \nReport of the game: {}" .format(datetime.now().strftime("%Y/%d/%m %H:%M:%S")))
report.write("\n\nInitial situation:\nPlayer 1 hand: {}\n" .format(p1_hand))
report.write("Player 2 hand: {}\n\n" .format(p2_hand))
report.write("Round {}\n" .format(round))
random_strategy(p1_hand)
random_strategy(p2_hand)
#game phase 
while p1_hand and p2_hand:
    round += 1
    report.write("\nRound {}\n" .format(round))
    res = super_aggressive_strategy(p1_hand)
    if res != 1:
        res = aggressive_prime_strategy(p1_hand)
        if res != 1:
            res = aggressive_comp_strategy(p1_hand)
            if res != 1:
                res = normal_strategy(p1_hand)
                if res != 1:
                    res = defensive_prime_strategy(p1_hand)
                    if res != 1:
                        res = defensive_composite_strategy(p1_hand)
                        if res != 1:
                            res = super_defensive_strategy(p1_hand)
                            if res != 1:
                                random_strategy(p1_hand)
    res = super_aggressive_strategy(p2_hand)
    if res != 1:
        res = aggressive_prime_strategy(p2_hand)
        if res != 1:
            res = aggressive_comp_strategy(p2_hand)
            if res != 1:
                res = normal_strategy(p2_hand)
                if res != 1:
                    res = defensive_prime_strategy(p2_hand)
                    if res != 1:
                        res = defensive_composite_strategy(p2_hand)
                        if res != 1:
                            res = super_defensive_strategy(p2_hand)
                            if res != 1:
                                random_strategy(p2_hand)

#compute the final score and write the result inside the file
[p1_score, p2_score] = final_result()
report.write("\n\nFINAL RESULT:\n\n")
report.write("Player 1 stack of prime numbers: {}\n" .format(p1_p_stack))
report.write("Player 1 stack of composite numbers: {}\n" .format(p1_c_stack))
report.write("Player 2 stack of prime numbers: {}\n" .format(p2_p_stack))
report.write("Player 2 stack of composite numbers: {}\n" .format(p2_c_stack))
report.write("\nPlayer 1 score:{}\n" .format(p1_score))
report.write("Player 2 score:{}\n" .format(p2_score))
if p1_score > p2_score:
    report.write("Player 1 wins\n")
elif p1_score < p2_score:
    report.write("Player 2 wins\n")
else:
    report.write("Game ends with a draw\n")
report.close()