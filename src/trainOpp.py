import pandas as pd
from os import listdir
from os.path import isfile, join

LOG_PATH = "./../../5H1AI_logs"
BB_value = 100

# Maps actions "no action", "fold", and "call"
# Raise is value of raise
action_map = {"na": -10, "f": -1, "c": 0} 

# Takes input "[num value char][suit char]"
# Returns suit*13 + num value
# Value of 0 implies card is unknown
def cardValue(card_str):
    
    suit_map = {"c": 0, "d": 1, "h": 2, "s": 3}
    num_map = {"A": 1, "T": 10, "J": 11, "Q": 12, "K": 13}
    try:
        num_val = num_map[card_str[0]]
    except KeyError:
        num_val = int(card_str[0])
    return suit_map[card_str[1]]*13 + num_val

def updateBets(action, prev_bets, turn):
    if action == 'f':
        return prev_bets
    elif action == 'c':
        prev_bets[turn] = max(prev_bets)
    else:
        prev_bets[turn] = int(action)/BB_value


# Takes input string for actions from all betting rounds
# Returns list of player actions and list of bot actions from each round 
def getActions(actions_string, bot_turn):
    folds = [0,0,0,0,0,0]
    
    round_actions_players = []
    round_action_bot = []

    round_actions = actions_string.split("/")
    
     # Init previous bets in pre-flop order (first non-blind player --> big blind)
    prev_bets = [0,0,0,0,.5,1]
    # Shift bot turn based on pre-flop order
    bot_turn = (bot_turn-2)%len(prev_bets)

    preflop = True

    for actions in round_actions:
        bot_fold = False
        single_round_actions_players = [action_map['na'] for i in range(5)]
        single_round_action_bot = [action_map['na']]
        turn = 0
        offset = 0

        try:
            # Check if betting round is after flop
            if actions == round_actions[1]:
                #Unflag preflop
                preflop = False
                # Un-shift bot turn
                bot_turn = (bot_turn+2)%len(prev_bets)
                prev_bets_preflop = prev_bets.copy()
                # Rearrage previous bets into regular order
                prev_bets = [prev_bets_preflop[(i-2)%len(prev_bets_preflop)] for i in range(len(prev_bets_preflop))]
        except IndexError:
            if actions != round_actions[0]:
                break

        for i in range(len(actions)):
            if i+offset == len(actions) or turn >= len(prev_bets):
                break
            if turn < bot_turn:
                print(actions[i+offset])
                if actions[i+offset] != 'r':
                    single_round_actions_players[turn] = action_map[actions[i+offset]]
                    updateBets(actions[i+offset], prev_bets, turn)
                    if actions[i+offset] == 'f':
                        folds[turn] = 1
                else:
                    end_idx = i+offset+1
                    while(actions[end_idx] != 'c' and actions[end_idx] != 'f' and actions[end_idx] != 'r'):
                        end_idx += 1
                    single_round_actions_players[turn] = int(actions[i+offset+1:end_idx])/BB_value - prev_bets[turn]
                    updateBets(actions[i+offset+1:end_idx], prev_bets, turn)
                    offset += end_idx-(i+offset+1)

            elif turn == bot_turn:
                if actions[i+offset] != 'r':
                    single_round_action_bot = [action_map[actions[i+offset]]]
                    updateBets(actions[i+offset], prev_bets, turn)
                    if actions[i+offset] == 'f':
                        # Flag to ignore rest of hand
                        bot_fold = True
                else:
                    end_idx = i+offset+1
                    while(actions[end_idx] != 'c' and actions[end_idx] != 'f' and actions[end_idx] != 'r'):
                        end_idx += 1
                    single_round_action_bot = [int(actions[i+offset+1:end_idx])/BB_value - prev_bets[turn]]   
                    updateBets(actions[i+offset+1:end_idx], prev_bets, turn)  
                    offset += end_idx-(i+offset+1)     
                if not preflop:
                    break
            elif preflop:
                if actions[i+offset] != 'r':
                    updateBets(actions[i+offset], prev_bets, turn)
                    if actions[i+offset] == 'f':
                        folds[turn] = 1
                else:
                    end_idx = i+offset+1
                    while(actions[end_idx] != 'c' and actions[end_idx] != 'f' and actions[end_idx] != 'r'):
                        end_idx += 1
                    updateBets(actions[i+offset+1:end_idx], prev_bets, turn)
                    offset += end_idx-(i+offset+1)
            turn += 1
        
        rem = 0
        for i in range(len(folds)):
            if folds[i]:         
                del prev_bets[i-rem]
                bot_turn -= 1
                rem+=1
        folds = [folds[i] for i in range(len(folds)) if folds[i] == 0]
                

        round_actions_players.append(single_round_actions_players)
        round_action_bot.append(single_round_action_bot)

        if bot_fold:
            break
        
    return round_actions_players, round_action_bot
                        
def getHandBoard(cards, bot_turn):
    bot_hand_vals = [cardValue(cards.split("/")[0].split("|")[bot_turn][0:2]), cardValue(cards.split("/")[0].split("|")[bot_turn][2:4])]
    bot_hand = [bot_hand_vals for _ in range(len(cards.split("/")))] 
    boards = [[0 for _ in range(5)]]
    card_num = 0
    if len(cards.split("/")) > 1:
        for dealt_cards in cards.split("/")[1:]:
            new_board = boards[-1].copy()
            for i in range(int(len(dealt_cards)/2)):
                new_board[card_num] = cardValue(dealt_cards[2*i:2*i+2])
                card_num += 1
            boards.append(new_board)
    return bot_hand, boards


def parseFile(f):
    with open(f) as file:
        for line in file:
            if line.split(":")[0] == 'STATE':
                print(line)
                _, _, actions, cards, _, players = line.split(":")
                players = players[:-1]
                bot_turn = players.split("|").index("Pluribus")
                #bot_hands, boards = getHandBoard(cards, bot_turn)
                actions_players, actions_bots = getActions(actions, bot_turn)

            

if __name__ == '__main__':
    input_cols = {'hand1':[],'hand2':[],'board1':[],'board2':[],'board3':[],'board4':[],'board5':[], 'action1':[],'action2':[],'action3':[],'action4':[],'action5':[]}
    input_train = pd.DataFrame(input_cols)

    output_cols = {'action':[]}
    output_train = pd.DataFrame(output_cols)

    print(input_train)
    files = [f for f in listdir(LOG_PATH) if isfile(join(LOG_PATH, f))]
    # print(files)
    for f in files:
            if f.split('.')[-1] == 'log':
                print("Opening {}".format(f))
                parseFile(join(LOG_PATH, f)) #inputs, outputs = 
            else:
                print("{} does not end with .log, not parsing".format(f))
                continue