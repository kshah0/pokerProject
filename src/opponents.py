from gametree.playerstate.player_id import PlayerId

from gametree.gamestate.game_state import GameState

from typing import Tuple

from opp_model import OpponentModel
from sklearn.tree import DecisionTreeClassifier
from pickle import load
from pandas import DataFrame

class Opponents(OpponentModel):
    botId: PlayerId
    model: DecisionTreeClassifier


    def __init__(self, id: PlayerId):
        self.botId = id

        decision_tree_model_pkl = open("opp_model.pkl", 'rb')
        self.model = load(decision_tree_model_pkl)

    def get_bot_id(self) -> PlayerId:
        return self.botID

    def get_action_probs(self, gs:GameState):
        player_map = {player: seat for seat, player in gs.seat_map.items()}
        suit_map = {"C": 0, "D": 1, "H": 2, "S": 3}
        num_map = {"A": 1, "T": 10, "J": 11, "Q": 12, "K": 13}
        action_list = []
        hand_list = []
        community_card_list = []
        for player, seat in player_map.items():
            if seat.getId() < player_map[self.botId].getId():
                # Get known actions
                # TO DO: convert output of get_prev_action() to -1,0,1+
                action_list.append(player.get_prev_action())
            elif(seat.getId() == player_map[self.botId].getId()):
                for card in player.get_cards():
                    try:
                        num_val = num_map[card.rank]
                    except KeyError:
                        num_val = int(card.rank)
                    hand_list.append(suit_map[card.suit]*13 + num_val)
            else:
                action_list.append(-10)

        for card in gs.get_community_cards():
            try:
                num_val = num_map[card.rank]
            except KeyError:
                num_val = int(card.rank)
            community_card_list.append(suit_map[card.suit]*13 + num_val)
        for _ in range(len(gs.get_community_cards),5):
            community_card_list.append(0)

        input_cols = {'hand1':[],'hand2':[],'board1':[],'board2':[],'board3':[],'board4':[],'board5':[], 'action1':[],'action2':[],'action3':[],'action4':[],'action5':[]}
        input = DataFrame(input_cols)
        input.loc[0] = [*hand_list, *community_card_list, *action_list]

        return self.model.predict(input), self.model.predict_proba(input)
    
    def get_check_bet_probabilities(self, gamestate: GameState, actor: PlayerId) -> Tuple[float, float]:
        _, probs = self.get_action_probs(gamestate)
        return (sum(probs[:2]), sum(probs[2:]))

    def get_fold_call_raise_probabilities(self, gamestate: GameState, actor: PlayerId) -> Tuple[float, float, float]:
        _, probs = self.get_action_probs(gamestate)
        return (probs[0], probs[1], sum(probs[2:]))