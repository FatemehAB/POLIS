
def heuristic(s):
    """
    Args:
        env: The environment
        s (list): The state. Attributes:
                  s[0] is your x position, approximate range is [100, 400]
                  s[1] is your y position, approximate range is [0, 8]
                  s[2] is your x speed, approximate range is [10, 30]
                  s[3] is your y speed, approximate range is [-3, 3]
                  s[4] is 1st car x position, approximate range is [100, 400]
                  s[5] is 1st car y position, approximate range is [0, 8]
                  s[6] is 1st car x speed, approximate range is [10, 30]
                  s[7] is 1st car y speed, approximate range is [-3, 3]
                  s[8] is 2nd car x position, approximate range is [100, 400]
                  s[9] is 2nd car y position, approximate range is [0, 8]
                  s[10] is 2nd car x speed, approximate range is [10, 30]
                  s[11] is 2nd car y speed, approximate range is [-3, 3]
    returns:
         action: The heuristic to be fed into the step function defined below to
            determine the next step and reward.
    """
    # left lane = 0, Nop = 1, right lane = 2, faster = 3, slower = 4

    ### please write your code here

    # move to the right-most lane and also maintain speed

    if s[1] < 8: # agent in the first or second lane
      action = 2
    else: # once in the right most lane, increase your speed using a simple PID controller (error = speed difference)
      if ((s[5] < 8) and (s[9] < 8)): # lane is empty; increase speed
        action = 3
      else: # avoid collision and still increase speed; also just focus on the nearest car
        if s[5] == 8:
          loc = s[4]
          vel = s[6]
        else:
          loc = s[8]
          vel = s[10]
        if loc < s[0]: # car behind me; increase speed
          action = 3    
        else: # car in front of me
          if vel < s[2]: # car is slower; decrease speed
            action = 4
          else:
            if loc - s[0] > 150: # faster car is much ahead; increase speed
              action = 3
            else: # faster car is close by; maintain speed
              action = 1

    
    # example code for highway game

    # if my car (green) is not in the right-most lane, go to the right-most lane
    # if s[1] < 8:
    #    action = 2
    # else:
    #    action = 1

    return action
    