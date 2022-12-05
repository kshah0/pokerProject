import copy
from typing import Dict, List, Set
from card import Card
from gametree.gamestate.abstract_game_state import AbstractGameState
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.events.new_round_event import NewRoundEvent
from gametree.playerstate.abstract_player_state import AbstractPlayerState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState
from gametree.playerstate.seat_id import SeatId
from gametree.round import Round
from gametree.table_config import TableConfiguration

class NewRoundPlayerState(AbstractPlayerState):
    def __init__(
        self,
        old_player_state: PlayerState,
    ) -> None:
        self.old_player_state = old_player_state

    def get_name(self) -> str:
        return self.old_player_state.get_name()

    def get_bet(self) -> int:
        return 0

    def get_total_investment(self) -> int:
        return self.old_player_state.get_total_investment()

    def get_cards(self) -> Set[Card]:
        return copy.deepcopy(self.old_player_state.get_cards())

    def get_stack(self) -> int:
        return self.old_player_state.get_stack()

    def has_folded(self) -> bool:
        return self.old_player_state.has_folded()

    def has_been_dealt(self) -> bool:
        return self.old_player_state.has_been_dealt()

    def get_player_id(self) -> PlayerId:
        return self.old_player_state.get_player_id()
    
    def get_seat_id(self) -> SeatId:
        return self.old_player_state.get_seat_id()

    def has_checked(self) -> bool:
        return False

    def get_bet_progression(self) -> List[int]:
        return []


class NewRoundState(AbstractGameState):
    event: NewRoundEvent
    player_states: Dict[PlayerId, PlayerState]
    dealer: PlayerId
    community_cards: Set[Card]
    table_config: TableConfiguration
    previous_round_state: GameState
    sb: PlayerId
    bb: PlayerId

    def __init__(
        self,
        game_state: GameState,
        event: NewRoundEvent
    ) -> None:
        self.event = event
        self.previous_round_state = game_state
        self.table_config = game_state.get_table_config()
        self.dealer = game_state.get_dealer()
        self.community_cards = game_state.get_community_cards()
        self.sb = game_state.get_small_blind()
        self.bb = game_state.get_big_blind()

        player_ids = game_state.seat_map.values()
        self.player_states = dict()
        for player_id in player_ids:
            old_player_state = game_state.get_player(player_id)
            player_state = NewRoundPlayerState(old_player_state)
            self.player_states[player_id] = player_state
        self.seat_map = self.previous_round_state.seat_map

    def get_table_config(self) -> TableConfiguration:
        return self.table_config

    def get_all_seated_player_ids(self) -> Set[PlayerId]:
        return set(self.player_states.keys())

    def get_community_cards(self) -> Set[Card]:
        return copy.deepcopy(self.community_cards)

    def get_dealer(self) -> PlayerId:
        return self.dealer

    def get_largest_bet(self) -> int:
        return 0

    def get_last_bettor(self) -> PlayerId:
        return None

    def get_last_event(self):
        return self.event

    def get_next_to_act(self) -> PlayerId:
        return None

    def get_min_next_raise(self) -> int:
        return self.table_config.get_small_bet()

    def get_player(self, player_id: PlayerId) -> PlayerState:
        return self.player_states[player_id]

    def get_previous_game_state(self) -> GameState:
        return self.previous_round_state

    def get_previous_rounds_pot_size(self) -> int:
        return self.event.pots.total_value
    
    def get_round(self) -> Round:
        return self.event.curr_round

    def get_round_pot_size(self) -> int:
        return 0

    def get_num_seats(self) -> int:
        return self.table_config.get_max_num_players()

    def get_num_raises(self) -> int:
        return 0

    def get_big_blind(self) -> PlayerId:
        return self.bb

    def get_small_blind(self) -> PlayerId:
        return self.sb