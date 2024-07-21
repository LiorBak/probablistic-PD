
from otree.api import *
c = cu

doc = '\nThis is a one-shot "Prisoner\'s Dilemma". Two players are asked separately\nwhether they want to cooperate or defect. Their choices directly determine the\npayoffs.\n'
class C(BaseConstants):
    NAME_IN_URL = 'prisoner'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 20
    ROUNDS_PER_SUPERGAME = 10
    PAYOFF_DC = cu(30)
    PAYOFF_CC = cu(20)
    PAYOFF_DD = cu(10)
    PAYOFF_CD = cu(0)
    PAYOFF_DC_HIGH = cu(300)
    PAYOFF_DC_LOW = cu(0)
    PAYOFF_DC_PROB_LOW = 0.9
    PAYOFF_CD_HIGH = cu(30)
    PAYOFF_CD_LOW = cu(-270)
    PAYOFF_CD_PROB_HIGH = 0.9
    IS_TEST = True
    DESICION_TIMEOUT = 15
    PENALTY = cu(5)
    SHOW_UP_FEE = 5
    BONUS_FEE = 5
    INSTRUCTIONS_TEMPLATE = 'prisoner/instructions.html'
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    
    if subsession.round_number == 1:
        for p in subsession.get_players():
            participant = p.participant
            participant.is_dropout = False  # may be changed in func "is_player_dropout(player)"
    
    # ------------------ set the game for 6 players ---------------
    # only activated if this is not a test
    if C.IS_TEST:
        return
    # -------------------------------------------------------------
    
    import math
    
    group_matrices = [
        [[1, 2], [3, 4], [5, 6]],
        [[1, 3], [2, 5], [4, 6]],
        [[1, 4], [2, 6], [3, 5]],
        [[1, 5], [2, 4], [3, 6]],
        [[1, 6], [2, 3], [4, 5]],
    ]
    
    for s in subsession.in_rounds(1, C.NUM_ROUNDS):
        super_game_number = math.floor((s.round_number-1) / C.ROUNDS_PER_SUPERGAME)
        s.set_group_matrix(group_matrices[super_game_number])
    
def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    print('in group by arrival time method')
    for player in waiting_players:
        if waiting_too_long(player):
            print("waiting too long")
            #mark opponent as dropout, so that in future rounds we'll skip him.
            other_player(player).participant.is_dropout = True
            # make a single-player group.
            return [player]
            #forward player as if he finished all rounds in this supergame
    
class Group(BaseGroup):
    pass
def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)
class Player(BasePlayer):
    cooperate = models.BooleanField(choices=[[True, 'Cooperate'], [False, 'Defect']], doc='This player s decision', widget=widgets.RadioSelect)
    opponent_id_in_session = models.StringField(initial='')
    game_type = models.StringField(initial='pPD')
    forgone_payoff = models.CurrencyField()
    opponent_cooperate = models.BooleanField()
    opponent_payoff = models.CurrencyField()
    opponent_number = models.StringField(initial='A')
    super_game_round_number = models.IntegerField()
    decision_time = models.FloatField()
    penalty = models.CurrencyField(initial=0)
    opponent_penaly = models.CurrencyField(initial=0)
    total_score = models.CurrencyField(initial=0)
    Email = models.StringField(label='Your e-mail address @exeter (needed for payment and contact)')
    chance_to_win_bonus = models.FloatField()
    win_bonus = models.BooleanField()
    total_experiment_payoffGDP = models.FloatField()
    is_pass = models.IntegerField(label='   ')
def other_player(player: Player):
    group = player.group
    return player.get_others_in_group()[0]
def set_payoff(player: Player):
    if player.field_maybe_none('cooperate') is None:
        return  # for the last 3 rounds of risk preferences survey
    
    import random
    
    other = other_player(player)
    if player.game_type == "PD":
        payoff_matrix = {
                (False, True): C.PAYOFF_DC,
                (True, True): C.PAYOFF_CC,
                (False, False): C.PAYOFF_DD,
                (True, False): C.PAYOFF_CD,
        }
        player.payoff = payoff_matrix[(player.cooperate, other.cooperate)]
        player.forgone_payoff = payoff_matrix[(not player.cooperate, other.cooperate)]
    
    if player.game_type == "CG":
        payoff_matrix = {
                (False, True): C.PAYOFF_CD,
                (True, True): C.PAYOFF_CC,
                (False, False): C.PAYOFF_DD,
                (True, False): C.PAYOFF_DC,
        }
        player.payoff = payoff_matrix[(player.cooperate, other.cooperate)]
        player.forgone_payoff = payoff_matrix[(not player.cooperate, other.cooperate)]
    
    
    if player.game_type == "pPD":
        payoff_matrix = {
                (False, True): [C.PAYOFF_DC_HIGH, 1-C.PAYOFF_DC_PROB_LOW, C.PAYOFF_DC_LOW],
                (True, True): [C.PAYOFF_CC, 1, 1],
                (False, False): [C.PAYOFF_DD, 1, 1],
                (True, False): [C.PAYOFF_CD_HIGH, C.PAYOFF_CD_PROB_HIGH, C.PAYOFF_CD_LOW],
        }
        payoff_values = payoff_matrix[(player.cooperate, other.cooperate)]
        forgone_values = payoff_matrix[(not player.cooperate, other.cooperate)]
        player.payoff = payoff_values[0] if random.random()<payoff_values[1] else payoff_values[2]
        player.forgone_payoff = forgone_values[0] if random.random()<forgone_values[1] else forgone_values[2]
    
    if player.game_type == "pCG":
        payoff_matrix = {
                (True, False): [C.PAYOFF_DC_HIGH, 1-C.PAYOFF_DC_PROB_LOW, C.PAYOFF_DC_LOW],
                (True, True): [C.PAYOFF_CC, 1, 1],
                (False, False): [C.PAYOFF_DD, 1, 1],
                (False, True): [C.PAYOFF_CD_HIGH, C.PAYOFF_CD_PROB_HIGH, C.PAYOFF_CD_LOW],
        }
        payoff_values = payoff_matrix[(player.cooperate, other.cooperate)]
        forgone_values = payoff_matrix[(not player.cooperate, other.cooperate)]
        player.payoff = payoff_values[0] if random.random()<payoff_values[1] else payoff_values[2]
        player.forgone_payoff = forgone_values[0] if random.random()<forgone_values[1] else forgone_values[2]
    
    player.payoff = player.payoff - player.penalty
    player.forgone_payoff = player.forgone_payoff - player.penalty
    
    player.total_score = player.total_score + player.payoff  # total score is set to previous round when entering desicion page (func 'falues for new round')
def waiting_too_long(player: Player):
    session = player.session
    subsession = player.subsession
    group = player.group
    participant = player.participant
    if player.round_number < 4:
        return False  # because first 3 rounds have longer waiting time
    
    # Called from ResultsWaitPage every time the player gets there, with a fixed delay of some seconds
    participant = player.participant
    
    # this function is being called from the ssubsession's group_by_arrival_time_method function. The last should be refreshed once ot twice a miniute, thus detecting over-wait.
    
    import time
    # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
    return time.time() - participant.wait_page_arrival > C.DESICION_TIMEOUT * 2 #seconds
def values_for_new_round(player: Player):
    player.super_game_round_number = ((player.round_number-1) % C.ROUNDS_PER_SUPERGAME) + 1 # The calculations intends to get round 10 = super_game round 10 instead of 0.
    is_new_opponent = (player.super_game_round_number == 1)
    
    if player.round_number > 1:
        #set repeeting values
        player.game_type = player.in_round(1).game_type
        player.opponent_number = player.in_round(player.round_number - 1).opponent_number
        player.total_score = player.in_round(player.round_number - 1).total_score
        # set charecter to visualize opponent
        if is_new_opponent:
            player.opponent_number = chr(ord(player.opponent_number)+1) 
        else:
            player.opponent_number = player.in_round(player.round_number - 1).opponent_number
    
    
def set_desicion_time(player: Player):
    # This funtion is called at page Desicion two times: 
    # a) at vars_for_template - when page loads, b) at before_bext_page - when page ends
    import time
    
    now = time.time()
    
    if player.field_maybe_none('decision_time') == None:
        player.decision_time = now
    else:
        player.decision_time = now - player.decision_time
def is_player_dropout(player: Player):
    participant = player.participant
    if player.decision_time >= C.DESICION_TIMEOUT + 3:  # in case user closed browers the timeout didn't work - so this is how we find he dropped
        player.participant.vars['is_dropout'] = True
def calc_total_payoff(player: Player):
    import random
    
    chance_to_win = (float(player.total_score) + 1200)/4000
    player.chance_to_win_bonus = chance_to_win
    random_number = random.uniform(0, 1)
    player.win_bonus = chance_to_win > random_number
    bonus = 0
    if player.win_bonus:
        bonus = C.BONUS_FEE
    player.total_experiment_payoffGDP = C.SHOW_UP_FEE + bonus
    
    return [chance_to_win, random_number]
class InformedConsentPage(Page):
    form_model = 'player'
    form_fields = ['Email']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        # << copied from Desicion >>
        
        payoff_matrix = {}        
        
        if player.game_type == "PD":
            payoff_matrix = {
                    (False, True): C.PAYOFF_DC,
                    (True, True): C.PAYOFF_CC,
                    (False, False): C.PAYOFF_DD,
                    (True, False): C.PAYOFF_CD,
            }
        
        if player.game_type == "CG":
            payoff_matrix = {
                    (False, True): C.PAYOFF_CD,
                    (True, True): C.PAYOFF_CC,
                    (False, False): C.PAYOFF_DD,
                    (True, False): C.PAYOFF_DC,
            }    
        
        if player.game_type == "pPD":
            payoff_matrix = {
                    (False, True): [C.PAYOFF_DC_LOW, C.PAYOFF_DC_HIGH],
                    (True, True): C.PAYOFF_CC,
                    (False, False): C.PAYOFF_DD,
                    (True, False): [C.PAYOFF_CD_HIGH, C.PAYOFF_CD_LOW],
            }
        
        if player.game_type == "pCG":
            payoff_matrix = {
                    (True, False): [C.PAYOFF_DC_LOW, C.PAYOFF_DC_HIGH],
                    (True, True): C.PAYOFF_CC,
                    (False, False): C.PAYOFF_DD,
                    (False, True): [C.PAYOFF_CD_HIGH, C.PAYOFF_CD_LOW],
            }
        
        # ---- set text for desicion table according to game type----
        
        text_left = {}
        text_right = {}
        text_desc_player = {}
        text_desc_other = {}
        value_to_text = lambda v: 'get '+ str(v) if v == 0 else ('gain '+ str(v) if v > 0 else 'lose ' + str(abs(v)))
        
        if player.game_type[0] == 'p': # game is probablistic version
            for i in [0, 1]:
                for j in [0,1]:
                    ti = 'C' if i == 1 else 'D'
                    tj = 'C' if j == 1 else 'D'
                    if i != j: #and type(payoff_matrix) == list
                        text_left[f"{ti}{tj}"] = f'{payoff_matrix[(i,j)][0]} with <nobr>90% chance,</nobr> and <nobr>{payoff_matrix[(i,j)][1]} with 10% chance</nobr>'  #player
                        text_right[f"{ti}{tj}"] = f'{payoff_matrix[(j,i)][0]} with <nobr>90% chance</nobr>, and <nobr>{payoff_matrix[(j,i)][1]} with 10% chance</nobr>'  #opponent
        
                        # _______<< only for introduction >>__________
                        text_desc_player[f"{ti}{tj}"] = f'{value_to_text(payoff_matrix[(i,j)][0])} with <nobr>probability 0.9 (90% chance),</nobr> and <nobr>{value_to_text(payoff_matrix[(i,j)][1])} otherwise (10% chance)</nobr>'  #player
                        text_desc_other[f"{ti}{tj}"] = f'{value_to_text(payoff_matrix[(j,i)][0])} with <nobr>probability 0.9 (90% chance),</nobr> and <nobr>{value_to_text(payoff_matrix[(j,i)][1])} otherwise (10% chance)</nobr>'  #opponent
                        # _______<< end of 'only for introduction' >>______
                    else:
                        text_left[f"{ti}{tj}"] = f'{payoff_matrix[(i,j)]}'  #player
                        text_right[f"{ti}{tj}"] = f'{payoff_matrix[(j,i)]}' #opponent
        
        
        else:  # game is Deterministic version
            for i in [0, 1]:
                for j in [0,1]:
                    ti = 'C' if i == 1 else 'D'
                    tj = 'C' if j == 1 else 'D'
                    text_left[f"{ti}{tj}"] = f'{payoff_matrix[(i,j)]}'
                    text_right[f"{tj}{ti}"] = f'{payoff_matrix[(j,i)]}'
        
        # << end of copy from Desicion >>
        
        return dict(
            t_left = text_left,
            t_right = text_right,
            desc_player = text_desc_player,
            desc_other = text_desc_other,
        )
class Decision(Page):
    form_model = 'player'
    form_fields = ['cooperate']
    @staticmethod
    def is_displayed(player: Player):
        return True
    @staticmethod
    def vars_for_template(player: Player):
        values_for_new_round(player)
        set_desicion_time(player)
        is_new_opponent = (player.super_game_round_number == 1)
        
        # ---- set history for historical scores table -------
        history = []
        super_game_start = player.round_number + 1 - player.super_game_round_number
        for round_number in range(super_game_start, player.round_number):
                past_player = player.in_round(round_number)
                history.append(past_player)
        
        # << start copy to introduction >>
        # ---- Define payoff_matrix -------
        
        payoff_matrix = {}        
        
        if player.game_type == "PD":
            payoff_matrix = {
                    (False, True): C.PAYOFF_DC,
                    (True, True): C.PAYOFF_CC,
                    (False, False): C.PAYOFF_DD,
                    (True, False): C.PAYOFF_CD,
            }
        
        if player.game_type == "CG":
            payoff_matrix = {
                    (False, True): C.PAYOFF_CD,
                    (True, True): C.PAYOFF_CC,
                    (False, False): C.PAYOFF_DD,
                    (True, False): C.PAYOFF_DC,
            }    
        
        if player.game_type == "pPD":
            payoff_matrix = {
                    (False, True): [C.PAYOFF_DC_LOW, C.PAYOFF_DC_HIGH],
                    (True, True): C.PAYOFF_CC,
                    (False, False): C.PAYOFF_DD,
                    (True, False): [C.PAYOFF_CD_HIGH, C.PAYOFF_CD_LOW],
            }
        
        if player.game_type == "pCG":
            payoff_matrix = {
                    (True, False): [C.PAYOFF_DC_LOW, C.PAYOFF_DC_HIGH],
                    (True, True): C.PAYOFF_CC,
                    (False, False): C.PAYOFF_DD,
                    (False, True): [C.PAYOFF_CD_HIGH, C.PAYOFF_CD_LOW],
            }
        
        # ---- set text for desicion table according to game type----
        
        text_left = {}
        text_right = {}
        
        if player.game_type[0] == 'p': # game is probablistic version
            for i in [0, 1]:
                for j in [0,1]:
                    ti = 'C' if i == 1 else 'D'
                    tj = 'C' if j == 1 else 'D'
                    if i != j: #and type(payoff_matrix) == list
                        text_left[f"{ti}{tj}"] = f'{payoff_matrix[(i,j)][0]} with <nobr> 90% chance,</nobr><br>and <nobr>{payoff_matrix[(i,j)][1]}</nobr> with <nobr>10% chance<nobr>'  #player
                        text_right[f"{ti}{tj}"] = f'{payoff_matrix[(j,i)][0]} with </nobr>90% chance</nobr>,<br>and <nobr>{payoff_matrix[(j,i)][1]}</nobr> with <nobr>10% chance<nobr>'  #opponent
                    else:
                        text_left[f"{ti}{tj}"] = f'{payoff_matrix[(i,j)]}'  #player
                        text_right[f"{ti}{tj}"] = f'{payoff_matrix[(j,i)]}' #opponent
        
        else:  # game is Deterministic version
            for i in [0, 1]:
                for j in [0,1]:
                    ti = 'C' if i == 1 else 'D'
                    tj = 'C' if j == 1 else 'D'
                    text_left[f"{ti}{tj}"] = f'{payoff_matrix[(i,j)]}'
                    text_right[f"{tj}{ti}"] = f'{payoff_matrix[(j,i)]}'
        
        # << end copy to introduction >>
        # ------------------
        return dict(
            is_new_opponent = is_new_opponent,
            history = history,
            t_left = text_left,
            t_right = text_right,
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        set_desicion_time(player) # second run as the page ends
        
        import random
        #  participant.wait_page_arrival = time.time()
        
        if timeout_happened:
            player.penalty = C.PENALTY
            action = random.randint(0, 1)
            player.cooperate = action
        else:
            player.penalty = 0
    @staticmethod
    def get_timeout_seconds(player: Player):
        if (player.round_number <= 3):
            return 2*C.DESICION_TIMEOUT
        else:
             return C.DESICION_TIMEOUT
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
            # In case his opponent dropped:
            # you should be able to open the respective participant’s URL and click on the “Next” button.
            # Or just forward him with 'other_participant.is_dropout = True' then it will skip waitpages
        other_participant = other_player(player).participant
        
        if other_participant.is_dropout:
            return False
        else:
            return True
class Results(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return True
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        participant = player.participant
        opponent = other_player(player)
        player.opponent_id_in_session = str(opponent.participant.id_in_session)
        player.opponent_cooperate = opponent.cooperate
        player.opponent_payoff = opponent.payoff
        player.opponent_penaly = opponent.penalty
        
        # value_to_text = lambda v: 'got '+ str(v) if v == 0 else ('gained '+ str(v) if v > 0 else 'lost ' + str(abs(v)))
        value_to_text = lambda v: 'got '+ str(v)
        
        return dict(
            opponent=opponent,
            my_decision=player.field_display('cooperate'),
            opponent_decision=opponent.field_display('cooperate'),
            payoff_text = value_to_text(player.payoff),
            forgone_text = value_to_text(player.forgone_payoff),
            opponent_payoff = value_to_text(opponent.payoff),
            opponent_penalty = opponent.penalty,
        )
    @staticmethod
    def get_timeout_seconds(player: Player):
        if (player.round_number <= 3):
            return 2*C.DESICION_TIMEOUT
        else:
             return (2/3)*C.DESICION_TIMEOUT
class EndOfSuperGame(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.super_game_round_number == C.ROUNDS_PER_SUPERGAME
    @staticmethod
    def vars_for_template(player: Player):
        # ---- set history for historical scores table -------
        history = []
        super_game_start = player.round_number + 1 - player.super_game_round_number
        for round_number in range(super_game_start, player.round_number + 1):
                player.test = round_number
                past_player = player.in_round(round_number)
                history.append(past_player)
        
        return dict(
            history = history,
        )
    @staticmethod
    def get_timeout_seconds(player: Player):
        return C.DESICION_TIMEOUT
class EndOfExperiment(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        chance_to_win, random_number = calc_total_payoff(player)
        return dict(
            bonus_chance = chance_to_win*100,
            bonus_prob = chance_to_win,
            lottery_num = random_number,
        )
class ReadMe(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return False
page_sequence = [InformedConsentPage, Introduction, Decision, ResultsWaitPage, Results, EndOfSuperGame, EndOfExperiment, ReadMe]