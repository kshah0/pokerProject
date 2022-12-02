# from typing import Set
# from card import Card
# from gametree.gamestate.abstract_game_state import AbstractGameState
# from gametree.gamestate.game_state import GameState
# from gametree.playerstate.player_id import PlayerId
# from gametree.playerstate.player_state import PlayerState
# from gametree.playerstate.seated_player_state import SeatedPlayerState
# from gametree.round import Round
# from gametree.table_config import TableConfiguration


# class DetailedHoldemTableState(AbstractGameState):
#     table: DetailedHoldemTable

#     def __init__(self, table: DetailedHoldemTable) -> None:
#         self.table = table
#         for player in table.get_players():
#             self.seat_map[player.get_seat_id()] = player.get_id()
    
#     def get_community_cards(self) -> Set[Card]:
#         return set(self.table.get_community_cards())

#     def get_dealer(self) -> PlayerId:
#         return self.table.get_dealer().get_id()

#     def get_largest_bet(self) -> int:
#         result = 0
#         for player in self.table.get_players():
#             result = max(result, player.get_bet_chips_value())
#         return result

#     def get_last_bettor(self) -> PlayerId:
#         max_bet = self.get_largest_bet()
#         dealer_seat_id = self.get_player(self.get_dealer()).get_seat_id().get_id()
#         candidates = []
#         for player in self.table.get_players():
#             if player.get_bet_chips_value() == max_bet:
#                 candidates.append(player)
#         for _ in range(self.table.get_table_config().get_max_num_players()):
#             for player in candidates:
#                 if player.get_seat_id().get_id() == dealer_seat_id:
#                     return player.get_id()
#             dealer_seat_id -= 1
#             if dealer_seat_id < 0:
#                 dealer_seat_id += self.table.get_table_config().get_max_num_players()
#         return None

#     def get_last_event(self):
#         return

#     def get_min_next_raise(self) -> int:
#         return

#     def get_num_raises(self) -> int:
#         return 0

#     def get_next_to_act(self) -> PlayerId:
#         return

#     def get_player(self, player_id: PlayerId) -> PlayerState:
#         selected = None
#         for player in self.table.get_players():
#             if player.get_id() == player_id:
#                 selected = player
#                 break
#         if (
#             selected is None
#             or not selected.is_sitting_in()
#         ):
#             return None
#         return SeatedPlayerState(selected)

#     def get_previous_game_state(self) -> GameState:
#         return self

#     def get_previous_rounds_pot_size(self) -> int:
#         pots = self.table.get_pots()
#         if pots is None:
#             return 0
#         return pots.total_value

#     def get_round(self) -> Round:
#         return self.table.get_round()

#     def get_round_pot_size(self) -> int:
#         result = 0
#         for player in self.table.get_players():
#             result += player.get_bet_chips_value()
#         return result
    
#     def get_table_config(self) -> TableConfiguration:
#         return self.table.get_table_config()

#     def get_big_blind(self) -> PlayerId:
#         return None
    
#     def get_small_blind(self) -> PlayerId:
#         return None

#     # def accept_history_visitor(self, visitor: GameStateVisitor, start: GameState) -> None:
#     #     if start != self:
#     #         self.accept_visitor(visitor)

#     # def accept_visitor(self, visitor: GameStateVisitor) -> None:
#     #     visitor.visit_initial_game_state(self)

#     def __str__(self) -> str:
#         return str(self.table)