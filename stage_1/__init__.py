from otree.api import *
import random

doc = '''Instructions and Game for Second-Price Auction Experiment'''

class C(BaseConstants):
    NAME_IN_URL = 'stage_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    # Follow up Quiz Answers
    correct_answers_follow_up_quiz = {
        'Q1': 'emily',
        'Q2': '0',
        'Q3': '29',
    }


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if 'treatment_list' not in subsession.session.vars:

        # Set the number of players per treatment
        number_in_treatment = subsession.session.config.get('number_in_treatment')

        # Create a dictionary to store which treatments are enabled based on session config
        possible_treatments = {
            'control_isolated': subsession.session.config.get('control_isolated'),
            'control_integrated': subsession.session.config.get('control_integrated'),
            'table_isolated': subsession.session.config.get('table_isolated'),
            'table_integrated': subsession.session.config.get('table_integrated'),
            'no_auction_isolated': subsession.session.config.get('no_auction_isolated'),
            'no_auction_integrated': subsession.session.config.get('no_auction_integrated'),
            'computer_isolated': subsession.session.config.get('computer_isolated'),
            'computer_integrated': subsession.session.config.get('computer_integrated'),
        }

        treatments = []

        # Loop through each treatment name and check if it is enabled
        for treatment_name in possible_treatments:
            is_enabled = possible_treatments[treatment_name]

            # If treatment is enabled, add it multiple times to the treatments list
            if is_enabled:
                repeated_treatments = [treatment_name] * number_in_treatment
                treatments.extend(repeated_treatments)

    random.shuffle(treatments)
    subsession.session.vars['treatment_list'] = treatments
    subsession.session.vars['treatment_index'] = 0

    for player in subsession.get_players():
        i = subsession.session.vars['treatment_index']
        player.treatment = subsession.session.vars['treatment_list'][i]
        subsession.session.vars['treatment_index'] += 1

        # Define sets of treatments for each boolean
        integrated_endowment_treatments = {
            'control_integrated',
            'table_integrated',
            'no_auction_integrated',
            'computer_integrated',
        }

        integrated_matrix_treatments = {
            'table_integrated',
            'table_isolated',
            'no_auction_integrated',
            'no_auction_isolated',
            'computer_integrated',
            'computer_isolated',
        }

        auction_instructions_treatments = {
            'table_integrated',
            'table_isolated',
            'control_integrated',
            'control_isolated',
        }

        computer_instructions_treatments = {
            'computer_integrated',
            'computer_isolated',
        }

        game_instructions_treatments = {
            'no_auction_integrated',
            'no_auction_isolated',
        }

        # Checks if booleans are true
        player.integrated_endowment = player.treatment in integrated_endowment_treatments
        player.integrated_matrix = player.treatment in integrated_matrix_treatments
        player.auction_instructions = player.treatment in auction_instructions_treatments
        player.computer_instructions = player.treatment in computer_instructions_treatments
        player.game_instructions = player.treatment in game_instructions_treatments


    if 'auction_values_list' not in subsession.session.vars:
        auction_instructions_enabled = (
            subsession.session.config.get('table_integrated') or
            subsession.session.config.get('table_isolated') or
            subsession.session.config.get('control_integrated') or
            subsession.session.config.get('control_isolated') or 
            subsession.session.config.get('computer_integrated') or 
            subsession.session.config.get('computer_isolated')
        )

        if auction_instructions_enabled:
            values = list(range(0, 501, 50))
        else:
            values = list(range(0, 11))

        enabled_treatments = sum(1 for enabled in possible_treatments.values() if enabled)

        auction_values = []
        for _ in range(enabled_treatments):
            for v in values:
                auction_values.extend([v] * 10)
        random.shuffle(auction_values)

        subsession.session.vars['auction_values_list'] = auction_values
        subsession.session.vars['auction_values_index'] = 0

    for player in subsession.get_players():
        i = subsession.session.vars['auction_values_index']
        player.auction_value = subsession.session.vars['auction_values_list'][i]
        subsession.session.vars['auction_values_index'] += 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatments
    treatment = models.StringField()
    integrated_endowment = models.BooleanField()
    integrated_matrix = models.BooleanField()
    auction_instructions = models.BooleanField()
    computer_instructions = models.BooleanField()
    game_instructions = models.BooleanField()

    # Participant ID
    prolific_id = models.StringField()

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
    instruction_value = models.IntegerField()
    auction_value = models.IntegerField()
    selected_bid = models.IntegerField()

    # Quiz 
    quiz_value = models.IntegerField()
    correct_answer_1 = models.IntegerField()
    correct_answer_2 = models.IntegerField()
    correct_answer_3 = models.BooleanField()
    Q1_number_1 = models.IntegerField()
    Q1_number_2 = models.IntegerField()
    Q2_number_1 = models.IntegerField()
    Q2_number_2 = models.IntegerField()

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
    def before_next_page(player, timeout_happened):
        player.prolific_id = player.participant.label


class P3(Page):
    ''' Instructions: Introduction (ID)'''

    def vars_for_template(player):
        return {
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'game_instructions' : player.game_instructions
        }


class P4(Page):
    '''Instructions: Values'''
    def vars_for_template(player):
        return {
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'game_instructions' : player.game_instructions
        }


class P5(Page):
    '''Instructions: Payoffs'''
    def vars_for_template(player):
        return {
            'auction_instructions' : player.auction_instructions,
            'game_instructions' : player.game_instructions,
            'computer_instructions' : player.computer_instructions
        }


class P6(Page):
    '''Payoff Example'''
    def before_next_page(player, timeout_happened):
        if player.game_instructions:
            player.instruction_value = random.choice(range(3, 7, 1))
        else:
            player.instruction_value = random.choice(range(150, 351, 50))



class P7(Page):
    '''Instructions: Payoff Table/Calculator'''
    def js_vars(player):
        integrated_endowment = player.integrated_endowment
        if integrated_endowment == True:
            constant = 650
        else:
            constant = 0
        return dict(constant = constant, 
                    auction_instructions = player.auction_instructions, 
                    instruction_value = player.instruction_value, 
                    computer_instructions = player.computer_instructions)
    
    def vars_for_template(player):
        return {
            'integrated_endowment' : player.integrated_endowment,
            'instruction_value' : player.instruction_value,
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'integrated_matrix' : player.integrated_matrix,
            'game_instructions' : player.game_instructions
        }
    
    @staticmethod
    def live_method(player: Player, data):
        if data.get('select_value') == 'select_value':
            player.stg1_value_dropdown_click += 1


class P8(Page):
    '''Attention Check 1'''
    form_model = 'player'
    form_fields = ['attn_check_1']
    def before_next_page(player, timeout_happened):
        if player.integrated_endowment:
            constant = 650
        else:
            constant = 0

        if player.game_instructions:
            player.quiz_value = random.choice(range(3, 7, 1))
            player.Q1_number_1 = random.choice(range(0, player.quiz_value + 1, 1))
            player.Q1_number_2 = random.choice(range(player.quiz_value, 11, 1))
            player.Q2_number_1 = random.choice(range(player.quiz_value, 11, 1))
            player.Q2_number_2 = random.choice(range(0, player.quiz_value + 1, 1))
            player.correct_answer_1 = constant
            player.correct_answer_2 = constant + (player.quiz_value - player.Q2_number_2) 
            player.correct_answer_3 = True 
        else:
            player.quiz_value = random.choice(range(150, 351, 50))
            player.Q1_number_1 = random.choice(range(0, player.quiz_value + 1, 50))
            player.Q1_number_2 = random.choice(range(player.quiz_value, 501, 50))
            player.Q2_number_1 = random.choice(range(player.quiz_value, 501, 50))
            player.Q2_number_2 = random.choice(range(0, player.quiz_value + 1, 50))
            player.correct_answer_1 = constant
            player.correct_answer_2 = constant + (player.quiz_value - player.Q2_number_2)
            player.correct_answer_3 = True 


class P9(Page):
    '''Comprehension Quiz'''
    def vars_for_template(player):
        return {
            'integrated_matrix' : player.integrated_matrix,
            'integrated_endowment' : player.integrated_endowment,
            'auction_instructions' : player.auction_instructions,
            'instruction_value' : player.instruction_value,
            'quiz_value' : player.quiz_value,
            'computer_instructions' : player.computer_instructions,
            'game_instructions' : player.game_instructions,
            'Q1_number_1' : player.Q1_number_1,
            'Q1_number_2': player.Q1_number_2,
            'Q2_number_1': player.Q2_number_1,
            'Q2_number_2': player.Q2_number_2,
        }
    
    def js_vars(player):
        if player.integrated_endowment == True:
            constant = 650
        else:
            constant = 0
        return dict(constant = constant, 
                    quiz_value = player.quiz_value,
                    instruction_value = player.instruction_value,
                    auction_instructions = player.auction_instructions,
                    computer_instructions = player.computer_instructions,
                    correct_answers_quiz1={'Q1': player.correct_answer_1, 'Q2': player.correct_answer_2, 'Q3': player.correct_answer_3})
    
    @staticmethod
    def live_method(player: Player, data):
        if data.get('select_value') == 'select_value':
            player.stg1_value_dropdown_click += 1

        if data.get('submit_quiz') == 'submit_quiz':
            answers_quiz1 = data.get('answers_quiz1', {})

            if answers_quiz1.get('Q1') != player.correct_answer_1:
                player.Q1_incorrect += 1

            if answers_quiz1.get('Q2') != player.correct_answer_2:
                player.Q2_incorrect += 1
                
            if answers_quiz1.get('Q3') != player.correct_answer_3:
                player.Q3_incorrect += 1

            if player.Q1_incorrect >= 2 or player.Q2_incorrect >= 2 or player.Q3_incorrect >= 2:
                return {player.id_in_group: {'advance_page': True}}


class P10(Page):
    '''Attention Check 2'''
    form_model = 'player'
    form_fields = ['attn_check_2']


class P11(Page):
    '''Optional Kickout Page'''
    def is_displayed(player):
        if player.attn_check_1 == 1 and player.attn_check_2 == 1:
            return True


class P12_1(Page):
    '''Auction/Game with Matrix'''
    form_model = 'player'
    form_fields = ['selected_bid']
    def is_displayed(player):
        return player.integrated_matrix
    
    def vars_for_template(player):
        return {
            'integrated_matrix' : player.integrated_matrix,
            'integrated_endowment' : player.integrated_endowment,
            'auction_value' : player.auction_value,
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'instruction_value' : player.instruction_value,
            'game_instructions' : player.game_instructions
        }

    def js_vars(player):
        integrated_endowment = player.integrated_endowment
        if integrated_endowment == True:
            constant = 650
        else:
            constant = 0
        return dict(constant = constant, 
                    auction_value = player.auction_value, 
                    instruction_value = player.instruction_value,
                    auction_instructions = player.auction_instructions,
                    computer_instructions = player.computer_instructions)

    @staticmethod
    def live_method(player: Player, data):
        if data.get('select_value') == 'select_value':
            player.stg2_value_dropdown_click += 1


class P12_2(Page):
    '''Auction Without Matrix'''
    form_model = 'player'
    form_fields = ['selected_bid']
    def is_displayed(player):
        return not player.integrated_matrix
    
    def vars_for_template(player):
        return {
            'integrated_matrix' : player.integrated_matrix,
            'integrated_endowment' : player.integrated_endowment,
            'auction_value' : player.auction_value,
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'instruction_value' : player.instruction_value,
            'game_instructions' : player.game_instructions
        }

    def js_vars(player):
        integrated_endowment = player.integrated_endowment
        if integrated_endowment == True:
            constant = 650
        else:
            constant = 0
        auction_value = player.auction_value
        return dict(auction_value = auction_value, 
                    constant = constant,         
                    instruction_value = player.instruction_value,
                    auction_instructions = player.auction_instructions)
    
    @staticmethod
    def live_method(player: Player, data):
        if data.get('select_value') == 'select_value':
            player.stg2_value_dropdown_click += 1


class P13(Page):
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


class P14(Page):
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


class P15(Page):
    '''Submitting Payment'''
    def vars_for_template(player):        
        return {
            'auction_instructions' : player.auction_instructions,
            'game_instructions' : player.game_instructions
        }

class P16(Page):
    '''Redirect Page'''
    def js_vars(player):
        return dict(
                completionlink=player.subsession.session.config['completionlink'])    

page_sequence = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12_1, P12_2, P13, P14, P15, P16]