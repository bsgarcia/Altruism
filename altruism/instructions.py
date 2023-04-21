from settings import pounds_per_point
from altruism.models import Constants
import numpy as np


def get_panels(m1=None, m2=None):
    return {
        1: """
        Welcome to the experiment! You have been randomly paired with another participant and together, you have received a bonus payment of $10. 
         You now get to decide together what to do with this bonus: you can donate part or all of it or you can keep it.
        """,
        2: """
         We will ask you to make three decisions, one of which will be randomly chosen to be implemented. If you made a positive donation in that decision, then the amount you indicated will be donated in your name. Anything you do not decide to donate will be split evenly between you and the other participant and given to you as a bonus payment for the study. 
            A donation decision consists of the choice of two parameters:<br>
            -a donation recipient (from a list of charities) <br>
            <div class="inst-video">
            <video width="640" height="480" controls autoplay loop muted>
            <source src="/static/video/select_charity.mp4" type="video/mp4" />
            Your browser does not support the video tag.
            </video>
            </div>

            - when you select a charity, a short description of the charity and its activities appears when you click the "read more" button.
             <div class="inst-video">
            <video width="640" height="480" controls autoplay loop muted>
            <source src="/static/video/read_description.mp4" type="video/mp4" />
            Your browser does not support the video tag.
        </video>
        </div>

            -a donation amount ($0-$10). 
            <div class="inst-video">
            <video width="640" height="480" controls autoplay loop muted>
            <source src="/static/video/select_amount.mp4" type="video/mp4" />
            Your browser does not support the video tag.
            </video>
            </div>



         """,
         3: """
         In order to make a decision, you have to coordinate with the other participant. You both have to choose the same donation recipient and amount. If you fail to do so, no donation will be made and you will not receive a bonus payment.
         To facilitate coordination with the other participant, you can use the chat window. 
         You can choose between predefined sentences that allow you to make suggestions about your preferred donation recipient and amount, and react to the other participant’s suggestions.
         

         Once you have chosen the charity and the amount (or chose to keep the money), please click on “validate”. 

         <div class="inst-video">
            <video width="640" height="480" controls autoplay loop muted>
            <source src="/static/video/chat_validate.mp4" type="video/mp4" />
            Your browser does not support the video tag.
        </video>
        </div>
         """,
         4: """
         If you click on a charity, a short description of the charity and its activities appears to help you make an informed decision. Additionally, we included ratings by the independent charity assessment organization “Charity Navigator”, which are based on the charities’ financial stability, adherence to best practices for both accountability and transparency, and results reporting. Charity Navigator is the largest and most-utilized evaluator of charities in the United States. It does not accept any advertising or donations from the organizations it evaluates.
If you wish, you can indicate your email address at the end of the experiment, so that we can send you the receipt of the donation that was made in the scope of the experiment to your chosen charity. 
After having made the three decisions, you will be redirected to a questionnaire that you need to fill in in order to receive your payment from Prolific.
         """

    }


titles = {
    1: 'Welcome!',
    2: 'Instructions 1/3',
    3: 'Instructions 2/3',
    4: 'Instructions 3/3',
}
