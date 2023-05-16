
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
    Te = 0.01 

    # Landing
    if s[1] < 1.0:
  
      # if the ship is too fast, slow it down
      if s[3] < -0.1:
          action = 2
      else:
          # Angular correction
          if s[4] > 0.2:
              action = 3
          elif s[4] < -0.2:
              action = 1
          else:
              # Horizontal correction
              if s[4] > 0:
                  action = 3
              else:
                  action = 1
    else:
          # Horizontal correction
          if s[4] > 0:
              action = 3
          else:
              action = 1

    return action
    