
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
    edge_boundary = 0.05
    tip_over_edge = -0.08
    ovverrotation = 0.15
    edge_falling_speed = 0.4
    low_height_ovverride = 0.2
    height_override = 0.5
    high_speed = 1
    slow_speed = 0.3

    if s[0] < neg(edge_boundary):
      if s[4] > tip_over_edge:
        action = 3
      else:
        if s[5] < neg(ovverrotation):
          action = 1
        else:
          if s[1] < low_height_ovverride:
            action = 2
          elif s[3] < neg(edge_falling_speed):
            action = 2
          else:
            action = 0
        
    elif s[0] > edge_boundary:
      if s[4] < neg(tip_over_edge):
        action = 1
      else:
        if s[5] > ovverrotation:
          action = 3
        else:
          if s[1] < low_height_ovverride:
            action = 2
          elif s[3] < neg(edge_falling_speed):
            action = 2
          else:
            action = 0
        
    else:
      if s[1] > height_override:
        if s[3] > neg(high_speed):
          if s[4] < tip_over_edge and s[4] > neg(tip_over_edge):
            action = 0
          else:
            if s[5] > 0:
              action = 3
            else:
              action = 1
        else:
          action = 2
      else:
        if s[3] < neg(slow_speed):
          action = 2
        else:
          action = 0

    return action
    