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
import shortuuid as su


class C(BaseConstants):
    # all variables should be in upper case
    NAME_IN_URL = 'instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ORDERS = [(1, 2, 3), (1, 3, 2), (2, 1, 3),
              (2, 3, 1), (3, 1, 2), (3, 2, 1)]


class Subsession(BaseSubsession):

    def init(self):
        """
        this method is called only once
        :return:
        """
        logger.debug('Initialization of participant')
        n_participant = self.session.num_participants
        logger.debug(f'N participants = {n_participant}')

        for i, p in enumerate(self.get_players()):
            p.participant.is_dropout = False
            p.participant.time_instructions = None
            p.participant.idx = np.random.randint(len(C.ORDERS))

    def creating_session(self):
        """
        set some attributes of the participant
        """
        if self.round_number == 1:
            # self.init()
            pass
 

class Player(BasePlayer):
    pass

class Group(BaseGroup):
    pass