from otree.api import *
from statics import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'stage_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    # Quiz Answers
    correct_answers_quiz1_integrated_endowment = QUIZ_ANSWERS["correct_answers_quiz1_integrated_endowment"]
    correct_answers_quiz1_no_endowment = QUIZ_ANSWERS["correct_answers_quiz1_no_endowment"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ethics = models.BooleanField(blank=0)
    attn_check_1 = models.BooleanField(blank=0)
    attn_check_2 = models.BooleanField(blank=0)
    Q1_incorrect = models.IntegerField(default=0)
    Q2_incorrect = models.IntegerField(default=0)
    Q3_incorrect = models.IntegerField(default=0)


# PAGES
class P1(Page):
    pass


class P2(Page):
    form_model = 'player'
    form_fields = ['ethics']


class P3(Page):
    pass


class P4(Page):
    pass


class P5(Page):
    pass


class P6_1(Page):
    def is_displayed(player):
        return player.session.config['integrated_payoff_matrix'] == True
    
    def js_vars(player):
        integrated_endowment = player.session.config['integrated_endowment']
        if integrated_endowment == True:
            constant = 400
        else:
            constant = 0
        return dict(constant = constant)
    

class P6_2(Page):
    def is_displayed(player):
        return player.session.config['integrated_payoff_matrix'] == False


class P7(Page):
    form_model = 'player'
    form_fields = ['attn_check_1']


class P8(Page):
    def vars_for_template(player):
        return {
            'integrated_payoff_matrix' : player.session.config['integrated_payoff_matrix'] == True,
        }
    
    def js_vars(player):
        auction_value = 250
        integrated_endowment = player.session.config['integrated_endowment']
        correct_answers_quiz1 = C.correct_answers_quiz1_integrated_endowment if integrated_endowment == True else C.correct_answers_quiz1_no_endowment
        if integrated_endowment == True:
            constant = 400
        else:
            constant = 0
        return dict(constant = constant, auction_value = auction_value, correct_answers_quiz1 = correct_answers_quiz1)
    
    def live_method(player: Player, data):
        if data.get('action') == 'submit_quiz':
            answers_quiz1 = data.get('answers_quiz1', {})
            integrated_endowment = player.session.config['integrated_endowment']
            correct_answers_quiz1 = C.correct_answers_quiz1_integrated_endowment if integrated_endowment == True else C.correct_answers_quiz1_no_endowment

            # Check each answer and update the incorrect count for the specific question
            if answers_quiz1.get('Q1') != correct_answers_quiz1.get('Q1'):
                player.Q1_incorrect += 1
            if answers_quiz1.get('Q2') != correct_answers_quiz1.get('Q2'):
                player.Q2_incorrect += 1
            if answers_quiz1.get('Q3') != correct_answers_quiz1.get('Q3'):
                player.Q3_incorrect += 1

            if player.Q1_incorrect >= 3 or player.Q2_incorrect >= 3 or player.Q3_incorrect >= 3:
                return {player.id_in_group: {'advance_page': True}}


class P9(Page):
    form_model = 'player'
    form_fields = ['attn_check_2']


page_sequence = [P1, P2, P3, P4, P5, P6_1, P6_2, P7, P8, P9]
