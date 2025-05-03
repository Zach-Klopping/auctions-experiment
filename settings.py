from os import environ

DEBUG = False

SESSION_CONFIGS = [
    dict(
        name = 'standard_no_matrix',
        display_name = "Standard Instructions, No Payoff Matrix",
        app_sequence = ['stage_1'],
        num_demo_participants = 1,
        computer_opponent = False,
        integrated_endowment = True,
        integrated_payoff_matrix = False,
        standard_instructions = True,
     ),

      dict(
        name = 'standard_with_matrix_integrated_endowment',
        display_name = "Standard Instructions, With Payoff Matrix, Integrated",
        app_sequence = ['stage_1'],
        num_demo_participants = 1,
        computer_opponent = False,
        integrated_endowment = True,
        integrated_payoff_matrix = True,
        standard_instructions = True,
     ),

     dict(
        name = 'standard_with_matrix_not_integrated_endowment',
        display_name = "Standard Instructions, With Payoff Matrix, Not Integrated",
        app_sequence = ['stage_1'],
        num_demo_participants = 1,
        computer_opponent = False,
        integrated_endowment = False,
        integrated_payoff_matrix = True,
        standard_instructions = True,
     ),

    dict(
        name = 'no_auction_with_matrix_integrated_endowment',
        display_name = "No Auction Instructions, With Payoff Matrix, Integrated",
        app_sequence = ['stage_1'],
        num_demo_participants = 1,
        computer_opponent = False,
        integrated_endowment = True,
        integrated_payoff_matrix = True,
        standard_instructions = False,
     ),

      dict(
        name = 'no_auction_with_matrix_not_integrated_endowment',
        display_name = "No Auction Instructions, With Payoff Matrix, Not Integrated",
        app_sequence = ['stage_1'],
        num_demo_participants = 1,
        computer_opponent = False,
        integrated_endowment = False,
        integrated_payoff_matrix = True,
        standard_instructions = False,
     ),

     dict(
        name = 'computer_with_matrix_integrated_endowment',
        display_name = "Computer Opponent, With Payoff Matrix, Integrated",
        app_sequence = ['stage_1'],
        num_demo_participants = 1,
        computer_opponent = True,
        integrated_endowment = True,
        integrated_payoff_matrix = True,
        standard_instructions = True,
     ),

         dict(
        name = 'computer_with_matrix_not_integrated_endowment',
        display_name = "Computer Opponent, With Payoff Matrix, Not Integrated",
        app_sequence = ['stage_1'],
        num_demo_participants = 1,
        computer_opponent = True,
        integrated_endowment = False,
        integrated_payoff_matrix = True,
        standard_instructions = True,
     ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point = 1.00, 
    participation_fee = 0.00, 
    doc = "",
    standard_instructions = True,
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7464521975030'
