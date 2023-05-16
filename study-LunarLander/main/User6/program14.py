
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
    #if s[4] < 0:
    #  action = 3
    #elif s[4] > 0:
    #  action = 2
    #else:
    #  action = 0
    desired_vertical_speed = -0.75
    fireengine = 0
    if s[3] > desired_vertical_speed: 
      action = 0
    elif s[3] < desired_vertical_speed:
      fireengine = 1
    else: # if you're at you're desired speed, then...
      action = 0
    new_angular_speed = abs(s[6]/6)
    new_horizontal_speed = abs(s[2]/1.8)
    calc_on_horiz_coor = 0
    if fireengine == 1:
      if s[5] < 0: 
        action = 1
      elif s[5] > 0:
        action = 3
      else:
        calc_on_horiz_coor = 1
    elif calc_on_horiz_coor == 1:
      if s[0] < 0:
        action = 3
      elif s[0] > 0:
        action = 1
      else:
        action = 0
    else:
      action = 0
    #elif s[2] < 0:
    #  action = 2
    #elif s[2] > 0:
    #  action = 3
    #else:
    #  action = 0

      
    # please write your code here
    # example code for LunarLander

    # if the ship is near ground, fire main engine to reduce the speed
    #if s[1] < 0.2:
     #   action = 2
    #else:
    #    action = 0

    return action
    