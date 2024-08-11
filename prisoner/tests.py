
import random
from . import InformedConsentPage, Introduction, Decision, ResultsWaitPage, Results, EndOfSuperGame, EndOfExperiment, ReadMe, Bot, C


class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number == 1:
            yield InformedConsentPage
            yield Introduction
        yield Decision, dict(cooperate=True if random.randint(0, 1) == 1 else False)
        yield Results
        if self.player.super_game_round_number == C.ROUNDS_PER_SUPERGAME:
            yield EndOfSuperGame
        if self.player.round_number == C.NUM_ROUNDS:
            yield EndOfExperiment
