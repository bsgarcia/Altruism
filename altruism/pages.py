from altruism._builtin import Page, WaitPage
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
class End(Page):

    def vars_for_template(self):
        return {'prolific_id': self.player.participant.label}

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

class Wait(WaitPage):
    # group_by_arrival_time = True
    def is_displayed(self):
        return self.round_number != C.NUM_ROUNDS
    
    def after_all_players_arrive(self):
        logger.debug('WaitPage: set status as connected')
        for p in self.group.get_players():
            logger.debug(
                'WaitPage: {p.participant.code}-{p.participant.label} is connected'.format(p=p))
            _set_as_connected(p)
            if p.participant.is_dropout:
                # if p.participant.is_dropout, set it to False as it is a new round
                logger.debug('WaitPage: {p.participant.code}-{p.participant.label} is not dropout anymore'.format(p=p))
                p.participant.is_dropout = False

class InitialWait(WaitPage):
    group_by_arrival_time = True
    
    def vars_for_template(self):
        return {'body_text': 'Waiting for another player... please do not leave this page.'}

    def is_displayed(self):
        return self.round_number == 1

    def after_all_players_arrive(self):
        logger.debug('WaitPage: set status as connected')
        for p in self.group.get_players():
            logger.debug(
                'WaitPage: {p.participant.code}-{p.participant.label} is connected'.format(p=p))
            _set_as_connected(p)
            if p.participant.is_dropout:
                # if p.participant.is_dropout, set it to False as it is a new round
                logger.debug('WaitPage: {p.participant.code}-{p.participant.label} is not dropout anymore'.format(p=p))
                p.participant.is_dropout = False


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
            1: [[charity, f'img/{charity}.png'] for charity in ('unicef', 'savethechildren')],
            2: [[charity, f'img/{charity}.png'] for charity in ('wwf', 'thenatureconservancy')],
            3: [[charity, f'img/{charity}.png'] for charity in ('unicef', 'savethechildren', 'wwf', 'thenatureconservancy')],
        }
        for k in ch:
            for i, (name, img) in enumerate(ch[k]):
                for name_with_space in charity_names:
                    if name_with_space.replace(' ', '') == name:
                        ch[k][i][0] = name_with_space

        self.player.condition = C.ORDERS[self.group.order_idx][self.round_number-1]
   
        return {
            'charities': ch[self.player.condition] +  [('none', 'img/none_of_them.png')] ,
            'endowment': endowment, 'notify': int(self.round_number == 1)
        }
    
    @staticmethod
    def live_method(player, data):
        _set_as_connected(player)
        _check_for_disconnections(players=player.get_others_in_group())

        # if player.choice is empty string ""
        if not player.choice and data != 'ping':
            logger.debug(f'Participant {player.participant.label} saving response. {data}')
            player.set_contribution(
                contribution=int(data['contribution']),
            )
            player.set_rt(
                rt=int(data['rt'])
            )
            player.set_choice(
                choice=data['choice']
            )

            player.set_msg(
                msg_clean=data['msg_clean'], msg_html=data['msg_html'], msg_json=data['msg_json']
            )
            
            #player.end_round()

    

page_sequence = [InitialWait, Main, End, Wait]

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


