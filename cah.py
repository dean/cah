from collections import defaultdict
import random
import re


NUM_CARDS = 8

print "Welcome to Cards Against Humanity! -- IRC Version"

def format_white(card):
    card = card.strip("\n")
    if card.endswith("."):
        card = card[:-1]
    return card

def init_black(card):
    card = card.strip("\n")
    if "__________" not in card:
        card += " __________."
    return card

def format_black(card):
    card.strip("\n")
    for x in xrange(card.count("__________")):
        card = card.replace("__________", "{" + str(x) + "}", 1)
    return card

def show_hand(name, players):
        cards = '. '.join((str(x + 1) + ": " + players[name][x]
                            for x in xrange(NUM_CARDS)))
        hand = p + ": Your hand is: \n[%s]"
        print hand % cards

# Look at db of cards -- mock it for now
whites = map(format_white, open("whites.txt", "r").readlines())
blacks = map(init_black, open("blacks.txt", "r").readlines())

random.shuffle(whites)
random.shuffle(blacks)

players = defaultdict(list)
names = ['johnsdea', 'brutal_chaos', 'edunham', 'rettigs']
names = ['Dean', 'Matt', 'Hans']
# Deal cards
for name in names:
    # Gives a player NUM_CARDS random cards. Then draw every turn.
    players[name] = [whites.pop(0) for x in xrange(NUM_CARDS-1)]

# Assign a starting player
black_discard = []
white_discard = []
scores = defaultdict(int)

# Put all players in a loop and then a while game around the rest.
while True:
    for player in players:
        prompt = blacks.pop(0)
        print player + " reads: " + prompt
        print "Type .play <card #> to fill in the blanks. Multiple " \
                "cards are played with: .play <card #> <card #>"

        avail_players = [p for p in players if p != player]

        # Draw cards!!
        for p in avail_players:
            while len(players[p]) < NUM_CARDS:
                players[p].append(whites.pop(0))

        for p in avail_players:
            show_hand(p, players)

        answers = defaultdict(list)
        num_to_play = prompt.count("__________")

        play_re = r"\.play (.*)"
        nums_re = r"\d"
        for p in avail_players:
            cards = raw_input(p + " enter which card "
                                "you want to play: ")
            nums = re.match(play_re, cards, re.S).group(1)
            cards_to_play = map(int, re.findall(nums_re, nums))
            if cards_to_play:
                # Handle an off by 1
                answers[p] = [players[p][c - 1] for c in cards_to_play]
                
                # Don't change index of cards to pop.
                for index in reversed(sorted(cards_to_play, key=lambda x: x)):
                    players[p].pop(index - 1)
            # Handle a wrong card here
            else:
                continue

        random.shuffle(avail_players)

        print "And the answers are: "
        for x in xrange(len(avail_players)):
            text = ("[Answer #" + str(x) + "]: " +
                    format_black(prompt).format(*answers[avail_players[x]]))
            print text if text.endswith(".") else text + "."

        winner_re = r".winner (\d)"
        winner = raw_input("[*] Type .winner <answer #> to choose a winner:")

        # Handle incorrect shit here

        winning_ind = re.match(winner_re, winner).group(1)
        print "And the winner is " + avail_players[int(winning_ind)] + "!"
        scores[avail_players[int(winning_ind)]] += 1

        sorted_scores = sorted(scores.items(), key=lambda x: scores[1])
        score_str = "{:^14}|{:^14}"
        for score in sorted_scores:
            print score_str.format(score[0], str(score[1]))
        print "Leaders: " + ' - '.join((score[0] + ": " + str(score[1])
                                        for score in sorted_scores))

        # Fill black discard
        black_discard.append(prompt)

        # Fill white discard
        for p in avail_players:
            print p
            for c in answers[p]:
                white_discard.append(c)

        if len(black_discard) > len(blacks) * 2:
            blacks += black_discard
            random.shuffle(blacks)
            black_discards = []

        if len(white_discard) > len(whites) * 2:
            whites += white_discard
            random.shuffle(whites)
            white_discards = []

