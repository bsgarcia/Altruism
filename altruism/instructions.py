from settings import pounds_per_point
from altruism.models import Constants
import numpy as np


def two_players(m1, m2, t1, t2):
    s = f'''<div class="row">
    <div class="col">
    <div class="box" align="center">
    <img width="80%" src="/static/img/{m1}.gif">
    <div style="font-size: 25px" class="text-centered">{t1}</div>
    </div>
    </div>
    <div class="col">
    <div class="box" align="center">
    <img width="80%" style="-webkit-transform: scaleX(-1);transform: scaleX(-1);" src="/static/img/{m2}.gif">
    <div style="left: 6%; font-size: 25px;" class="text-centered">{t2}</div>
    </div>
    </div>
    </div><br><br>'''
    return s


def get_panels(m1=None, m2=None):
    return {
        1: '<p>'
           'You are about to participate in an experiment on decision-making in economics. '
           'This study is based on your voluntary participation and your data will be treated confidentially and anonymously.'
           'This experiment is composed of four phases: <br>'
           '1) Instructions<br>'
           '2) A short training game.<br>'
           '3) A game<br>'
           '4) A short survey<br>'
         #   '<b>Please note that from now on you have 9 minutes to read these instructions. <br>'
         #   'After that the game will start automatically.</b>'
           '</p>',

        2: '<p>'
           'In the game there are <b>two types</b> of players: the <b style="color: #5893f6">blue</b> and <b style="color: #d4c84d">yellow</b> one.'
           'You will be randomly attributed to one color in the beginning of the game.'
           'Your type will <b>remain</b> the same all along the game.<br>'
           'Note that different types have different multipliers (the latter is displayed on the character t-shirt).'
           '<br><br>' + two_players(Constants.multiplier_good, Constants.multiplier_bad, Constants.multiplier_good, Constants.multiplier_bad) +
           f'In total there are <b>{Constants.num_rounds - 3} rounds</b> (+ 3 training rounds). '
           f'A round is divided into 3 steps:<br><br>'
           '1) You will be randomly matched with a robot player, controlled by the computer. Then you will be asked to either disclose or hide your multiplier, so that the other player will know your type or not. <br><br>'
           '2) You will be asked to contribute (a certain number of points) to a public pot.<br><br>'
           '3) Your contribution will be multiplied according to your type and the points put in the public pot'
           ' will be equally distributed among you and the artificial player. <br><br>'
           'Thereafter, you will continue to the next round.<br>'
           '</p>',

        3: '<p>'
           'In the beginning of each round you will be presented with your character and your multiplier. '
           'You will be also asked whether or not you want to <b>disclose it</b>.<br> '
           'If you choose to disclose it, the <b>other player</b> will be <b>informed</b> of this information,'
           ' in the contribution step. '
           f' Also, <b>{Constants.disclosure_cost} points</b> will be removed from your private wallet.'
           'Conversely, if you choose to hide it, the <b>other player</b> will see your character hiding her/his multiplier'
           ' by means of a sign in the <b>contribution step</b>.<br>'
           '<br>Suppose you were attributed the <b style="color: #5893f6">blue</b> type and the other player the <b style="color: #d4c84d">yellow</b>'
           '. There are 4 possible "disclosure" situations:<br><br>'
           '<b>1) You both disclose</b> <br><br>' + two_players(Constants.multiplier_good, Constants.multiplier_bad,
                                                                Constants.multiplier_good, Constants.multiplier_bad) +
           '<b>2) You both hide</b> <br><br>' + two_players(None, None, '...', '...') +
           '<b>3) You disclose and the other player hides</b> <br><br>' + two_players(Constants.multiplier_good, None,
                                                                                      Constants.multiplier_good, '...') +
           '<b>4) You hide and the other player discloses</b> <br><br>' + two_players(None, Constants.multiplier_bad, '...',
                                                                                      Constants.multiplier_bad) +
           '<br><br><b> Please note that you have 120 seconds to choose to disclose or hide your multiplier, if you take more time, you will be disconnected.<br>'
           '<p>',

        4: '<p>'
           'In the second step of the round, you will see the outcome of the previous decision, that is one of the <b>4 "disclosure" situations</b>.'
           '<br><br>Also, in each round, your private wallet  will be <b>endowed with 10 points</b>, and you will be asked to contribute to the public pot. '
           f' Please note that if you chose to disclose your multiplier in the previous step, <b>{Constants.disclosure_cost} points</b> will be'
           f' substracted from your initial endowment, which lets you with <b>{Constants.endowment - Constants.disclosure_cost} points</b>.'
           'You will be able to do so '
           'using a slider, which value corresponds to the number of points you want to put in the public pot. <br>'
           'To select a value on the slider you can either select with your mouse cursor, either using your left and right arrow keys on your keyboard.'
           f' The maximum contribution is 10 if you hide your multiplier (8 if you disclose), while the minimum is 0.<br>'
           '<br><div align="center"><img src="/static/img/contribute.gif"><br></div>'
           '<br><b> Please note that you have 120 seconds to give your contribution, if you take more time, you will be disconnected.<br>'
           '</p>',
        5: '<p>'
           'In the third step of the round, you will see the <b>outcome</b> of the <b>contribution step</b>. '
           'Your type, as well as the type of the player with whom you have played will be revealed.<br>'  
           f'<br><br>Suppose you are a <b style="color: #d4c84d">yellow</b> player, your contribution to the public pot will be multiplied by <b style="color: #d4c84d">{Constants.multiplier_bad}</b>. '
           f'Suppose you chose to contribute 10 points to the public pot, then your final contribution will be {Constants.multiplier_bad * 10} because 10x<b style="color: #d4c84d">{Constants.multiplier_bad}</b> = {Constants.multiplier_bad * 10}.<br>'
           '<br>Suppose the other player is <b style="color: #5893f6">blue</b> and chose to contribute also 10 points to the public pot, '
           f' then his/her final contribution will be {Constants.multiplier_good * 10} because 10x <b style="color: #5893f6">{Constants.multiplier_good}</b> = {Constants.multiplier_good * 10} <br>'
           '<br><br>The total contribution (the sum of both player contribution) is then distributed equally among the players such that:<br>'
           f'<div align="center">IND. SHARE = {(Constants.multiplier_good * 10 + Constants.multiplier_bad * 10) / 2} = ((10x<b style="color: #d4c84d">{Constants.multiplier_bad}</b>) + (10x<b style="color: #5893f6">{Constants.multiplier_good}</b>))/2</div>'
           f'<br>It means that both player individual share is {round((Constants.multiplier_good * 10 + Constants.multiplier_bad * 10) / 2)} points for this hypothetical round. <br><br>'
           '<b>Please note that the payoff you will receive is your individual share added to the points left in your private wallet. In the fictional example above, there are no points letft '
           'in your private wallet because you contributed the maximum number of points.<b><br><br>'
           f'<b>Please note that payoffs from all the {Constants.num_rounds - 3} rounds are summed at the end of the experiment. This sum is used to compute your bonus compensation.'
           ' Also note that the first 3 training rounds are not used to compute your bonus.</b><br><br>'
           'Regarding your bonus compensation, here is the conversion: <br>'
           f' 1 point = {np.round(pounds_per_point * 100, 2)} pence <br>'
           f' 333 points =  {np.round(333 * pounds_per_point, 2)} pound <br>'
           f'Note that you can win up to {np.round(pounds_per_point * 25 * (Constants.num_rounds - 3), 2)} pound(s) as a bonus compensation.'
           '</p>',
        6: '<p>'
           '<br><br><b>Click on "next" to start the training game.</b>'
           '<p>'
    }

titles = {
    1: 'Welcome!',
    2: 'Short summary of the game',
    3: 'Disclosure',
    4: 'Contribution',
    5: 'Results',
    6: 'End of the instructions'
}
