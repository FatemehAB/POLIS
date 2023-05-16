
def heuristic(s):
    """
    Args:
        env: The environment
        s (list): The state. Attributes:
                  s[0] is the horizontal coordinate, approximate range is [-1, 1]
                  s[1] is the vertical coordinate, approximate range is [-0.4, 1.7]
                  s[2] is the horizontal speed, approximate range is [-1.8, 1.8]
                  s[3] is the vertical speed, approximate range is [-2, 0.5]
                  s[4] is the angle, approximate range is [-3, 3]
                  s[5] is the angular speed, approximate range is [-6, 6]
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

    # make small adjustment at beginning to ensure longer time to make adjustment (decrease vert speed)
    if s[1] > 1 and s[1] < 1.1 and (s[4] < 0.12):
        action = 2
    elif s[1] > 1 and s[3] < -0.7 and s[0] < -0.05:
      action = 3
    elif s[1] > 1 and s[3] < -0.8 and s[0] > 0.05:
      action = 1
    # if we're off centre because we're off to the left, fire left engine
    elif s[0] < -0.15 and s[4] > 0.1 and s[0] < 0:
      action = 3
    # if we're off centre because we're off to the right, fire right engine
    elif s[0] < 0.13 and s[4] < -0.1 and s[0] > 0:
      action = 1
    # when coming close to ground fire main engine to slow down descent
    elif s[1] < 0.8 and s[1] > 0.3:
      action = 2
    # make small adjustments to left-right alignment when near ground
    elif s[1] <= 0.3 and s[4] > 0.09:
      action = 3
    elif s[1] <= 0.3 and s[4] < -0.09:
      action = 1
    elif s[1] <= 0.3 and s[3] < 0:
      action = 2
    else:
        action = 0

    return action
    