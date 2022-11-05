from card import Card
from hand_ranking import HandRanking
from player_hand import PlayerHand
from game_deck import GameDeck
from player_interface import Player, PlayerAction
from typing import List, Tuple
import random

# Used to simulate a single hand of a full poker game
class GameHand:
    # Assumes we play 1/2 NLHE
    relative_sb_value = 0.5

    def __init__(self, players: List[Player], button_position: int):
        num_players = len(players)
        self.num_players = num_players
        self.players = players
        self.button_position = button_position
        # Math for positions to make it easier later
        self.bb_position = (button_position + 2) % num_players if num_players > 2 else button_position^1
        self.sb_position = (self.bb_position - 1 + num_players) % num_players
        # Create game deck
        self.deck = GameDeck(num_players)
        # Initialize values necessary for preflop
        players[self.bb_position].current_bet = min(1, players[self.bb_position].stack_size)
        players[self.bb_position].stack_size = max(0, players[self.bb_position].stack_size - 1)
        players[self.sb_position].current_bet = min(self.relative_sb_value, players[self.sb_position].stack_size)
        players[self.sb_position].stack_size = max(0, players[self.sb_position].stack_size - self.relative_sb_value)
        self.pot_size = self.current_bets[self.bb_position] + self.current_bets[self.sb_position]
    
    def sim_betting_round(self, preflop: bool = False):
        first_loop = True
        # Indicate player closest to button (or big blind in case of preflop) as last aggressor
        last_aggro = self.button_position if not preflop else self.bb_position
        while not self.players[last_aggro].active:
            last_aggro = (last_aggro - 1 + self.num_players) % self.num_players
        # Figure out who goes first on this rotation
        if preflop:
            self.current_turn = (self.button_position + 3) % self.num_players if self.num_players > 2 else self.button_position
        else:
            self.current_turn = self.sb_position
            while not self.players[self.current_turn].active:
                self.current_turn = (self.current_turn + 1) % self.num_players
        # Loop until everyone is in with the same money or folds
        while last_aggro != self.current_turn or (last_aggro == self.current_turn and first_loop):
            if not self.players[self.current_turn].active:
                self.current_turn = (self.current_turn + 1) % self.num_players
                continue
            todo = self.players[self.current_turn].action(self.current_turn, self.players, self.deck, self.pot_size)
            # Update internal state of game
            self.pot_size += todo[1]
            if todo[0] == PlayerAction.RAISE:
                last_aggro = self.current_turn
                first_loop = False
            # Case to catch limping from all parties involved
            if last_aggro == self.current_turn and todo[0] == PlayerAction.CHECK:
                break
            self.current_turn = (self.current_turn + 1) % self.num_players
        # Reset current bet sizings to 0 and add end state to hand history
        for player in self.players:
            # Second element of tuple is for cumulative information to be used later
            player.history.append((PlayerAction.END_OF_STREET, player.current_bet))
            player.current_bet = 0

    # Find the winning player(s) and their hand(s) as well as how much they won
    def get_winners(self) -> Tuple(List[Tuple(int, PlayerHand, List[Card])], float):
        # First check if only one player is active
        active_player = -1
        for i in range(self.num_players):
            player = self.players[i]
            if player.active:
                if active_player != -1:
                    active_player = -1
                    break
                active_player = i
        if active_player != -1:
            player = self.players[active_player]
            return ([active_player, player.hand, player.hand.get_best_hand(self.deck.get_board())[2]], self.pot_size)

        # Now verify showdown value
        best = (HandRanking.HIGH_CARD, [], [])
        winners = []
        for i in range(self.num_players):
            player = self.players[i]
            if player.active:
                hand = player.hand.get_best_hand(self.deck.get_board())
                if hand[0] > best[0] or (hand[0] == best[0] and hand[1] > best[1]):
                    best = hand
                    winners = []
                if hand[0] == best[0] and hand[1] == best[1]:
                    winners.append((i, player.hand, hand[2]))
        return (winners, self.pot_size / len(winners))

    # Get the number of players still in a hand
    def get_active_player_count(self):
        cnt = 0
        for player in self.players:
            if player.active:
                cnt += 1
        return cnt

    # Run a full hand for all players
    def run_game(self):
        # Preflop
        self.sim_betting_round(preflop=True)
        # Check multiple people are still in
        if self.get_active_player_count() == 1:
            return
        for street in range(3):
            # Street
            self.sim_betting_round(preflop=False)
            # Check multiple people are still in
            if self.get_active_player_count() == 1:
                return
