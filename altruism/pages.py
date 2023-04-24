from altruism._builtin import Page, WaitPage
#from altruism.instructions import get_panels, titles
from .models import Constants
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

class End(Page):

    def vars_for_template(self):
        # last backup
        self.player.backup(with_sqlite=True)
        total = self.player.participant.total
        dtotal = np.round(total*pounds_per_point, 2)
        # if decimals show, if not use int
        pounds = int(dtotal) if dtotal.is_integer() else dtotal
        pences = int(dtotal*100) if (dtotal*100).is_integer() else dtotal*100
        return {'total': total, 'pences': pences, 'pounds': pounds}

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class Wait(WaitPage):
    def after_all_players_arrive(self):
        pass

class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        from .instructions import get_panels, titles
        if self.player.time_instructions == -1:
            self.player.time_instructions = time.time()
        limit = self.session.config.get('instructions_time') * SECOND
        # single_player = int(self.session.config.get('single_player')) 
        return {'panels': get_panels(), 'titles': titles, 'instructionsTime': limit}#, 'single_player': single_player}

    @staticmethod
    def live_method(player, data):
        _set_as_connected(player)
        time_since_opening = (time.time() - player.time_instructions) * SECOND
        limit = player.session.config.get('instructions_time') * SECOND
        if time_since_opening > limit:
            return {player.id_in_group: True}
        return False


class Disclose(Page):
    def get_template_name(self):
        if self.participant.is_dropout:
            return 'altruism/Dropout.html'
        # if not dropout then execute the original method
        
        # backup every twenty round (avoid overload)
        if self.round_number % 20 == 0:
            self.player.backup(with_sqlite=True)

        return super().get_template_name()

    def vars_for_template(self):
        from .html import wait, real
        _set_as_connected(self.player)
        training_round_number = self.session.config.get('training_round_number')
        return {
            'player_character': 'img/{}.gif'.format(self.player.participant.multiplier),
            'html': wait,
            'modalReal': real,
            # if decimals, show, if not, then round to closest integer
            'total': self.player.participant.total if self.player.participant.total % 1 else int(self.player.participant.total),
            'player_color': '#5893f6' if self.player.participant.multiplier == Constants.multiplier_good else '#d4c84d',
            'training': int(self.player.round_number <= training_round_number),
            'real': int(self.player.round_number == (training_round_number+1)),
        }

    @staticmethod
    def live_method(player, data):
        _set_as_connected(player)
        _check_for_disconnections(players=player.get_others_in_subsession())

        if not player.response1:
            logger.debug(f'Participant {player.participant.id_in_session}'
                         ' saving disclosure response.')
            player.set_disclose(
                disclose=bool(data['disclose']),
                rt1=int(data['RT'])
            )

        return {player.id_in_group: player.response1}



class Contribute(Page):
    def get_template_name(self):
        if self.participant.is_dropout:
            return 'altruism/Dropout.html'
        # if not dropout then execute the original method
        return super().get_template_name()


    def vars_for_template(self):
        from .html import wait

        _set_as_connected(self.player)

        opp_character, opp_multiplier = [self.player.see_opponent_type(), ] * 2
        player_character, player_multiplier = [self.player.participant.multiplier, ] * 2

        if opp_multiplier is None:
            opp_multiplier = '...'

        if not self.player.disclose:
            player_multiplier = '...'
            player_character = None

        endowment = Constants.endowment - (Constants.disclosure_cost*self.player.disclose)

        training_round_number = self.session.config.get('training_round_number')
        return {
            'player_character': 'img/{}.gif'.format(player_character),
            'opponent_character': 'img/{}.gif'.format(opp_character),
            'opp_color': '#5893f6' if opp_multiplier == Constants.multiplier_good else '#d4c84d',
            'opponent_multiplier': opp_multiplier,
            'player_multiplier': player_multiplier,
            'endowment': endowment,
            'html': wait,
            'training': int(self.player.round_number <= training_round_number)
        }

    @staticmethod
    def live_method(player, data):
        _set_as_connected(player)
        _check_for_disconnections(players=player.get_others_in_subsession())

        if not player.response2:
            logger.debug(f'Participant {player.participant.id_in_session}'
                         ' saving contribution response.')
            player.set_contribution(
                contribution=int(data['contribution']),
                rt2=int(data['RT'])
            )
            
            player.end_round()
        
        return {player.id_in_group: player.response2}



class Results(Page):
    def get_template_name(self):
        if self.participant.is_dropout:
            return 'altruism/Dropout.html'
        # if not dropout then execute the original method
        return super().get_template_name()


    def vars_for_template(self):
        player_multiplier = self.player.participant.multiplier

        opp_multiplier = self.player.opp_multiplier
        opp_disclose = self.player.opp_disclose
        opp_contribution = self.player.opp_contribution
        opp_payoff = self.player.opp_payoff
        individual_share = int(self.player.individual_share)
        payoff = int(self.player.payoff)
        
        training_round_number = self.session.config.get('training_round_number')

        if self.round_number == Constants.num_rounds:
            self.player.participant.end = True
            # self.sorting()

        return {
            'player_character': 'img/{}.gif'.format(player_multiplier),
            'opp_character': 'img/{}.gif'.format(opp_multiplier),
            'player_multiplier': player_multiplier,
            'opp_multiplier': opp_multiplier,
            'opp_contribution': opp_contribution,
            'opp_left': Constants.endowment - opp_contribution - (Constants.disclosure_cost*opp_disclose),
            'player_left': Constants.endowment - self.player.contribution - (Constants.disclosure_cost*self.player.disclose),
            'opp_payoff': opp_payoff,
            'player_color': '#5893f6' if player_multiplier == Constants.multiplier_good else '#d4c84d',
            'opp_color': '#5893f6' if opp_multiplier == Constants.multiplier_good else '#d4c84d',
            'disclose': opp_disclose,
            'individual_share': individual_share,
            'payoff': payoff,
            'resultsTime': self.session.config.get('results_time') * SECOND,
            'training': int(self.player.round_number <= training_round_number)

        }

class Main(Page):
    def get_template_name(self):
        if self.participant.is_dropout:
            return 'altruism/Dropout.html'
        # if not dropout then execute the original method
        return super().get_template_name()
    
    def vars_for_template(self):
        charity_names = self.session.config.get('charities')
        endowment = self.session.config.get('endowment')

        ch = {
            1: [(charity, f'img/{charity}.png') for charity in ('unicef', 'savethechildren')],
            2: [(charity, f'img/{charity}.png') for charity in ('wwf', 'thenatureconservancy')],
            3: [(charity, f'img/{charity}.png') for charity in ('unicef', 'savethechildren', 'wwf', 'thenatureconservancy')],
        }
                            # add a none option
        charities = ch[self.round_number] + [('none', 'img/none_of_them.png')] 
        return {
            'charities': charities,
            'endowment': endowment,
        }

        
# page_sequence = [Instructions, Disclose, Contribute, Results, End]
page_sequence = [Wait, Instructions, Main]

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
        if t > limit and not p.participant.end:
            p.participant.is_dropout = True

def _get_all_players(player):
    return [player, ] + player.get_others_in_subsession()


# function that returns time in months between two dates without additional libraries
def _months_between(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


