from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'stage_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class P1(Page):
    pass


class P2(Page):
    pass


class P3(Page):
    pass


class P4(Page):
    pass


class P5(Page):
    pass


class P6(Page):
    pass


class P7(Page):
    pass


class P8(Page):
    pass


class P9(Page):
    pass


page_sequence = [P1, P2, P3, P4, P5, P6, P7, P8, P9]
