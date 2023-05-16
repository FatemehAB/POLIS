
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

    action = 1

    ### please write your code here

    # example code for highway game

    # if my car (green) is not in the right-most lane, go to the right-most lane
    if s[1] < 8: # if not in right-most lane
        if abs(s[4] - s[0]) >= 4: # if no car on right
          action = 2 # go right
        else: # if car on right
          if s[2] >= s[6]: # if going faster or equal speed to car on right
            action = 4 # slow down
          else: # if slower than car on right
            action = 1 # do nothing
    else:
        if s[2] > s[6] and abs(s[5] - s[1]) <= 1: # if going faster than 1st closest and in the same lane
          action = 4
        else:
          action = 1
          
    return action
    