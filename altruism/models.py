from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
# import otree.database
# import sqlite3
import numpy as np
import random
from requests import session
from utils.debug import logger
from settings import export_style
import shutil

class Constants(BaseConstants):
    name_in_url = 'altruism'
    players_per_group = 2
    num_rounds = 3
    endowment = 10
    multiplier_good = 2.5
    multiplier_bad = 1.5
    disclosure_cost=  2


class Subsession(BaseSubsession):

    def init(self):
        """
        this method is called only once
        :return:
        """
        logger.debug('Initialization of the first phase:'
                    ' attributing multipliers and participant labels.')
        n_participant = self.session.num_participants
        logger.debug(f'N participants = {n_participant}')

        for i, p in enumerate(self.get_players()):
            p.participant.is_dropout = False
#
#        # self.session.sorting = False
#        n_bad_multiplier = self.session.config.get('n_bad_multiplier')
#        n_training_rounds = self.session.config.get('training_round_number')
#        multipliers = [Constants.multiplier_bad, ] * \
#            n_bad_multiplier
#        multipliers += [Constants.multiplier_good, ] * \
#            (n_participant-n_bad_multiplier)
#
#        np.random.shuffle(multipliers)
#
#        for i, p in enumerate(self.get_players()):
#            # print(p.participant.id_in_session)
#            p.participant.idx = i
#            # assert len(multipliers) > i
#            p.participant.multiplier = multipliers[p.participant.idx]
#
#            p.participant.is_dropout = False
#
#            p.participant.time_at_last_response = np.NaN
#
#            p.participant.total = 0
#            p.participant.end = False
#
#            # random values for training rounds
#            opp_multipliers = list(np.random.choice(
#                [Constants.multiplier_bad, Constants.multiplier_good],
#                size=n_training_rounds, replace=True))
#
#            opp_p_disclose_beg = [.5,] * n_training_rounds
#            opp_disclose_beg = list(np.random.choice([0, 1], size=n_training_rounds, replace=True))
#
#            # set half 1.5/2.5 
#            opp_multipliers += [Constants.multiplier_bad, ] * \
#                self.session.config.get('number_of_rounds_against_bad')
#            opp_multipliers += [Constants.multiplier_good, ] * \
#                self.session.config.get('number_of_rounds_against_good')
#
#            # there are 4 disclose probabilities, organized as random blocks of .25/.5/.75/1
#            opp_p_disclose = [
#                [i, ] * ((Constants.num_rounds-n_training_rounds) //
#                         len(Constants.disclosure_p))
#                for i in Constants.disclosure_p
#            ]
#            
#            chunk_size = len(opp_p_disclose[0])
#            n_chunk = len(opp_p_disclose)
#
#            # draw outcomes (0, 1) from previously generated probabilities of disclosure 
#            opp_disclose = [[int(t < round(chunk_size * prob)) for t, prob in enumerate(opp_p_disclose[i])]
#                for i in range(n_chunk)]
#            
#            n_rounds = self.session.config.get('number_of_rounds_against_bad')
#            
#            opp_bad_contribution = [
#                Decision.choice[(Constants.multiplier_bad, None)]
#                [int(t < round(n_rounds * .5))] for t in range(n_rounds)
#            ]
#            
#
#            np.random.shuffle(opp_bad_contribution)
#            
#            order = random.sample(range(n_chunk), n_chunk)
#
#            opp_p_disclose = opp_p_disclose_beg + list(np.array(opp_p_disclose)[order].flatten())
#            opp_disclose = opp_disclose_beg + list(np.array(opp_disclose)[order].flatten())
#
#            opp_multipliers = np.array(opp_multipliers)
#
#            np.random.shuffle(opp_multipliers[n_training_rounds:])
#
#            p.participant.opp_p_disclose = opp_p_disclose
#            p.participant.opp_disclose = opp_disclose
#            p.participant.opp_multiplier = opp_multipliers
#            p.participant.opp_bad_contribution = opp_bad_contribution
#
# 
    def creating_session(self):
        """
        match according to deterministic good/bad, good/good, bad/bad
        """
        if self.round_number == 1:
            # pass
            self.init()

    

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contribution = models.IntegerField(default=-1)
    rt = models.IntegerField(default=-1)
    reward = models.FloatField(default=-1)
    time_instructions = models.FloatField(default=-1)

    def see_opponent_type(self):
        opp_multiplier = self.participant.opp_multiplier[self.round_number-1]
        opp_disclosed = self.participant.opp_disclose[self.round_number-1]
        return opp_multiplier if opp_disclosed else None


    def set_contribution(self, contribution: int, rt: int = None):
        self.contribution = int(contribution)
        if rt is not None:
            self.rt = rt
        # self.participant.contribution[self.round_number - 1] = self.contribution

    def end_round(self):
        """
        this method is called at the end of each round
        :return:
        """
        pass

       # if not self.response3:

       #     logger.debug(f'Round {self.round_number}/ Participant {self.id_in_subsession}:'
       #                  f' Setting payoffs and saving data.')
       #     data = self.set_payoffs()
       #     self.record_round_data(data)
       #     self.response3 = True


def custom_export(players):
    col = [                                    
        'session',
        'is_bot',
        'prolific_id',
        'id_in_session',
        'idx',
        'round_number',
        'multiplier',
        'disclose',
        'contribution',
        'rt1',
        'rt2',
        'reward',
        'payoff',
        'total',
        'individual_share',
        'opp_multiplier',
        'opp_disclose',
        'opp_p_disclose',
        'opp_contribution',
        'opp_payoff',
        'total_contribution'
    ]
    yield col
    for p in players:
        row = [
            p.session.code,
            p.participant.is_dropout,
            p.participant.label,
            p.participant.id_in_session,
            p.participant.idx,
            p.round_number,
            p.participant.multiplier,
            p.disclose,
            p.contribution,
            p.rt1,
            p.rt2,
            p.reward,
            p.payoff,
            p.total,
            p.individual_share,
            p.opp_multiplier,
            p.opp_disclose,
            p.opp_p_disclose,
            p.opp_contribution,
            p.opp_payoff,
            p.total_contribution
        ]
        yield row

 

