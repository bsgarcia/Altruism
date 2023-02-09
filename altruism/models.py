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
import otree.database
import sqlite3
import numpy as np
import random
from requests import session
from utils.debug import logger
from settings import export_style
import shutil


class Constants(BaseConstants):
    name_in_url = 'step1'
    players_per_group = None
    num_rounds = 63
    multiplier_bad = 1.5
    multiplier_good = 2.5
    endowment = 10
    disclosure_cost = 2
    disclosure_p = [.25, .5, .75, 1]


class Decision:
    choice = {
        (Constants.multiplier_bad, Constants.multiplier_bad): (0,10),
        (Constants.multiplier_good, Constants.multiplier_bad): 10,
        (Constants.multiplier_bad, Constants.multiplier_good): (0, 10),
        (Constants.multiplier_good, Constants.multiplier_good): 10,
        (Constants.multiplier_good, None): 10,
        (Constants.multiplier_bad, None): (0, 10),
    }


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

        # self.session.sorting = False
        n_bad_multiplier = self.session.config.get('n_bad_multiplier')
        n_training_rounds = self.session.config.get('training_round_number')
        multipliers = [Constants.multiplier_bad, ] * \
            n_bad_multiplier
        multipliers += [Constants.multiplier_good, ] * \
            (n_participant-n_bad_multiplier)

        np.random.shuffle(multipliers)

        for i, p in enumerate(self.get_players()):
            # print(p.participant.id_in_session)
            p.participant.idx = i
            # assert len(multipliers) > i
            p.participant.multiplier = multipliers[p.participant.idx]

            p.participant.is_dropout = False

            p.participant.time_at_last_response = np.NaN

            p.participant.total = 0
            p.participant.end = False

            # random values for training rounds
            opp_multipliers = list(np.random.choice(
                [Constants.multiplier_bad, Constants.multiplier_good],
                size=n_training_rounds, replace=True))

            opp_p_disclose_beg = [.5,] * n_training_rounds
            opp_disclose_beg = list(np.random.choice([0, 1], size=n_training_rounds, replace=True))

            # set half 1.5/2.5 
            opp_multipliers += [Constants.multiplier_bad, ] * \
                self.session.config.get('number_of_rounds_against_bad')
            opp_multipliers += [Constants.multiplier_good, ] * \
                self.session.config.get('number_of_rounds_against_good')

            # there are 4 disclose probabilities, organized as random blocks of .25/.5/.75/1
            opp_p_disclose = [
                [i, ] * ((Constants.num_rounds-n_training_rounds) //
                         len(Constants.disclosure_p))
                for i in Constants.disclosure_p
            ]
            
            chunk_size = len(opp_p_disclose[0])
            n_chunk = len(opp_p_disclose)

            # draw outcomes (0, 1) from previously generated probabilities of disclosure 
            opp_disclose = [[int(t < round(chunk_size * prob)) for t, prob in enumerate(opp_p_disclose[i])]
                for i in range(n_chunk)]
            
            n_rounds = self.session.config.get('number_of_rounds_against_bad')
            
            opp_bad_contribution = [
                Decision.choice[(Constants.multiplier_bad, None)]
                [int(t < round(n_rounds * .5))] for t in range(n_rounds)
            ]
            

            np.random.shuffle(opp_bad_contribution)
            
            order = random.sample(range(n_chunk), n_chunk)

            opp_p_disclose = opp_p_disclose_beg + list(np.array(opp_p_disclose)[order].flatten())
            opp_disclose = opp_disclose_beg + list(np.array(opp_disclose)[order].flatten())

            opp_multipliers = np.array(opp_multipliers)

            np.random.shuffle(opp_multipliers[n_training_rounds:])

            p.participant.opp_p_disclose = opp_p_disclose
            p.participant.opp_disclose = opp_disclose
            p.participant.opp_multiplier = opp_multipliers
            p.participant.opp_bad_contribution = opp_bad_contribution


    def creating_session(self):
        """
        match according to deterministic good/bad, good/good, bad/bad
        """
        if self.round_number == 1:
            self.init()

    

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contribution = models.IntegerField(default=-1)
    disclose = models.BooleanField(default=None)
    rt1 = models.IntegerField(default=-1)
    rt2 = models.IntegerField(default=-1)
    response1 = models.BooleanField(default=False)
    response2 = models.BooleanField(default=False)
    response3 = models.BooleanField(default=False)
    reward = models.FloatField(default=-1)
    time_instructions = models.FloatField(default=-1)
    total = models.FloatField(default=0)
    total_contribution = models.FloatField(default=-1)
    individual_share = models.FloatField(default=-1)
    opp_multiplier = models.FloatField(default=-1)
    opp_disclose = models.BooleanField(default=None)
    opp_p_disclose = models.FloatField(default=-1)
    opp_contribution = models.IntegerField(default=-1)
    opp_payoff = models.FloatField(default=-1)

    def see_opponent_type(self):
        opp_multiplier = self.participant.opp_multiplier[self.round_number-1]
        opp_disclosed = self.participant.opp_disclose[self.round_number-1]
        return opp_multiplier if opp_disclosed else None

    def set_disclose(self, disclose: bool, rt1: int = None):
        self.disclose = disclose
        if rt1 is not None:
            self.rt1 = rt1
        self.response1 = True
        # self.participant.disclose[self.round_number - 1] = self.disclose

    def set_contribution(self, contribution: int, rt2: int = None):
        self.contribution = int(contribution)
        if rt2 is not None:
            self.rt2 = rt2
        self.response2 = True
        # self.participant.contribution[self.round_number - 1] = self.contribution

    def end_round(self):
        """
        this method is called at the end of each round
        :return:
        """

        if not self.response3:
            logger.debug(f'Round {self.round_number}/ Participant {self.id_in_subsession}:'
                         f' Setting payoffs and saving data.')
            data = self.set_payoffs()
            self.record_round_data(data)
            self.response3 = True

    def set_payoffs(self):

        pp = self.participant
        p = self

        opp_multiplier = pp.opp_multiplier[self.round_number-1]
        participant_multiplier = pp.multiplier if self.disclose else None

        n_training_rounds = self.session.config.get('training_round_number')

        opp_disclose = pp.opp_disclose[self.round_number-1]

        # if opponent multiplier is good, choose max
        # if opponent multiplier is bad, choose 0, or max
        if opp_multiplier == Constants.multiplier_bad:
            if self.round_number <= n_training_rounds:
                opp_contribution = np.random.choice(Decision.choice[(
                opp_multiplier, participant_multiplier)])
            else:
                opp_contribution = pp.opp_bad_contribution.pop()
        else:
            opp_contribution = Decision.choice[(
                opp_multiplier, participant_multiplier)]

        # remove disclosure cost from opponent contribution if opponent disclosed and selects max contribution (max is now 8)
        if opp_contribution == Constants.endowment: 
            opp_contribution -= Constants.disclosure_cost * opp_disclose

        contributions = [p.contribution*pp.multiplier, opp_contribution*opp_multiplier]
        self.total_contribution = sum(contributions)
        self.individual_share = np.round(self.total_contribution / 2)

        p.payoff = np.round(
            Constants.endowment
            - (Constants.disclosure_cost * p.disclose)
            - p.contribution + self.individual_share, 2)
        p.reward = np.round(
            Constants.endowment
            - (Constants.disclosure_cost * p.disclose)
            - p.contribution + self.individual_share, 2)

        self.opp_payoff = np.round(
            Constants.endowment
            - (Constants.disclosure_cost * opp_disclose)
            - opp_contribution + self.individual_share, 2)

        pp.total += p.reward
        p.total = np.round(pp.total, 2)

        if self.round_number == self.session.config.get('training_round_number'):
            pp.total = 0

        return p, opp_contribution, opp_multiplier

    def record_round_data(self, data):

        p = data[0]

        self.opp_contribution = int(data[1])
        self.opp_multiplier = float(data[2])

        self.opp_disclose = bool(p.participant.opp_disclose[self.round_number-1])
        self.opp_p_disclose = float(p.participant.opp_p_disclose[self.round_number-1])

    @staticmethod
    def backup(with_sqlite=False):
        
        if with_sqlite:
            c1 = otree.database.get_disk_conn()
            # get in-memory database connection
            c2 = sqlite3.connect('db_backup.sqlite3')
            # create physical database file
            c2.commit()
            # commit changes
            c1.commit()

            c1.backup(c2)
            # copy in-memory database to physical database file
            c2.cursor().execute(f'PRAGMA user_version = {otree.database.version_for_pragma()};')
            # set user_version to current oTree version
            c2.commit()
            # commit changes
            c1.commit()
            # commit changes (not sure this is needed)
            # c1.close()
            # close in-memory database connection
            c2.close()
            # close physical database connection
        else:
            shutil.copyfile('db.sqlite3', 'db_backup.sqlite3')
            # c2 = sqlite3.connect('db_backup.sqlite3')
            # c2.cursor().execute(f'PRAGMA user_version = {otree.database.version_for_pragma()};')
            # c2.commit()
            # c2.close()

        logger.info('Backup successful')


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

 

