
def heuristic(s):
    myCar_next_y = s[1] + s[3]
    myCar_next_x = s[0] + s[2]
    firstCar_next_y = s[5] + s[7]
    firstCar_next_x = s[4] + s[6]
    secondCar_next_y = s[9] + s[11]
    secondCar_next_x = s[8] + s[10]

    action = 1 #IDLE
    if myCar_next_y < 8:
        if abs(myCar_next_y - firstCar_next_y) < 4:
            if firstCar_next_x - myCar_next_x > 20:
                action = 2
            else:
                action = 4
        else:
            if abs(myCar_next_y - secondCar_next_y) < 4:
                if secondCar_next_x - myCar_next_x > 20:
                    action = 2
                else:
                    action = 4
            else:
                action = 2
    else:
        if abs(myCar_next_y - firstCar_next_y) < 4:
            if firstCar_next_x - myCar_next_x > 45:
                action = 3
            else:
                action = 4
        else:
            if abs(myCar_next_y - secondCar_next_y) < 4:
                if secondCar_next_x - myCar_next_x > 45:
                    action = 3
                else:
                    action = 4
            else:
                action = 3


    return action

