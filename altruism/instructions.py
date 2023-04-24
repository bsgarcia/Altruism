from settings import pounds_per_point
from altruism.models import Constants
import numpy as np


def get_panels(m1=None, m2=None):
    return {
        1: """
        Welcome to the experiment! This experiment will take about 15 minutes. You have 5 minutes to
read these instructions. After that, you will be randomly paired with another participant.

         <div class="quiz-question-text-container quiz-question-info-container orange">
         <span class="quiz-question-text-item-icon fa-solid fa-warning orange" style="font-size: 30px; margin-right: 1.5%; position: relative; top: 4px;"></span>
         <span class="quiz-question-text-item green"><b>Warning</b>&nbsp;<br>
         To avoid
waiting times for other participants, please note that if you are inactive for more than one minute,
you will be excluded from the experiment and your submission on Prolific will be rejected.
        </span>
        </div>
        """,
        2: """
        You and the other participant will receive a joint endowment of £10.
You now get to decide together what to do with this endowment: you can donate part or all of it to a given charity, or
you can keep it.
There will be three rounds, one of which will be randomly chosen to be implemented. If you made a
positive donation in that round, then the amount you indicated will be donated in your name.
Anything you do not decide to donate will be split evenly between you and the other participant and
given to you as a bonus payment for the study.

   <div class="quiz-question-text-container quiz-question-info-container magenta">
         <span class="quiz-question-text-item-icon fa-solid fa-info-circle magenta" style="font-size: 30px; margin-right: 1.5%; position: relative; top: 4px;"></span>
         <span class="quiz-question-text-item magenta"><b>Info</b>&nbsp;<br>
         Please note that only one out of three rounds will be actually implemented (i.e. we will take care of
making the actual donation to the charity you’ve chosen in that selected round).
        </span>
        </div>
        A round consists of two choices:<br>
        <b>1. a donation recipient (from a list of charities) </b>
        <div class="inst-video">
            <video width="640" height="480" controls autoplay loop muted>
            <source src="/static/video/select_charity.mp4" type="video/mp4" />
            Your browser does not support the video tag.
            </video>
            </div>
        <b>...a short description of the charity and its activities appears when you click the &quot;read more&quot; button.</b>
        <div class="inst-video">
            <video width="640" height="480" controls autoplay loop muted>
            <source src="/static/video/read_description.mp4" type="video/mp4" />
            Your browser does not support the video tag.
        </video>
        </div>
       <b> 2. a donation amount (£0-£10)</b>
            
            <div class="inst-video">
            <video width="640" height="480" controls autoplay loop muted>
            <source src="/static/video/select_amount.mp4" type="video/mp4" />
            Your browser does not support the video tag.
            </video>
            </div>

         """,
         3: """
        In order to make a decision, you have to coordinate with the other participant. You both have to
choose the same donation recipient and amount. You can update both of your choices (charity and
amount) at any time.
         
   <div class="quiz-question-text-container quiz-question-info-container orange">
         <span class="quiz-question-text-item-icon fa-solid fa-info-circle orange" style="font-size: 30px; margin-right: 1.5%; position: relative; top: 4px;"></span>
         <span class="quiz-question-text-item orange"><b>Warning</b>&nbsp;<br>
         If you fail to coordinate with the other participant (coordination means make
exactly the same decision regarding charity and amount), no donation will be made and neither of
you will receive a bonus payment.
        </span>
        </div>

        To facilitate coordination with the other participant, you can use the chat window which will open
automatically once you have clicked on a charity. You have to choose between predefined messages
that allow you to make suggestions about your preferred donation recipient and amount, and react
to the other participant’s suggestions.
Once you have agreed on both choices (charity and amount), you have to send your partner the
message “I will validate” in order to enable the validation button. After clicking the validation
button, the subsequent round will start (there are three rounds in total).

   <div class="inst-video">
            <video width="640" height="480" controls autoplay loop muted>
            <source src="/static/video/chat_validate.mp4" type="video/mp4" />
            Your browser does not support the video tag.
        </video>
        </div>

          <div class="quiz-question-text-container quiz-question-info-container orange">
         <span class="quiz-question-text-item-icon fa-solid fa-info-circle orange" style="font-size: 30px; margin-right: 1.5%; position: relative; top: 4px;"></span>
         <span class="quiz-question-text-item orange"><b>Warning</b>&nbsp;<br>
You have to send “I will validate” in order to enable the validation button and continue to the next
round.
        </span>
        </div>
         """,
         4: """
         If you wish, you can indicate your email address at the end of the experiment, so that we can send
you the receipt of the donation that was made in the scope of the experiment to your chosen
charity.<br><br>
After the three rounds, you will be redirected to a questionnaire that you need to fill
in in order to receive your payment from Prolific.<br><br>
Ready? The experiment will start automatically in <b>100</b> second(s).

         """
         

    }


titles = {
    1: 'Welcome!',
    2: 'Instructions 1/3',
    3: 'Instructions 2/3',
    4: 'Instructions 3/3',
}
