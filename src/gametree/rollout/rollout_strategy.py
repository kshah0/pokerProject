from abc import ABC
import copy
import random
from typing import List, Set

from card import Card
from gametree.gamestate.game_state import GameState
from gametree.playerstate.player_id import PlayerId
from gametree.playerstate.player_state import PlayerState


class RollOutStrategy(ABC):
    # Static variables
    offsets: List[int] = [0, 1277, 4137, 4995, 5853, 5863, 7140, 7296, 7452]
    cards: List[Card] = [
        Card(rank[0] + suit)
        for rank in sorted(Card.card_order_dict.items(), key=lambda x: x[1])
        for suit in Card.suits
    ]
    # TODO: Figure out wtf this code does
    # final static int[] handRanks;
	# static {
	# 	handRanks = StateTableEvaluator.getInstance().handRanks;
	# }
    game_state: GameState
    bot_state: PlayerState
    bot_id: PlayerId
    all_players: Set[PlayerState]
    active_opponents: Set[PlayerState]
    game_pot_size: int
    bot_card_1: Card
    bot_card_2: Card
    used_fixed_community_and_bot_cards: Set[Card]
    used_fixed_community_cards: Set[Card]
    fixed_rank: int
    num_missing_community_cards: int

    def __init__(self, game_state: GameState, bot_id: PlayerId) -> None:
        self.bot_id = bot_id
        self.game_state = game_state
        self.bot_state = self.game_state.get_player(bot_id)
        self.all_players = self.game_state.get_all_seated_players()
        self.active_opponents = self.get_active_opponents(self.all_players)

        self.game_pot_size = self.game_state.get_game_pot_size()
        self.bot_card_1, self.bot_card_2 = tuple(self.bot_state.cards)

        self.used_fixed_community_cards = self.game_state.get_community_cards()
        self.used_fixed_community_and_bot_cards = self.get_set_of(
            self.bot_card_1, self.bot_card_2, self.used_fixed_community_cards
        )

        fixed_rank_builder = 53
        for card in self.used_fixed_community_cards:
            fixed_rank_builder = self.update_intermediate_rank(fixed_rank_builder, card)
        self.fixed_rank = fixed_rank_builder
        self.num_missing_community_cards = 5 - len(self.used_fixed_community_cards)

    def get_final_rank(
        self,
        community_rank: int,
        hand_card_1: Card,
        hand_card_2: Card,
    ) -> int:
        return self.extract_final_rank(
            self.update_intermediate_rank(
                self.update_intermediate_rank(
                    community_rank, hand_card_1
                ),
                hand_card_2
            )
        )

    def calc_amount_won(
        self,
        bot_state: PlayerState,
        max_opponent_win: int,
        drawers: Set[PlayerState],
        players: Set[PlayerState],
    ) -> int:
        bot_investment = bot_state.get_total_investment()
        if max_opponent_win >= bot_investment:
            # Won nothing
            return 0
        elif len(drawers) == 0:
            # won something, no draw
            if max_opponent_win == 0 and not bot_state.is_all_in():
                # just win everything
                return self.game_pot_size
            else:
                # Calculate from individual contributions
                total_to_distribute = 0
                for player in players:
                    total_to_distribute += max(
                        0,
                        min(bot_investment, player.get_total_investment()) - max_opponent_win
                    )
                return total_to_distribute
        else:
            # Won something but must share
            my_share = 0
            distributed = max_opponent_win
            num_drawers = len(drawers) + 1
            for drawer in drawers:
                limit = min(bot_investment, drawer.get_total_investment())
                if limit > distributed:
                    total_to_distribute = 0
                    for player in players:
                        total_to_distribute += max(
                            0,
                            min(limit, player.get_total_investment()) - distributed
                        )
                    my_share += total_to_distribute / num_drawers
                    distributed = limit
                num_drawers -= 1
            return int(my_share + bot_investment - distributed)

  # TODO: Figure out where this is used and implement in python
 	# protected static Comparator<PlayerState> playerComparatorByInvestment = new Comparator<PlayerState>() {

	# 	@Override
	# 	public int compare(PlayerState o1, PlayerState o2) {
	# 		int o1i = o1.getTotalInvestment();
	# 		int o2i = o2.getTotalInvestment();
	# 		if (o1i == o2i) {
	# 			return o1.hashCode() - o2.hashCode();
	# 		}
	# 		return o1i - o2i;
	# 	}

	# };

    def draw_new_card(self, used_cards: Set[Card]) -> Card:
        while True:
            community_card = self.get_random_card()
            if community_card not in used_cards:
                break
        used_cards.add(community_card)
        return community_card

    def extract_final_rank(self, rank: int) -> int:
        # TODO: Check that this code is equivalent
        # int type = (rank >>> 12) - 1;
		# rank = rank & 0xFFF;
		# return offsets[type] + rank - 1;
        offset_type = ((rank & 0xffffffff) >> 12) - 1
        rank = rank & 0xFFF
        return RollOutStrategy.offsets[offset_type] + rank - 1

    def get_active_opponents(self, all_players: Set[PlayerState]) -> Set[PlayerState]:
        opponents_that_can_win = set()
        for player_state in all_players:
            if (
                not player_state.has_folded() and
                not player_state.player_id == self.bot_id
            ):
                opponents_that_can_win.add(player_state)
        return opponents_that_can_win

    def get_random_card(self) -> Card:
        return random.choice(self.cards)

    def get_set_of(
        self,
        bot_card_1: Card,
        bot_card_2: Card,
        used_fixed_community_cards: Set[Card],
    ) -> Set[Card]:
        used_fixed_community_and_bot_cards = copy.deepcopy(used_fixed_community_cards)
        used_fixed_community_and_bot_cards.add(bot_card_1)
        used_fixed_community_and_bot_cards.add(bot_card_2)
        return used_fixed_community_and_bot_cards

    def update_intermediate_rank(
        self,
        rank: int,
        card: Card,
    ) -> int:
        return RollOutStrategy.hand_rank[self.cards.index(card) + 1 + rank]

    def get_upper_win_bound(self) -> float:
        bot_state = self.game_state.get_player(self.bot_id)
        return self.game_state.get_game_pot_size() + bot_state.get_stack()