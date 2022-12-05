import copy
from math import exp, isinf, isnan, log
from gametree.gamestate.game_state import GameState
from gametree.playerstate.player_id import PlayerId
from gametree.rollout.rollout_result import RolloutResult
from gametree.rollout.rollout_strategy import RollOutStrategy


class DistributionRollout(RollOutStrategy):
    rel_pot_size: int

    def __init__(self, game_state: GameState, bot_id: PlayerId) -> None:
        super().__init__(game_state, bot_id)
        self.rel_pot_size = (
            self.game_pot_size / (
                len(self.all_players) * self.game_state.get_table_config().get_big_blind()
            )
        )

    def do_rollout(
        self,
        num_community_samples: int,
        num_opponent_samples: int,
    ) -> RolloutResult:
        total_prob = 0
        drawers = set() # set of players who drew with bot
        values = dict() # dict with keys of the amount won and values of the total probability of winning that amount
        for _ in range(num_community_samples):
            community_sample_rank = self.fixed_rank
            used_community_and_bot_cards = copy.deepcopy(self.used_fixed_community_and_bot_cards)
            for _ in range(self.num_missing_community_cards):
                community_card = self.draw_new_card(used_community_and_bot_cards)
                self.community_sample_rank = self.update_intermediate_rank(
                    self.community_sample_rank,
                community_card)
            bot_rank = self.get_final_rank(self.community_sample_rank, self.bot_card_1, self.bot_card_2)
            for _ in range(num_opponent_samples):
                used_opponent_cards = copy.deepcopy(used_community_and_bot_cards)
                log_prob = 0.0
                max_opponent_win = 0
                drawers.clear()
                for opponent_that_can_win in self.active_opponents:
                    opponent_card_1 = self.draw_new_card(used_opponent_cards)
                    opponent_card_2 = self.draw_new_card(used_opponent_cards)
                    opponent_rank = self.get_final_rank(community_sample_rank, opponent_card_1, opponent_card_2)
                    if opponent_rank > bot_rank:
                        max_opponent_win = max(max_opponent_win, opponent_that_can_win.get_total_investment())
                    elif opponent_rank == bot_rank:
                        drawers.add(opponent_that_can_win)
                    opponent_rank_prob = self.get_relative_nearest_probability(opponent_rank, self.rel_pot_size)
                    log_prob += log(opponent_rank_prob)
                prob = exp(log_prob)
                won = self.calc_amount_won(self.bot_state, max_opponent_win, drawers, self.all_players)
                value = values.get(won)
                if value is None:
                    values[won] = prob
                else:
                    values[won] += prob
                total_prob += prob
        return RolloutResult(
            values,
            total_prob,
        )

    def get_relative_nearest_probability(
        self,
        rank: int,
        relative_pot_size: int
    ) -> float:
        prob = self.get_relative_probability(rank, self.rel_pot_size)
        if prob == 0:
            prob = self.get_relative_nearest_probability(rank - 1, relative_pot_size)
        if isinf(prob) or isnan(prob):
            raise RuntimeError(f"Bad opponent_rank_prob{prob}")
        return prob

    def get_relative_probability(
        self,
        rank: int,
        relative_pot_size: int,
    ) -> float:
        pass
        # TODO
