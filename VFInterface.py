import numpy as np
import cv2
import mss
from pynput.mouse import Button, Controller
import time

mouse = Controller()

CLICK_DELAY = 0.5

SCREEN_X = 971
SCREEN_Y = 192
START_SQUARE = 64
SQUARE_WIDTH = 120
QUIT_X = 828
QUIT_Y = 652
YES_X = 828
YES_Y = 322
PLAY_X = 606
PLAY_Y = 293
CLEAR_X = 154
CLEAR_Y = 582
TEXTBOX_COLOUR = np.array([223, 134, 182, 255])
SQUARE_REVEALED_COLOUR = np.array([134, 142, 190, 255])
VOLTORB_COLOUR = np.array([85, 117, 231, 255])
PLAY_BUTTON_COLOUR = np.array([182, 199, 125, 255])
DARK_DIGIT_COLOUR = np.array([69, 69, 69, 255])
SOLVED_COLOUR = np.array([60, 85, 28, 255])
MAXED_COLOUR = np.array([239, 239, 231, 255])
VERTICAL_NUMS_X = 653
VERTICAL_NUMS_Y = 19
HORIZONTAL_NUMS_X = 53
HORIZONTAL_NUMS_Y = 619
NUM_EXTRA_RIGHT = 30
NUM_EXTRA_DOWN = 49

zero = cv2.imread('images/digits/digit-0.png',0)
one = cv2.imread('images/digits/digit-1.png',0)
two = cv2.imread('images/digits/digit-2.png',0)
three = cv2.imread('images/digits/digit-3.png',0)
four = cv2.imread('images/digits/digit-4.png',0)
five = cv2.imread('images/digits/digit-5.png',0)
six = cv2.imread('images/digits/digit-6.png',0)
seven = cv2.imread('images/digits/digit-7.png',0)
eight = cv2.imread('images/digits/digit-8.png',0)
nine = cv2.imread('images/digits/digit-9.png',0)
game_clear = cv2.imread('images/gameclear.png',0)

digits = [zero,one,two,three,four,five,six,seven,eight,nine]

def get_screenshot():
    with mss.mss() as sct:
        monitor = {'top': SCREEN_Y, 'left': SCREEN_X, 'height': 709, 'width': 938}
        screen = np.array(sct.grab(monitor))
        return screen

def get_digit(digit_img):
    digit = 0
    gray_digit = cv2.cvtColor(digit_img, cv2.COLOR_BGR2GRAY)

    for d in range(0,10):
        # Find digit match
        res = cv2.matchTemplate(gray_digit,digits[d],cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if(max_val > 0.90):
            digit = d
            #print(f"Digit found: {digit}")
            break

    return digit

def get_inside_digit(digit_img):
    digit = 0

    bgr = digit_img[17][2]

    if bgr.tolist() == np.array([174,182,166,255]).tolist():
        digit = 2
    elif bgr.tolist() == SQUARE_REVEALED_COLOUR.tolist():
        digit = 1
    elif bgr.tolist() == np.array([255,255,255,255]).tolist():
        digit = 3
    else:
        print("Digit not found!")
        return -2

    print(f"Digit found: {digit}")

    return digit

def is_textbox():
    screen = get_screenshot()
    
    if screen[624][16].tolist() == TEXTBOX_COLOUR.tolist():
        return True
    else:
        return False

def check_maxed():
    screen = get_screenshot()

    if screen[13][782].tolist() == MAXED_COLOUR.tolist():
        print("\n~~MAX COINS~~")
        return True
    else:
        return False

def check_solved():
    screen = get_screenshot()

    """
    region = screen[CLEAR_Y:CLEAR_Y + 26, CLEAR_X:CLEAR_X + 60]
    region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(region,game_clear,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 0.95) or screen[PLAY_Y][PLAY_X].tolist() == PLAY_BUTTON_COLOUR.tolist():
        print("\n~~GAME FINISHED~~")
        return True
    else:
        return False
    """

    if screen[9][9].tolist() != SOLVED_COLOUR.tolist():
        # Click
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)
        time.sleep(CLICK_DELAY)

    if screen[9][9].tolist() == SOLVED_COLOUR.tolist():
        print("\n~~GAME SOLVED~~")
        return True
    else:
        return False

def check_textbox():
    screen = get_screenshot()
    
    while screen[624][16].tolist() == TEXTBOX_COLOUR.tolist():
        # Move mouse
        #mouse.position = (SCREEN_X + 16, SCREEN_Y + 552)

        # Click
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)

        screen = get_screenshot()

    time.sleep(CLICK_DELAY)
        
    #print("Clicked textboxes")

def click_play():
    screen = get_screenshot()

    # Only if textbox present
    if screen[624][16].tolist() == TEXTBOX_COLOUR.tolist():
        while screen[PLAY_Y][PLAY_X].tolist() != PLAY_BUTTON_COLOUR.tolist():

            # Move mouse
            #mouse.position = (PLAY_X + SCREEN_X, PLAY_Y + SCREEN_Y)

            # Click
            mouse.press(Button.left)
            time.sleep(0.01)
            mouse.release(Button.left)

            screen = get_screenshot()

        time.sleep(CLICK_DELAY)

        mouse.position = (PLAY_X + SCREEN_X, PLAY_Y + SCREEN_Y)
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)

        time.sleep(CLICK_DELAY)

        print("Clicked play")

        return True
    else:
        return False

def click_to_play():
    screen = get_screenshot()

    # Move mouse
    mouse.position = (1 + SCREEN_X, 1 + SCREEN_Y)

    while screen[PLAY_Y][PLAY_X].tolist() != PLAY_BUTTON_COLOUR.tolist():

        # Click
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)

        screen = get_screenshot()

    time.sleep(CLICK_DELAY)

def check_game_over(x,y):
    screen = get_screenshot()
    
    if screen[y-SCREEN_Y][x-SCREEN_X].tolist() == VOLTORB_COLOUR.tolist():
        print("\n~~VOLTORB FOUND~~")
        click_to_play()
        return True
    else:
        return False
        

def click_tile(row, col):
    x = SCREEN_X + START_SQUARE + col * SQUARE_WIDTH
    y = SCREEN_Y + START_SQUARE + row * SQUARE_WIDTH

    screen = get_screenshot()

    # Move mouse
    mouse.position = (x,y)

    while screen[y+32-SCREEN_Y][x+32-SCREEN_X].tolist() != SQUARE_REVEALED_COLOUR.tolist() and screen[PLAY_Y][PLAY_X].tolist() != PLAY_BUTTON_COLOUR.tolist():

        # Click
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)

        screen = get_screenshot()

    print(f"Clicked tile ({row},{col})")
    time.sleep(CLICK_DELAY * 2)

    if check_game_over(x,y) == True:
        return -1
    else:
        #check_textbox()
        mouse.position = (SCREEN_X + 1, SCREEN_Y + 1)

        # Click
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)

        screen = get_screenshot()
        
        # Get img of digit
        digit_img = screen[y-15-SCREEN_Y : y+15-SCREEN_Y, x-11-SCREEN_X : x+11-SCREEN_X]

        #time.sleep(0.2)

        inside_digit = get_inside_digit(digit_img)

        #print(inside_digit)

        return inside_digit

def restart_game():
    screen = get_screenshot()

    # Move to quit button
    mouse.position = (QUIT_X + SCREEN_X, QUIT_Y + SCREEN_Y)

    # Wait for yes, then press
    while screen[YES_Y][YES_X].tolist() != np.array([255,255,255,255]).tolist():

        # Click
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)

        screen = get_screenshot()

    time.sleep(CLICK_DELAY)

    # Click YES
    mouse.position = (YES_X + SCREEN_X, YES_Y + SCREEN_Y)

    # Click
    mouse.press(Button.left)
    time.sleep(0.01)
    mouse.release(Button.left)

    while screen[PLAY_Y][PLAY_X].tolist() != PLAY_BUTTON_COLOUR.tolist():

        # Click
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)

        screen = get_screenshot()

    time.sleep(CLICK_DELAY)

    print("Clicked quit")

def read_board():
    screen = get_screenshot()

    # [[horiz-totals, vert-totals], [horiz-orbs, vert-orbs]]
    info = [[[],[]],[[],[]]]

    # Get nums
    for num in range(0, 5):
        # Get horizontal
        start_x = HORIZONTAL_NUMS_X + (SQUARE_WIDTH * num)
        start_y = HORIZONTAL_NUMS_Y

        digit = 0
        # Test for first digit 1 or 0
        if screen[start_y + 8][start_x + 1].tolist() != DARK_DIGIT_COLOUR.tolist():
            digit += 10

        # Second total digit
        # Get img of digit
        digit_img = screen[start_y:start_y + 30, start_x + NUM_EXTRA_RIGHT: start_x + NUM_EXTRA_RIGHT + 22]

        digit += get_digit(digit_img)

        info[0][0].append(digit)

        # Voltorb num
        # Get img of digit
        digit_img = screen[start_y + NUM_EXTRA_DOWN:start_y + NUM_EXTRA_DOWN + 30, start_x + NUM_EXTRA_RIGHT: start_x + NUM_EXTRA_RIGHT + 22]

        digit = get_digit(digit_img)
        info[1][0].append(digit)

        # Get vertical
        start_x = VERTICAL_NUMS_X
        start_y = VERTICAL_NUMS_Y + (SQUARE_WIDTH * num)

        digit = 0
        # Test for first digit 1 or 0
        if screen[start_y + 8][start_x + 1].tolist() != DARK_DIGIT_COLOUR.tolist():
            digit += 10

        # Second total digit
        # Get img of digit
        digit_img = screen[start_y:start_y + 30, start_x + NUM_EXTRA_RIGHT: start_x + NUM_EXTRA_RIGHT + 22]

        digit += get_digit(digit_img)

        info[0][1].append(digit)

        # Voltorb num
        # Get img of digit
        digit_img = screen[start_y + NUM_EXTRA_DOWN:start_y + NUM_EXTRA_DOWN + 30, start_x + NUM_EXTRA_RIGHT: start_x + NUM_EXTRA_RIGHT + 22]

        digit = get_digit(digit_img)
        info[1][1].append(digit)

    return info

def test_tile_read(row, col):
    x = SCREEN_X + START_SQUARE + col * SQUARE_WIDTH
    y = SCREEN_Y + START_SQUARE + row * SQUARE_WIDTH
    
    screen = get_screenshot()
        
    # Get img of digit
    digit_img = screen[y-15-SCREEN_Y : y+15-SCREEN_Y, x-11-SCREEN_X : x+11-SCREEN_X]

    #time.sleep(0.2)

    inside_digit = get_inside_digit(digit_img)

def test_voltorb(row, col):
    x = SCREEN_X + START_SQUARE + col * SQUARE_WIDTH
    y = SCREEN_Y + START_SQUARE + row * SQUARE_WIDTH

    check_game_over(x,y)

def fail_click(row, col):
    x = SCREEN_X + START_SQUARE + col * SQUARE_WIDTH
    y = SCREEN_Y + START_SQUARE + row * SQUARE_WIDTH

    # Move mouse
    mouse.position = (x,y)

    time.sleep(CLICK_DELAY * 2)

    # Click
    mouse.press(Button.left)
    time.sleep(CLICK_DELAY)
    mouse.release(Button.left)

    start_time = time.time()

    while (time.time() - start_time) < 30:

        # Move mouse
        mouse.position = (x,y)

        time.sleep(CLICK_DELAY)
