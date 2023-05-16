
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

    action = 0

    ### please write your code here

    if s[5] == s[1]:
        if s[10] < s[6] and (s[8] - s[0]) < 30:
            if s[2] > s[6]:
                action = 4
            elif s[2] < s[6]:
                action = 3
            else:
                action = 1
        elif s[1] < 3.9999:
          action = 2
        elif s[1] < 4.0001:
          action = 0
        else:
            if s[9] > s[1]:
                action = 0
            elif s[9] < s[1]:
                action = 2
            else:
                action = 0
    elif s[2] > s[6]:
        action = 4
    else:
        action = 1

    return action
    