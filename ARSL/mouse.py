# https://github.com/boppreh/mouse#api
import mouse
import pygetwindow
import pyperclip
import PIL
#from runepy_common import logger
#from runepy_common import globals
#from runepy_controller import keyboard
#from runepy_module import screen

# [TODO] Implement xRange, yRange, and durationRange
# Possibly rename them to something more approriate mathematically? Smear?
def move(x, y, rel = False, duration = 0.1, xRange = 0, yRange = 0, durationRange = 0):
    #findRunescape()

    # [TODO] Fix this coordinate system complication across all functions
    #mouse.move(screen.coords[0] + x, screen.coords[1] + y, absolute = not rel, duration = duration)
    mouse.move(x, y, absolute = not rel, duration = duration)

# Change this to click(self, x = -1, y = -1, button = "left", holdPosition = True)
# Where -1 implies current position by default allowing movement to location by default
# holdPosition means it goes back to start otherwise allow you to move the mouse freely
def click(button = "left"):
    mouse.click(button)

# [TODO] Find out if this returns absolute or relative to window focus
# I think it's absolute screen, which can become an issue
def get_position():
    return mouse.get_position()

# [TODO] Find a way to factor out getting the pixel color without recalculating ImageGrab.grab()
def get_custom_overlay_color_value_in_range_PIL(xDelta, yDelta, goal):
    img = screen.get_screenshot()

    mouseLoc = mouse.get_position()
    x = mouseLoc[0] - screen.coords[0] + xDelta
    y = mouseLoc[1] - screen.coords[1] + yDelta

    # We don't want to crash if the mouse goes outside the bounds of the screen
    if x < screen.coords[0] or x >= screen.coords[2] or y < screen.coords[1] or y >= screen.coords[3]: return

    rgb = img.getpixel((x, y))

    # We don't care if the rgb doesn't match the goal
    # We can pass custom value calculation as an optimization
    if sum(rgb) != goal: return None

    # [NOTE] Aaron came up with this, I'm not that smart
    # It iterates over 'length' and calculates a custom value depending on the cursor overlay text
    # This is an arbitrary value that seems to work well
    length = 30

    totalA = 0
    for n in range(-length, length):
        rgbA = img.getpixel((x + n, y + 14))
        totalA += sum(rgbA)

    totalB = 0
    for n in range(-length, length):
        rgbB = img.getpixel((x + n, y + 10))
        totalB += sum(rgbB)

    total = int("{}{}".format(totalA, totalB))
    if total != 0: return total

    return total

    '''desktop = os.path.expanduser("~/Desktop")
    path = "{}/test.png".format(desktop)
    img.save(path)'''

# [TODO] Get the dang blasted coordinate system ironed out for pete's sake!
def get_cursor_info(xDelta = 0, yDelta = 0):
    p = get_position()
    img = screen.get_screenshot()
    pixel = img.getpixel((p[0], p[1]))

    string = "{} = {}".format(p, pixel)
    print(string)

    pyperclip.copy(string)
    spam = pyperclip.paste()

    return string

#i_desktop_window_id = win32gui.GetDesktopWindow()
#i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)

#logger.log("Mouse Controller Initiating")
#screen.findRunescape()
#keyboard.registerHotkey("ctrl+alt+c", get_cursor_info, "Grab Cursor Info")
