from gametree.gamestate.forwarding_game_state import ForwardingGameState
from gametree.gamestate.game_state import GameState
from gametree.gamestate.modifiers.events.next_player_event import NextPlayerEvent
from gametree.playerstate.player_id import PlayerId


class NextPlayerState(ForwardingGameState):

    event: NextPlayerEvent

    def __init__(self, game_state: GameState, event: NextPlayerEvent) -> None:
        super().__init__(game_state)
        self.event = event

    def get_next_to_act(self) -> PlayerId:
        return self.event.player_id

    def get_last_event(self):
        return self.event

    def __str__(self) -> str:
        return "" + self.get_previous_game_state()