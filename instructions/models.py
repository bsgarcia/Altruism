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


class Subsession(BaseSubsession):

    def init(self):
        """
        this method is called only once
        :return:
        """
        logger.debug('Initialization of participant + instructions') 
        n_participant = self.session.num_participants
        logger.debug(f'N participants = {n_participant}')

        for i, p in enumerate(self.get_players()):
            p.participant.is_dropout = False
            p.participant.time_instructions = None

    def creating_session(self):
        """
        match according to deterministic good/bad, good/good, bad/bad
        """
        if self.round_number == 1:
            # pass
            self.init()

class Player(BasePlayer):
    pass

class Group(BaseGroup):
    pass