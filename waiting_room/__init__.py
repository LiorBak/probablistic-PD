from otree.api import BaseSubsession, BasePlayer, BaseConstants, BaseGroup, Page


doc = """
Exclusion and Results App
"""


class C(BaseConstants):
    NAME_IN_URL = 'waiting_room'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class ForwardLink(Page):
    pass


page_sequence = [ForwardLink]
