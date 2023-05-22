from os import environ

DEBUG = 0

SESSION_CONFIGS = [
    dict(
        name='altruism',
        display_name="alt_single_player",
        num_demo_participants=2,
        instructions_time=5,#60*9,
        dropout_time=60,
        app_sequence=['altruism'],
        charities=['wwf', 'save the children', 'the nature conservancy', 'unicef'],
        endowment=10,
        # training_round_number=3,
        # n_bad_multiplier=5,
        # number_of_rounds_against_bad=30,
        # number_of_rounds_against_good=30,
    ),
]

export_style = 'player'
pounds_per_point = 0.01

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['opp_id', 'multiplier', 'disclose', 'contribution', 'opp_bad_contribution',
                      'prolific_id', 'idx', 'is_dropout', 'time_at_last_response', 'total',
                      'disclosure_group', 'end', 'opp_multiplier', 'opp_disclose', 'opp_p_disclose', 'time_instructions']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='prolific1',
        display_name='Prolific 1',
        # participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '2997710251445'

INSTALLED_APPS = ['otree' ,'altruism']
