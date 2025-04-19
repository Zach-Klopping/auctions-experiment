from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'stage_2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    fllw_up_Q1 = models.StringField()
    fllw_up_Q2 = models.IntegerField()
    fllw_up_Q3 = models.IntegerField()
    auction_value = models.IntegerField()


# PAGES
class P1(Page):
    def vars_for_template(player):
        player.auction_value = random.choice(range(0, 501, 50))  # ensures js_vars uses the same one

        return {
            'integrated_payoff_matrix' : player.session.config['integrated_payoff_matrix'] == True, 
            'integrated_endowment' : player.session.config['integrated_endowment'] == True,
            'auction_value' : player.auction_value

        }

    def js_vars(player):
        auction_value = player.auction_value
        integrated_endowment = player.session.config['integrated_endowment']
        if integrated_endowment == True:
            constant = 400
        else:
            constant = 0
        return dict(constant=constant, auction_value = auction_value)


class P2(Page):
    form_model = 'player'
    form_fields = ['fllw_up_Q1','fllw_up_Q2','fllw_up_Q3']

class P3(Page):
    pass


page_sequence = [P1, P2, P3]
