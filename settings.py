from os import environ
from dotenv import load_dotenv

load_dotenv() 

DEBUG = False

SESSION_CONFIGS = [
    dict(
        name = 'full_experiment',
        display_name = "Full Experiment",
        app_sequence = ['stage_1'],
        num_demo_participants = 1,
        control_integrated = True,
        control_isolated = False,
        table_integrated = False,
        table_isolated = False,
        calculator_integrated = False,
        calculator_isolated = False,
        no_auction_integrated = False,
        no_auction_isolated = False,
        computer_integrated = False,
        computer_isolated = False,
        pilot = False,
        number_in_treatment = 2,
        completion_link = 'https://app.prolific.com/submissions/complete?cc=CGH8YZX1'
    )
]

ROOMS = [
    dict(
        name = 'full_experiment',
        display_name = "Full Experiment",
     ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point = 0.01, 
    participation_fee = 2.00, 
    doc = "",
)

LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'

ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = environ.get('OTREE_SECRET_KEY')

