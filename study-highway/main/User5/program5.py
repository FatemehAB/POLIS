
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
    speed_collision1 = s[4] - s[0]
    speed_collision2 = s[8] -  s[0]
    #if s[5] < 2

    ### please write your code here

    # example code for highway game

    #check if speed is < 30

    #check if speeding up will cause a collision
    if ((s[1] == s[5]) and (speed_collision1 < s[2]+1)) or ((s[1] == s[9]) and (speed_collision2 < s[2]+1)):
      #check if switching lanes right is possible

      #check if it will hit car 1
      if ((s[0] <= s[4]) and (s[0] >= s[4] - 30)) and (s[1] == (s[5] - 1)):
            
        if speed_collision1 < s[2]*2:
          action = 4
        else:
          action = 1
                
      #check if it will hit car 2
      elif ((s[0] <= s[8]) and (s[0] >= s[8] - 30)) and (s[1] == (s[9] - 1)) :
              
        if speed_collision1 < s[2]*2:
          action = 4
        else:
          action = 1
            
      #change lanes right
      else:
        action = 2

    #speeding up will not cause collision
    else:

      if s[2] < 30:
        action = 3

      #check if switching lanes right is possible
      else:
        #check if it will hit car 1
        if ((s[0] <= s[4]) and (s[0] >= s[4] - 30)) and (s[1] == (s[5] - 1)):
          
          if speed_collision1 < s[2]*2:
            action = 4
          else:
            action = 1
              
        #check if it will hit car 2
        elif ((s[0] <= s[8]) and (s[0] >= s[8] - 30)) and (s[1] == (s[9] - 1)) :
            
          if speed_collision1 < s[2]*2:
            action = 4
          else:
            action = 1
          
        #change lanes right
        else:
          action = 2


    return action
