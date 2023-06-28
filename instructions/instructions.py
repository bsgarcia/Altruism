from settings import pounds_per_point
from instructions.models import C
import numpy as np


def get_panels(m1=None, m2=None):
    return {
        1: """
        Welcome to the experiment! This experiment will take about 5 minutes.
        You will receive an endowment of £5.<br><br>
You now get to decide what to do with this endowment: you can donate part or all of it to a given charity, or
you can keep it.
There will be three rounds, one of which will be randomly chosen to be implemented. If you made a
positive donation in that round, then the amount you indicated will be donated in your name.
Anything you do not decide to donate will be 
given to you as a bonus payment for the study.

   <div class="quiz-question-text-container quiz-question-info-container magenta">
         <span class="quiz-question-text-item-icon fa-solid fa-info-circle magenta" style="font-size: 30px; margin-right: 1.5%; position: relative; top: 4px;"></span>
         <span class="quiz-question-text-item magenta"><b>Info</b>&nbsp;<br>
         Please note that only one out of three rounds will be actually selected and implemented (i.e. we will take care of
making the actual donation to the charity you’ve chosen in that selected round).
        </span>
        </div>
        A round consists of two choices:<br>
        <b>1. a donation recipient</b> (from a list of charities). A short description of the charity and its activities appears when you click the &quot;read more&quot; button.<br>
       <b> 2. a donation amount (£0-£5)</b>
            
         """,
         2:"""
 <div class="quiz-question-text-container quiz-question-info-container magenta">
         <span class="quiz-question-text-item-icon fa-solid fa-info-circle magenta" style="font-size: 30px; margin-right: 1.5%; position: relative; top: 4px;"></span>
         <span class="quiz-question-text-item magenta"><b>Info</b>&nbsp;<br>
         The first round is a test round for you to get familiarized with the process. The decision you make in the test round will not be implemented, but please behave as if it
were.
After the test round the actual decision-making will begin.
        </span>
        </div>

         If you wish, you can indicate your email address at the end of the experiment, so that we can send
you the receipt of the donation that was made in the scope of the experiment to your chosen
charity.<br><br>
After the three rounds, you will be redirected to a questionnaire that you need to fill
in in order to receive your payment from Prolific.<br><br>
<p id="count">Ready? You can start the experiment in <b>100</b> second(s).</p>

         """
         

    }


titles = {
    1: 'Instructions 1/2',
    2: 'Instructions 2/2',
}
