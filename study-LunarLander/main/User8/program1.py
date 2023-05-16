
"""
Please wait for a few seconds after clicking on Finish and confirming it for the system to show you the final score of your policy. 
"""

def heuristic(s):
    """
    Args:
        env: The environment
        s (list): The state. Attributes:
                  s[0] is the horizontal coordinate
                  s[1] is the vertical coordinate
                  s[2] is the horizontal speed
                  s[3] is the vertical speed
                  s[4] is the angle
                  s[5] is the angular speed
                  s[6] 1 if first leg has contact, else 0
                  s[7] 1 if second leg has contact, else 0
    returns:
         action: The heuristic to be fed into the step function defined below to
            determine the next step and reward.
    """
    # Nop = 0, fire right engine = 1, main engine = 2, left engine = 3

    action = 0

    # please write your code here

    # example code for LunarLander

    # if the ship is near ground, fire main engine to reduce the speed
    if s[1] < 0.2:
        action = 2
    else:
        action = 0

    return action
    