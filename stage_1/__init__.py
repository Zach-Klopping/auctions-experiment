from otree.api import *
from statics import *
import random

doc = '''Instructions and Game for Second-Price Auction Experiment'''

class C(BaseConstants):
    NAME_IN_URL = 'stage_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    # Quiz Answers from Statics File
    correct_answers_quiz1_integrated_endowment = QUIZ_ANSWERS["correct_answers_quiz1_integrated_endowment"]
    correct_answers_quiz1_no_endowment = QUIZ_ANSWERS["correct_answers_quiz1_no_endowment"]
    correct_answers_follow_up_quiz = QUIZ_ANSWERS["correct_answers_follow_up_quiz"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Participant ID
    user_id = models.StringField()

    # Ethics Check Box
    ethics = models.BooleanField()

    # Attention Check Answers
    attn_check_1 = models.BooleanField()
    attn_check_2 = models.BooleanField()

    # Comprehension Questions Incorrect Counter
    Q1_incorrect = models.IntegerField(default = 0)
    Q2_incorrect = models.IntegerField(default = 0)
    Q3_incorrect = models.IntegerField(default = 0)

    # Value For Payoff Table Dropdown Click Counter
    stg1_value_dropdown_click = models.IntegerField(default=0)
    stg2_value_dropdown_click = models.IntegerField(default=0)

    # Follow-Up Question's Answer
    fllw_up_Q1 = models.StringField()
    fllw_up_Q2 = models.IntegerField()
    fllw_up_Q3 = models.IntegerField()

    # Follow-Up Question's Incorrect Counter
    fllw_up_Q1_incorrect = models.IntegerField(default = 0)
    fllw_up_Q2_incorrect = models.IntegerField(default = 0)
    fllw_up_Q3_incorrect = models.IntegerField(default = 0)

    # Demographic Answers
    demographic_1 = models.BooleanField()
    demographic_2 = models.BooleanField()

    # Auction Value and Partcipant Bid
    auction_value = models.IntegerField()
    selected_bid = models.IntegerField()

    # Payments
    comprehension_quiz_payment = models.FloatField(default = 0.00)
    follow_up_quiz_payment = models.FloatField(default = 0.00)


class P1(Page):
    ''' Consent Page'''
    pass


class P2(Page):
    ''' Ethics Statement'''
    form_model = 'player'
    form_fields = ['ethics']


class P3(Page):
    ''' Instructions: Introduction (ID)'''
    form_model = 'player'
    form_fields = ['user_id']

    def vars_for_template(player):
        return {
            'standard_instructions' : player.session.config['standard_instructions'] == True,
        }


class P4(Page):
    '''Instructions: Values'''
    def vars_for_template(player):
        return {
            'standard_instructions' : player.session.config['standard_instructions'] == True,
            'computer_opponent' : player.session.config['computer_opponent'] == True,
        }


class P5(Page):
    '''Instructions: Payoffs'''
    def vars_for_template(player):
        return {
            'standard_instructions' : player.session.config['standard_instructions'] == True,
            'computer_opponent' : player.session.config['computer_opponent'] == True,
        }


class P6(Page):
    '''Instructions: Payoff Table/Calculator'''
    def js_vars(player):
        integrated_endowment = player.session.config['integrated_endowment']
        standard_instructions = player.session.config['standard_instructions']
        computer_opponent = player.session.config['computer_opponent']
        auction_value = 250
        if integrated_endowment == True:
            constant = 450
        else:
            constant = 0
        return dict(constant = constant, 
                    standard_instructions = standard_instructions, 
                    auction_value = auction_value, 
                    computer_opponent = computer_opponent)
    
    def vars_for_template(player):
        return {
            'integrated_endowment' : player.session.config['integrated_endowment'] == True,
            'standard_instructions' : player.session.config['standard_instructions'] == True,
            'computer_opponent' : player.session.config['computer_opponent'] == True,
            'integrated_payoff_matrix' : player.session.config['integrated_payoff_matrix'] == True
        }
    
    @staticmethod
    def live_method(player: Player, data):
        if data.get('select_value') == 'select_value':
            player.stg1_value_dropdown_click += 1
    
    
class P7(Page):
    '''Attention Check 1'''
    form_model = 'player'
    form_fields = ['attn_check_1']


class P8(Page):
    '''Comprehension Quiz'''
    def vars_for_template(player):
        return {
            'integrated_payoff_matrix' : player.session.config['integrated_payoff_matrix'] == True,
            'integrated_endowment' : player.session.config['integrated_endowment'] == True,
            'standard_instructions' : player.session.config['standard_instructions'] == True,
            'computer_opponent' : player.session.config['computer_opponent'] == True,
        }
    
    def js_vars(player):
        auction_value = 250 if player.session.config['standard_instructions'] == True else 5
        standard_instructions = player.session.config['standard_instructions']
        integrated_endowment = player.session.config['integrated_endowment']
        computer_opponent = player.session.config['computer_opponent']
        correct_answers_quiz1 = C.correct_answers_quiz1_integrated_endowment if integrated_endowment == True else C.correct_answers_quiz1_no_endowment
        if integrated_endowment == True:
            constant = 450
        else:
            constant = 0
        return dict(constant = constant, 
                    auction_value = auction_value, 
                    correct_answers_quiz1 = correct_answers_quiz1, 
                    standard_instructions = standard_instructions,
                    computer_opponent = computer_opponent)
    
    @staticmethod
    def live_method(player: Player, data):
        if data.get('select_value') == 'select_value':
            player.stg1_value_dropdown_click += 1

        if data.get('submit_quiz') == 'submit_quiz':
            answers_quiz1 = data.get('answers_quiz1', {})
            integrated_endowment = player.session.config['integrated_endowment']
            correct_answers_quiz1 = C.correct_answers_quiz1_integrated_endowment if integrated_endowment == True else C.correct_answers_quiz1_no_endowment

            if answers_quiz1.get('Q1') != correct_answers_quiz1.get('Q1'):
                player.Q1_incorrect += 1

            if answers_quiz1.get('Q2') != correct_answers_quiz1.get('Q2'):
                player.Q2_incorrect += 1
                
            if answers_quiz1.get('Q3') != correct_answers_quiz1.get('Q3'):
                player.Q3_incorrect += 1

            if player.Q1_incorrect >= 2 or player.Q2_incorrect >= 2 or player.Q3_incorrect >= 2:
                return {player.id_in_group: {'advance_page': True}}


class P9(Page):
    '''Attention Check 2'''
    form_model = 'player'
    form_fields = ['attn_check_2']
    
    def before_next_page(player: Player, timeout_happened):
        if player.session.config['standard_instructions'] == True:
            player.auction_value = random.choice(range(0, 501, 50))
        else:
            player.auction_value = random.choice(range(0, 11, 1))


class P10(Page):
    '''Optional Kickout Page'''
    def is_displayed(player):
        if player.attn_check_1 == 1 and player.attn_check_2 == 1:
            return True


class P11_1(Page):
    '''Auction/Game with Matrix'''
    form_model = 'player'
    form_fields = ['selected_bid']
    def is_displayed(player):
        return player.session.config['integrated_payoff_matrix'] == True
    
    def vars_for_template(player):
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
            constant = 450
        else:
            constant = 0
        return dict(constant = constant, 
                    auction_value = auction_value, 
                    standard_instructions = standard_instructions,
                    computer_opponent = computer_opponent)

    @staticmethod
    def live_method(player: Player, data):
        if data.get('select_value') == 'select_value':
            player.stg2_value_dropdown_click += 1


class P11_2(Page):
    '''Auction Without Matrix'''
    form_model = 'player'
    form_fields = ['selected_bid']
    def is_displayed(player):
        return player.session.config['integrated_payoff_matrix'] == False
    
    def vars_for_template(player):
        return {
            'integrated_payoff_matrix' : player.session.config['integrated_payoff_matrix'] == True, 
            'integrated_endowment' : player.session.config['integrated_endowment'] == True,
            'auction_value' : player.auction_value,
            'standard_instructions' : player.session.config['standard_instructions'] == True,
            'computer_opponent' : player.session.config['computer_opponent'] == True,
        }

    def js_vars(player):
        integrated_endowment = player.session.config['integrated_endowment']
        if integrated_endowment == True:
            constant = 450
        else:
            constant = 0
        auction_value = player.auction_value
        return dict(auction_value = auction_value, constant = constant)
    
    @staticmethod
    def live_method(player: Player, data):
        if data.get('select_value') == 'select_value':
            player.stg2_value_dropdown_click += 1


class P12(Page):
    '''Follow-Up Quiz'''
    form_model = 'player'
    form_fields = ['fllw_up_Q1','fllw_up_Q2','fllw_up_Q3']

    def before_next_page(player, timeout_happened):
        correct_answers = C.correct_answers_follow_up_quiz

        if str(player.fllw_up_Q1).strip().lower() != str(correct_answers['Q1']).strip().lower():
            player.fllw_up_Q1_incorrect += 1

        if str(player.fllw_up_Q2).strip() != str(correct_answers['Q2']).strip():
            player.fllw_up_Q2_incorrect += 1
            
        if str(player.fllw_up_Q3).strip() != str(correct_answers['Q3']).strip():
            player.fllw_up_Q3_incorrect += 1


class P13(Page):
    '''Demographics'''
    form_model = 'player'
    form_fields = ['demographic_1','demographic_2']
    def before_next_page(player, timeout_happened):
        if player.Q1_incorrect == 0 and player.Q2_incorrect == 0 and player.Q3_incorrect == 0:
            player.comprehension_quiz_payment = 0.50

        elif player.Q1_incorrect <= 1 and player.Q2_incorrect <= 1 and player.Q3_incorrect <= 1:
            player.comprehension_quiz_payment = 0.20

        else:
            player.comprehension_quiz_payment = 0.00
            
        player.follow_up_quiz_payment = 0
        
        if player.fllw_up_Q1_incorrect == 0:
            player.follow_up_quiz_payment += 0.25

        if player.fllw_up_Q2_incorrect == 0:
            player.follow_up_quiz_payment += 0.25
            
        if player.fllw_up_Q3_incorrect == 0:
            player.follow_up_quiz_payment += 0.25


class P14(Page):
    '''Submitting Payment'''
    def vars_for_template(player):        
        return {
            'standard_instructions' : player.session.config['standard_instructions'] == True
        }


page_sequence = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11_1, P11_2, P12, P13, P14]
