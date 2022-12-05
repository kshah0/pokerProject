from abc import ABC
from gametree.playerstate.player_state import PlayerState


class AbstractPlayerState(PlayerState, ABC):
    def is_all_in(self) -> bool:
        return (
            self.has_been_dealt() 
            and self.get_stack() == 0
        )

    def is_actively_playing(self) -> bool:
        return (
            self.has_been_dealt()
            and not self.has_folded()
            and not self.is_all_in()
        )