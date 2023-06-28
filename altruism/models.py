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
    NAME_IN_URL = 'altruism'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 4
    ENDOWMENT = 5
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
            self.init()


class Group(BaseGroup):
    order_idx = models.IntegerField(default=-1)
    group_id = models.StringField(default="")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.set_group_id()
        # self.set_condition()

    def set_condition(self):
        if self.round_number == 1:
            self.order_idx = np.random.randint(len(C.ORDERS))
        else:
            self.order_idx = self.in_round(1).order_idx

    def set_group_id(self):
        if self.round_number == 1:
            self.group_id = su.uuid()[:8]
        else:
            self.group_id = self.in_round(1).group_id


class Player(BasePlayer):
    contribution = models.IntegerField(default=-1)
    rt = models.IntegerField(default=-1)
    choice = models.StringField(default='')
    condition = models.IntegerField(default=-1)
    msg_clean = models.LongStringField(default='')
    msg_html = models.LongStringField(default='')
    msg_json = models.LongStringField(default='')
    order_idx = models.IntegerField(default=-1)

    def set_condition(self, condition: int):
        self.condition = condition

    def set_contribution(self, contribution: int):
        self.contribution = contribution

    def set_rt(self, rt: int):
        self.rt = rt

    def set_choice(self, choice: str):
        self.choice = choice

    def set_msg(self, msg_clean: str, msg_html: str, msg_json: str):
        self.msg_clean = msg_clean
        self.msg_html = msg_html
        self.msg_json = msg_json
    
    def set_order_idx(self, order_idx: int):
        self.order_idx = order_idx

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
        'prolific_id',
        'group_id',
        'id_in_session',
        'round_number',
        'contribution',
        'choice',
        'rt',
        'condition',
        'order_idx',
        'msg_clean',
        'msg_json',
        'msg_html'
    ]
    yield col
    for p in players:
        order_idx = getattr(p, 'order_idx', p.group.order_idx)
        row = [
            p.session.code,
            p.participant.label,
            p.group.group_id,
            p.id_in_subsession,
            p.round_number,
            p.contribution,
            p.choice,
            p.rt,
            p.condition,
            order_idx,
            p.msg_clean,
            p.msg_json,
            p.msg_html,
        ]
        yield row
