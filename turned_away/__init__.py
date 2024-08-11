from otree.api import BaseSubsession, BasePlayer, BaseConstants, BaseGroup, Page


doc = """
Send the students to the payment page for the turned away fee
"""


class C(BaseConstants):
    NAME_IN_URL = 'turned_away'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS
def get_fwd_url(payment, label: str):
    import base64
    import json
    data = {'computername': label, 'payment': float(payment)}

    enc_data = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
    url = "http://ph.feele.exeter.ac.uk?epd="

    return url + enc_data


# PAGES
class TurnedAway(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(
            fwd_url=get_fwd_url(
                player.session.config['turned_away_fee'],
                (participant.label or participant.code)
            )
        )


page_sequence = [TurnedAway]
