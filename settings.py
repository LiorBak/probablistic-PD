from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, 
                               participation_fee=5,
                               bonus_payment=5,
                               turned_away_fee=3)

SESSION_CONFIGS = [
    dict(name='experiment_main',
         num_demo_participants=6,
         app_sequence=['prisoner', 'survey'],
         use_browser_bots=False,
         game_type="pPD",
         ),
    dict(
        name='forwrd_link',
        display_name='Waiting room to provide the Zoom link to start the experiment',
        app_sequence=['waiting_room'],
        num_demo_participants=1,
        zoom_link="TODO PUT YOUR ZOOM LINK HERE",
    ),
    dict(
        name='turned_away',
        display_name='Turned Away - session to ensure people that get turned away get paid',
        app_sequence=['turned_away'],
        num_demo_participants=1
    ),      
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['wait_page_arrival', 'is_dropout', 'total_score', 'chance_to_win', 'random_lottery_number', 'win_bonus', 'bonus']
SESSION_FIELDS = []

ROOMS = [
    dict(
        name='room1',
        display_name='Room 1 pPD',
    ),
    dict(
        name='room2',
        display_name='Room 2 pCG',
    ),
        dict(
        name='room3',
        display_name='Room 3 PD',
    ),
    dict(
        name='room_turned_away',
        display_name='Room Turned Away',
    ),
    dict(
        name='waiting_room',
        display_name='Waiting Room',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
