from instructions._builtin import Page, WaitPage
#from altruism.instructions import get_panels, titles
from .models import C
#import numpy as np
import time
from settings import pounds_per_point

from utils.debug import logger


SECOND = 1000
MINUTE = SECOND * 60
DROPOUT_TIME = 30 * SECOND
INSTRUCTIONS_TIME = 10 * MINUTE
RESULTS_TIME = 7.5 * SECOND


# ------------------------------------------------------------------------------------------------------------------- #
# Pages
# ------------------------------------------------------------------------------------------------------------------- #
class Instructions(Page):
    # def get_template_name(self):
        # return 'instructions/templates/Instructions.html'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        from .instructions import get_panels, titles
        if self.player.participant.time_instructions is None:
            self.player.participant.time_instructions = int(time.time() * SECOND)
        limit = self.session.config.get('instructions_time') * SECOND
        # single_player = int(self.session.config.get('single_player')) 
        return {'panels': get_panels(), 'titles': titles, 'instructionsTime': limit,
         'startTime': self.player.participant.time_instructions}#, 'single_player': single_player}

    @staticmethod
    def live_method(player, data):
        _set_as_connected(player)
        time_since_opening = time.time() * SECOND -  player.participant.time_instructions
        limit = player.session.config.get('instructions_time') * SECOND
        if time_since_opening > limit:
            return {player.id_in_group: True}
        return False


page_sequence = [Instructions]

# ------------------------------------------------------------------------------------------------------------------- #
# Side Functions #                                                                                                    # 
# ------------------------------------------------------------------------------------------------------------------- #
def _set_as_connected(player):
    player.participant.time_at_last_response = time.time()


def _check_for_disconnections(players):
    player = players[0]
    real_players = [p for p in players if not p.participant.is_dropout]
    limit = player.session.config.get('dropout_time')*SECOND
    if player.round_number == 1:
        limit *= 2
    for p in real_players:
        t = (time.time() - p.participant.time_at_last_response) * SECOND
        # if t > limit and not p.participant.end:
        if t > limit:
            p.participant.is_dropout = True

def _get_all_players(player):
    return [player, ] + player.get_others_in_subsession()


# function that returns time in months between two dates without additional libraries
def _months_between(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


