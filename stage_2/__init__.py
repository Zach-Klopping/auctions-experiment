from otree.api import *
from statics import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'stage_2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    correct_answers_follow_up_quiz = QUIZ_ANSWERS["correct_answers_follow_up_quiz"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    fllw_up_Q1 = models.StringField()
    fllw_up_Q2 = models.IntegerField()
    fllw_up_Q3 = models.IntegerField()
    fllw_up_Q1_incorrect = models.IntegerField(default = 0)
    fllw_up_Q2_incorrect = models.IntegerField(default = 0)
    fllw_up_Q3_incorrect = models.IntegerField(default = 0)
    auction_value = models.IntegerField()
    selected_bid = models.IntegerField()
    demographic_1 = models.BooleanField(blank = 0)
    demographic_2 = models.BooleanField(blank = 0)


# PAGES
class P1_1(Page):
    form_model = 'player'
    form_fields = ['selected_bid']
    def is_displayed(player):
        return player.session.config['integrated_payoff_matrix'] == True
    def vars_for_template(player):
        player.auction_value = random.choice(range(0, 501, 50))

        return {
            'integrated_payoff_matrix' : player.session.config['integrated_payoff_matrix'] == True, 
            'integrated_endowment' : player.session.config['integrated_endowment'] == True,
            'auction_value' : player.auction_value,
            'standard_instructions' : player.session.config['standard_instructions'] == True,
            'computer_opponent' : player.session.config['computer_opponent'] == True,
        }

    def js_vars(player):
        auction_value = player.auction_value
        integrated_endowment = player.session.config['integrated_endowment']
        standard_instructions = player.session.config['standard_instructions']
        computer_opponent = player.session.config['computer_opponent']

        if integrated_endowment == True:
            constant = 400
        else:
            constant = 0
        return dict(constant = constant, 
                    auction_value = auction_value, 
                    standard_instructions = standard_instructions,
                    computer_opponent = computer_opponent)


class P1_2(Page):
    def is_displayed(player):
        return player.session.config['integrated_payoff_matrix'] == False
    
    def vars_for_template(player):
        player.auction_value = random.choice(range(0, 501, 50))
        return {'auction_value' : player.auction_value}

    def js_vars(player):
        integrated_endowment = player.session.config['integrated_endowment']
        if integrated_endowment == True:
            constant = 400
        else:
            constant = 0
        auction_value = player.auction_value
        return dict(auction_value = auction_value, constant = constant, )

class P2(Page):
    form_model = 'player'
    form_fields = ['fllw_up_Q1','fllw_up_Q2','fllw_up_Q3']

    def before_next_page(player, timeout_happened):
        correct_answers = C.correct_answers_follow_up_quiz

        # Check Q1
        if str(player.fllw_up_Q1).strip().lower() != str(correct_answers['Q1']).strip().lower():
            player.fllw_up_Q1_incorrect += 1
        # Check Q2
        if str(player.fllw_up_Q2).strip() != str(correct_answers['Q2']).strip():
            player.fllw_up_Q2_incorrect += 1
        # Check Q3
        if str(player.fllw_up_Q3).strip() != str(correct_answers['Q3']).strip():
            player.fllw_up_Q3_incorrect += 1


class P3(Page):
    form_model = 'player'
    form_fields = ['demographic_1','demographic_2']


class P4(Page):
    pass


page_sequence = [P1_1, P1_2, P2, P3, P4]
