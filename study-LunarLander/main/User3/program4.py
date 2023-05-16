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
  
    # balanced = False
    left = 1
    main = 2
    right = 3
    noop = 0

    # please write your code here
    # pos = (s[0], s[1])
    # # x_pos, y_pos = pos
    # x_pos = pos[0]
    # y_pos = pos[1]
    # speed = (s[2], s[3])
    # x_speed, y_speed = speed
    # x_speed = speed[0]
    # y_speed = speed[1]
    # angle = s[4]
    # angular_speed = s[5]
    
    # First lets try to balance out

    # target_angular_speed = angle / 5.0
    # angular_speed_thresh = 0.05

    # x_pos_thresh = 0.05
    # target_x_pos = 0
  
    # y_pos_thresh = 0.05
    # target_y_pos = 0.5
  
    # # Angled left

    # if abs(target_angular_speed - angular_speed) < angular_speed_thresh:
    #   # When balanced
    #   # action = main

      
    #   # First look at x-coord
    #   if x_pos < target_x_pos - x_pos_thresh:
    #     action = left
    #   elif x_pos > target_x_pos + x_pos_thresh:
    #     action = right
    #   elif y_pos < target_y_pos - y_pos_thresh:
    #     action = main
    #   elif y_pos > target_y_pos + y_pos_thresh:
    #     action = noop
    #   else:
    #     action = main

        
    # elif target_angular_speed - angular_speed < 0:
    #   action = left
    # elif target_angular_speed - angular_speed > 0:
    #   action = right
    # else:
    #   action = noop
  
    # example code for LunarLander

    # if the ship is near ground, fire main engine to reduce the speed
    # if s[1] < 0.2:
    #     action = 2
    # else:
    #     action = 0

    return action
    