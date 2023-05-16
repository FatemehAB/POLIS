
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

    # Want to be in the right most lane
    # With the highest possible average speed.
    # Pass the car if possible


    # Slow down if going to faster then car in same lane
    if(abs(s[1] - s[5]) < 2.7):
      # Check if you are going slower then the car. Adding a speed gap of 5
      # in order to counter balance reaction time
      if(s[2] < s[6] and s[2] < 25):
        action = 3
      else:
        action = 4

    elif(abs(s[1] - s[9]) < 2.7):
      if(s[2] < s[10] and s[2] < 25):
        action = 3
      else:
        action = 4

    # Go to the right most lane if empty thus the two nearest cars dont
    # have the same x position. An you are not going as fast as the car in front
    elif(s[1] < 8 and abs(s[0] - s[4]) < 5 and abs(s[0] - s[8]) < 5):
      action = 2

    # If no previous action speed up
    else:
      action = 3

        
    # example code for highway game

    # if my car (green) is not in the right-most lane, go to the right-most lane
    #if s[1] < 8:
        #action = 2
    #else:
        #action = 1

    return action
    