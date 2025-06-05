from otree.api import *
import random
import json
import datetime

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
    # Setting Treatment
    if 'treatment_list' not in subsession.session.vars:

        # Set the number of players per treatment
        number_in_treatment = subsession.session.config.get('number_in_treatment')

        # Create a dictionary to store which treatments are enabled based on session config
        possible_treatments = {
            'control_isolated': subsession.session.config.get('control_isolated'),
            'control_integrated': subsession.session.config.get('control_integrated'),
            'calculator_isolated': subsession.session.config.get('calculator_isolated'),
            'calculator_integrated': subsession.session.config.get('calculator_integrated'),
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

        # Randomly shuffle the full list of treatments before assigning to players
        random.shuffle(treatments)
        subsession.session.vars['treatment_list'] = treatments
        subsession.session.vars['treatment_index'] = 0  # Index to keep track of assignment

    # Assign treatments to each player sequentially from the shuffled list
    for player in subsession.get_players():
        i = subsession.session.vars['treatment_index']
        player.treatment = subsession.session.vars['treatment_list'][i]
        subsession.session.vars['treatment_index'] += 1

        # Define sets of treatments for boolean flags
        control_treatment = {
            'control_integrated',
            'control_isolated',
        }

        integrated_endowment_treatments = {
            'control_integrated',
            'calculator_integrated',
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
            'calculator_integrated',
            'calculator_isolated',
        }

        computer_instructions_treatments = {
            'computer_integrated',
            'computer_isolated',
        }

        game_instructions_treatments = {
            'no_auction_integrated',
            'no_auction_isolated',
        }

        # Set boolean attributes on player based on their assigned treatment
        player.control_instructions = player.treatment in control_treatment
        player.integrated_endowment = player.treatment in integrated_endowment_treatments
        player.integrated_matrix = player.treatment in integrated_matrix_treatments
        player.auction_instructions = player.treatment in auction_instructions_treatments
        player.computer_instructions = player.treatment in computer_instructions_treatments
        player.game_instructions = player.treatment in game_instructions_treatments

    # Setting Auction Value and Quiz Value
    if 'auction_values_list' not in subsession.session.vars or 'final_pairs' not in subsession.session.vars:
        # Check if any auction-related treatments are enabled in the session config
        standard_values_enabled = (
            subsession.session.config.get('control_integrated') or
            subsession.session.config.get('control_isolated') or
            subsession.session.config.get('table_integrated') or
            subsession.session.config.get('table_isolated') or
            subsession.session.config.get('calculator_integrated') or
            subsession.session.config.get('calculator_isolated') or 
            subsession.session.config.get('computer_integrated') or 
            subsession.session.config.get('computer_isolated')
        )

        # Set ranges of values based on whether auction instructions are enabled
        if standard_values_enabled:
            values = list(range(0, 501, 50)) 

        else:
            values = list(range(0, 11))
            
        # Count how many treatments are enabled
        enabled_treatments = sum(1 for enabled in possible_treatments.values() if enabled)

        auction_values = []
        # For each enabled treatment, add values repeated 10 times each
        for _ in range(enabled_treatments):
            for v in values:
                auction_values.extend([v] * 10)
        random.shuffle(auction_values)

        # Store the auction values and initialize the index counter
        subsession.session.vars['auction_values_list'] = auction_values
        subsession.session.vars['auction_values_index'] = 0

    # Assign auction and quiz values to each player sequentially
    for player in subsession.get_players():
        # Assign auction value
        if subsession.session.config.get('pilot'):
            player.auction_value = random.choice([100, 200, 300, 400])
        else:
            i = subsession.session.vars['auction_values_index']
            player.auction_value = subsession.session.vars['auction_values_list'][i]
            subsession.session.vars['auction_values_index'] += 1

    # Assign constant based on treatment
        if player.integrated_endowment:
            player.constant = 650
        else:
            player.constant = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Participant ID
    prolific_id = models.StringField()

    # Treatment
    treatment = models.StringField()

    # Constant, Auction Value's and Partcipant Bid
    constant = models.IntegerField()
    instruction_value = models.IntegerField()
    auction_value = models.IntegerField()
    selected_bid = models.IntegerField()

    # Ethics Check Box
    ethics = models.BooleanField()

    # Attention Check Answers
    attn_check_1 = models.BooleanField()
    attn_check_2 = models.BooleanField()

    # Comprehension Questions Incorrect Counter
    Q1_incorrect = models.IntegerField(default = 0)
    Q2_incorrect = models.IntegerField(default = 0)
    Q3_incorrect = models.IntegerField(default = 0)
    Q4_incorrect = models.IntegerField(default = 0)

    # Quiz 
    quiz_value = models.IntegerField()
    correct_answer_1 = models.IntegerField()
    correct_answer_2 = models.IntegerField()
    correct_answer_3 = models.IntegerField()
    correct_answer_4 = models.BooleanField()
    Q1_number_1 = models.IntegerField()
    Q1_number_2 = models.IntegerField()
    Q2_number_1 = models.IntegerField()
    Q2_number_2 = models.IntegerField()
    Q3_number_1 = models.IntegerField()
    Q3_number_2 = models.IntegerField()
    
    # Data Tracker
    instr_value_dropdown = models.LongStringField(initial="[]")
    quiz_value_dropdown = models.LongStringField(initial="[]")
    game_value_dropdown = models.LongStringField(initial="[]")
    instr_calculate_payoff = models.LongStringField(initial="[]")
    quiz_calculate_payoff = models.LongStringField(initial="[]")
    game_calculate_payoff = models.LongStringField(initial="[]")

    # Data tracking function
    def append_json_values(player, field_name, new_value):
        current = json.loads(getattr(player, field_name))
        current.append(new_value)
        setattr(player, field_name, json.dumps(current))

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

    # Payments
    comprehension_quiz_payment = models.FloatField(default = 0.00)
    follow_up_quiz_payment = models.FloatField(default = 0.00)
    payoff_from_auction = models.FloatField(default = 0.00)
    game_payoff = models.FloatField(initial=0)

    # Instruction Booleans
    control_instructions = models.BooleanField()
    integrated_endowment = models.BooleanField()
    integrated_matrix = models.BooleanField()
    auction_instructions = models.BooleanField()
    computer_instructions = models.BooleanField()
    game_instructions = models.BooleanField()

    # Timestamps
    page_timestamps = models.LongStringField(initial='[]')
    page_enter_time = models.StringField()
    current_page_name = models.StringField()
    total_time_spent = models.FloatField()

    # Feedback
    feedback_bool = models.BooleanField()
    feedback_text = models.LongStringField(blank=True)


def track_timestamps(player, timeout_happened):
    enter_time_str = player.field_maybe_none('page_enter_time')
    submit_time = datetime.datetime.utcnow().isoformat()

    try:
        start = datetime.datetime.fromisoformat(enter_time_str)
        end = datetime.datetime.fromisoformat(submit_time)
        duration = (end - start).total_seconds()
    except Exception as e:
        duration = None

    data = json.loads(player.page_timestamps or "[]")
    data.append({
        "page": player.current_page_name,
        "duration": duration
    })
    player.page_timestamps = json.dumps(data)

    if player.current_page_name == 'Payment':
        total_seconds = round(sum(item["duration"] for item in data if item["duration"] is not None))
        total_minutes = total_seconds / 60
        player.total_time_spent = round(total_minutes, 2)


class P1(Page):
    ''' Consent Page'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)

    def vars_for_template(player):
        return {'page_name': 'Consent'}


class P2(Page):
    ''' Ethics Statement'''
    form_model = 'player'
    form_fields = ['ethics', 'page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {'page_name': 'Ethics'}
    
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)
        player.prolific_id = player.participant.label


class P3(Page):
    ''' Instructions: Introduction (ID)'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {
            'page_name': 'Introduction',
            'control_instructions' : player.control_instructions,
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'game_instructions' : player.game_instructions
        }
    
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P4(Page):
    '''Instructions: Values'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {
            'page_name': 'Values',
            'control_instructions' : player.control_instructions,
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'game_instructions' : player.game_instructions
        }
    
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P5(Page):
    '''Instructions: Payoffs'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {
            'page_name': 'Payoffs',
            'auction_instructions' : player.auction_instructions,
            'control_instructions' : player.control_instructions,
            'game_instructions' : player.game_instructions,
            'computer_instructions' : player.computer_instructions
        }
    
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P6(Page):
    '''Instructions: Payoff Example'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {'page_name': 'Payoff Example'}

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)
        if player.game_instructions:
            player.instruction_value = 6
        else:
            player.instruction_value = 300


class P7(Page):
    '''Instructions: Payoff Table/Calculator'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def is_displayed(player):
        if player.control_instructions:
            return False
        else:
            return True

    def js_vars(player):
        return dict(constant = player.constant, 
                    auction_instructions = player.auction_instructions, 
                    instruction_value = player.instruction_value, 
                    computer_instructions = player.computer_instructions)
    
    def vars_for_template(player):
        return {
            'page_name': 'Payoff Matrix',
            'integrated_endowment' : player.integrated_endowment,
            'instruction_value' : player.instruction_value,
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'integrated_matrix' : player.integrated_matrix,
            'game_instructions' : player.game_instructions
        }
    
    @staticmethod
    def live_method(player: Player, data):
        if player.integrated_matrix:
            if 'dropdown_value' in data:
                value = data['dropdown_value']
                existing = json.loads(getattr(player, 'instr_value_dropdown')) or []
                index = len(existing) + 1
                player.append_json_values('instr_value_dropdown', {'index': index, 'value': value})
        else:
            if 'your_bid_value' in data:
                existing = json.loads(getattr(player, 'instr_calculate_payoff')) or []
                index = len(existing) + 1
                payoff_data = {
                    'index': index,
                    'value': data.get('value_dropdown'),
                    'your_bid': data.get('your_bid_value'),
                    'opponent_bid': data.get('opponent_bid_value'),
                }
                player.append_json_values('instr_calculate_payoff', payoff_data)

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P8(Page):
    '''Attention Check 1'''
    form_model = 'player'
    form_fields = ['attn_check_1', 'page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {'page_name': 'Check 1'}

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)
        if player.game_instructions:
            player.quiz_value = 5
            player.Q1_number_2 = random.choice(range(0, player.quiz_value))
            player.Q1_number_1 = random.choice(range(player.Q1_number_2 + 1, 11))
            player.Q2_number_2 = random.choice(range(player.quiz_value + 1, 10))
            player.Q2_number_1 = random.choice(range(player.Q2_number_2 + 1, 11))
            player.Q3_number_1 = random.choice(range(0, player.quiz_value))
            player.Q3_number_2 = random.choice(range(player.quiz_value, 11))
            player.correct_answer_1 = player.constant + (player.quiz_value - player.Q1_number_2)
            player.correct_answer_2 = player.constant + (player.quiz_value - player.Q2_number_2)
            player.correct_answer_3 = player.constant
            player.correct_answer_4 = True 
        else:
            player.quiz_value = 250
            player.Q1_number_2 = random.choice(range(0, player.quiz_value, 50))
            player.Q1_number_1 = random.choice(range(player.Q1_number_2 + 50, 501, 50))
            player.Q2_number_2 = random.choice(range(player.quiz_value + 50, 500, 50))
            player.Q2_number_1 = random.choice(range(player.Q2_number_2 + 50, 501, 50))
            player.Q3_number_1 = random.choice(range(0, player.quiz_value, 50))
            player.Q3_number_2 = random.choice(range(player.quiz_value, 501, 50))
            player.correct_answer_1 = player.constant + (player.quiz_value - player.Q1_number_2)
            player.correct_answer_2 = player.constant + (player.quiz_value - player.Q2_number_2)
            player.correct_answer_3 = player.constant
            player.correct_answer_4 = True 


class P9(Page):
    '''Comprehension Quiz'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {
            'page_name': 'Quiz',
            'control_instructions' : player.control_instructions,
            'integrated_matrix' : player.integrated_matrix,
            'integrated_endowment' : player.integrated_endowment,
            'auction_instructions' : player.auction_instructions,
            'instruction_value' : player.instruction_value,
            'quiz_value' : player.quiz_value,
            'computer_instructions' : player.computer_instructions,
            'game_instructions' : player.game_instructions,
            'Q1_number_1' : player.Q1_number_1,
            'Q1_number_2' : player.Q1_number_2,
            'Q2_number_1' : player.Q2_number_1,
            'Q2_number_2' : player.Q2_number_2,
            'Q3_number_1' : player.Q3_number_1,
            'Q3_number_2' : player.Q3_number_2,
        }
    
    def js_vars(player):
        return dict(constant = player.constant, 
                    quiz_value = player.quiz_value,
                    instruction_value = player.instruction_value,
                    auction_instructions = player.auction_instructions,
                    computer_instructions = player.computer_instructions,
                    correct_answers_quiz1={'Q1': player.correct_answer_1, 'Q2': player.correct_answer_2, 'Q3': player.correct_answer_3, 'Q4': player.correct_answer_4})
    
    @staticmethod
    def live_method(player: Player, data):
        if player.integrated_matrix:
            if 'dropdown_value' in data:
                value = data['dropdown_value']
                existing = json.loads(getattr(player, 'quiz_value_dropdown')) or []
                index = len(existing) + 1
                player.append_json_values('quiz_value_dropdown', {'index': index, 'value': value})
        else:
            if 'your_bid_value' in data:
                existing = json.loads(getattr(player, 'quiz_calculate_payoff')) or []
                index = len(existing) + 1
                payoff_data = {
                    'index': index,
                    'value': data.get('value_dropdown'),
                    'your_bid': data.get('your_bid_value'),
                    'opponent_bid': data.get('opponent_bid_value'),
                }
                player.append_json_values('quiz_calculate_payoff', payoff_data)

        if data.get('submit_quiz') == 'submit_quiz':
            answers_quiz1 = data.get('answers_quiz1', {})

            if answers_quiz1.get('Q1') != player.correct_answer_1:
                player.Q1_incorrect += 1

            if answers_quiz1.get('Q2') != player.correct_answer_2:
                player.Q2_incorrect += 1

            if answers_quiz1.get('Q3') != player.correct_answer_3:
                player.Q3_incorrect += 1

            if bool(answers_quiz1.get('Q4')) != bool(player.correct_answer_4):
                player.Q4_incorrect += 1

            if player.Q1_incorrect >= 2 or player.Q2_incorrect >= 2 or player.Q3_incorrect >= 2 or player.Q4_incorrect >= 2:
                return {player.id_in_group: {'advance_page': True}}
        
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class Quiz_Review(Page):
    '''Quiz Feedback'''
    form_model = 'player'
    form_fields = [ 'page_enter_time', 'current_page_name']

    def is_displayed(player):
        if player.Q1_incorrect >= 2 or player.Q2_incorrect >= 2 or player.Q3_incorrect >= 2 or player.Q4_incorrect >= 2:
            return True

    def js_vars(player):
        return dict(Q1_incorrect = player.Q1_incorrect,
                    Q2_incorrect = player.Q2_incorrect,
                    Q3_incorrect = player.Q3_incorrect,
                    Q4_incorrect = player.Q4_incorrect)
    
    def vars_for_template(player):
        return {
            'page_name': 'Quiz Feedback',
            'integrated_endowment' : player.integrated_endowment,
            'quiz_value' : player.quiz_value,
            'Q1_incorrect' : player.Q1_incorrect,
            'Q2_incorrect' : player.Q2_incorrect,
            'Q3_incorrect' : player.Q3_incorrect,
            'Q4_incorrect' : player.Q4_incorrect,
            'correct_answer_1_cents' : (player.quiz_value - player.Q1_number_2),
            'correct_answer_1_dollars' : f"{((player.quiz_value - player.Q1_number_2) / 100):.2f}",
            'correct_answer_2_cents' : (player.quiz_value - player.Q2_number_2),
            'correct_answer_2_dollars' : f"{((player.quiz_value - player.Q2_number_2) / 100):.2f}",
            'Q1_number_1' : player.Q1_number_1,
            'Q1_number_2': player.Q1_number_2,
            'Q2_number_1': player.Q2_number_1,
            'Q2_number_2': player.Q2_number_2,
            'Q3_number_1' : player.Q3_number_1,
            'Q3_number_2' : player.Q3_number_2,
            'total_Q1_earnings': f"{(((player.quiz_value - player.Q1_number_2) / 100) + 6.5):.2f}",
            'total_Q2_earnings': f"{(((player.quiz_value - player.Q2_number_2) / 100) + 6.5):.2f}"
        }
    
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P10(Page):
    '''Attention Check 2'''
    form_model = 'player'
    form_fields = ['attn_check_2', 'page_enter_time', 'current_page_name']
    
    def vars_for_template(player):
        return {
            'page_name': 'Check 2',
        }
    
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P11(Page):
    '''Optional Kickout Page'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {'page_name': 'Kickout'}

    def is_displayed(player):
        if player.attn_check_1 == 1 and player.attn_check_2 == 1:
            return True
    
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P12_1(Page):
    '''Auction/Game with Matrix'''
    form_model = 'player'
    form_fields = ['selected_bid', 'page_enter_time', 'current_page_name']

    def is_displayed(player):
        return player.integrated_matrix
    
    def vars_for_template(player):
        return {
            'page_name': 'Game',
            'control_instructions' : player.control_instructions,
            'integrated_matrix' : player.integrated_matrix,
            'integrated_endowment' : player.integrated_endowment,
            'auction_value' : player.auction_value,
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'instruction_value' : player.instruction_value,
            'game_instructions' : player.game_instructions
        }

    def js_vars(player):
        return dict(constant = player.constant, 
                    control_instructions = player.control_instructions,
                    auction_value = player.auction_value, 
                    instruction_value = player.instruction_value,
                    auction_instructions = player.auction_instructions,
                    computer_instructions = player.computer_instructions)

    @staticmethod
    def live_method(player: Player, data):
        if 'dropdown_value' in data:
            value = data['dropdown_value']
            existing = json.loads(getattr(player, 'game_value_dropdown')) or []
            index = len(existing) + 1
            player.append_json_values('game_value_dropdown', {'index': index, 'value': value})

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P12_2(Page):
    '''Auction Without Matrix'''
    form_model = 'player'
    form_fields = ['selected_bid', 'page_enter_time', 'current_page_name']

    def is_displayed(player):
        return not player.integrated_matrix
    
    def vars_for_template(player):
        return {
            'page_name': 'Game',
            'control_instructions' : player.control_instructions,
            'integrated_matrix' : player.integrated_matrix,
            'integrated_endowment' : player.integrated_endowment,
            'auction_value' : player.auction_value,
            'auction_instructions' : player.auction_instructions,
            'computer_instructions' : player.computer_instructions,
            'instruction_value' : player.instruction_value,
            'game_instructions' : player.game_instructions
        }

    def js_vars(player):
        auction_value = player.auction_value
        return dict(auction_value = auction_value, 
                    control_instructions = player.control_instructions,
                    constant = player.constant,         
                    instruction_value = player.instruction_value,
                    auction_instructions = player.auction_instructions)
    
    @staticmethod
    def live_method(player: Player, data):
        if 'your_bid_value' in data:
            existing = json.loads(getattr(player, 'game_calculate_payoff')) or []
            index = len(existing) + 1
            payoff_data = {
                'index': index,
                'value': data.get('value_dropdown'),
                'your_bid': data.get('your_bid_value'),
                'opponent_bid': data.get('opponent_bid_value'),
            }
            player.append_json_values('game_calculate_payoff', payoff_data)

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P13(Page):
    '''Follow-Up Quiz'''
    form_model = 'player'
    form_fields = ['fllw_up_Q1', 'fllw_up_Q2', 'fllw_up_Q3', 'page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {'page_name': 'CRT'}

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)
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
    form_fields = ['demographic_1', 'demographic_2', 'page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {'page_name': 'Demographics'}

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)
        if player.Q1_incorrect == 0 and player.Q2_incorrect == 0 and player.Q3_incorrect == 0 and player.Q4_incorrect == 0:
            player.comprehension_quiz_payment = 50

        elif player.Q1_incorrect <= 1 and player.Q2_incorrect <= 1 and player.Q3_incorrect <= 1 and player.Q4_incorrect <= 1:
            player.comprehension_quiz_payment = 20

        else:
            player.comprehension_quiz_payment = 0
            
        player.follow_up_quiz_payment = 0
        
        if player.fllw_up_Q1_incorrect == 0:
            player.follow_up_quiz_payment += 25

        if player.fllw_up_Q2_incorrect == 0:
            player.follow_up_quiz_payment += 25
            
        if player.fllw_up_Q3_incorrect == 0:
            player.follow_up_quiz_payment += 25


class P15(Page):
    '''Submitting Payment'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def vars_for_template(player):        
        return {
            'page_name': 'Payment',
            'control_instructions' : player.control_instructions,
            'auction_instructions' : player.auction_instructions,
            'game_instructions' : player.game_instructions
        }

    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)


class P16(Page):
    '''Redirect Page'''
    form_model = 'player'
    form_fields = ['page_enter_time', 'current_page_name']

    def vars_for_template(player):
        return {'page_name': 'Redirect'}

    def js_vars(player):
        return dict(
                completion_link=player.subsession.session.config['completion_link'])    
    
    def before_next_page(player, timeout_happened):
        track_timestamps(player, timeout_happened)

class Feedback(Page):
    ''' Feedback Page'''
    form_model = 'player'
    form_fields = ['feedback_bool', 'feedback_text']

    def is_displayed(player):
        return player.subsession.session.config.get('pilot', False)

    def vars_for_template(player):
        return {'page_name': 'Feedback'}
        

page_sequence = [P1, P2, P3, P4, P5, P6, P7, P8, P9, Quiz_Review, P10, P11, P12_1, P12_2, Feedback, P13, P14, P15, P16]