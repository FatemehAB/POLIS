
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

    your_x_pos = s[0]
    your_y_pos = s[1]
    your_x_spd = s[2]
    your_y_spd = s[3]
    car1_x_pos = s[4]
    car1_y_pos = s[5]
    car1_x_spd = s[6]
    car1_y_spd = s[7]
    car2_x_pos = s[8]
    car2_y_pos = s[9]
    car2_x_spd = s[10]
    car2_y_spd = s[11]


    # if your_x_pos > 100:
    #     action = 4
    # else:
    # If there is a car in the lane, move back up.
    if (car1_y_pos == your_y_pos and car1_x_pos < your_x_pos and your_x_pos - car1_x_pos  < 100) or (car2_y_pos == your_y_pos and car2_x_pos < your_x_pos and your_x_pos - car2_x_pos  < 100):
         action = 0
    # If there is a car in the right lane, do not move.
    elif (car1_y_pos == your_y_pos + 4 and car1_x_pos < your_x_pos and your_x_pos - car1_x_pos  < 100) or (car2_y_pos == your_y_pos + 4 and car2_x_pos < your_x_pos and your_x_pos - car2_x_pos < 100):
        action = 1
    else:
        action = 2

    return action
    