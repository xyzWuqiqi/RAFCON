import gtk.gdk

FONT_NAMES = ["DIN Next LT Pro", "FontAwesome"]
STYLE_NAMES = ["awesome_style.xml"]
FONT_STYLE_PATHS = {"DIN Next LT Pro":    "themes/dark/fonts/DIN Next LT Pro",
                    "FontAwesome":        "themes/dark/fonts/FontAwesome.otf",
                    "awesome_style.xml":  "themes/dark/gtksw-styles/awesome_style.xml"}

ICON_FONT = FONT_NAMES[1]
FONT_SIZE_SMALL = "10"
FONT_SIZE_NORMAL = "12"
FONT_SIZE_BIG = "14"

LETTER_SPACING_NONE = "0"
LETTER_SPACING_05PT = "512"
LETTER_SPACING_075PT = "756"
LETTER_SPACING_1PT = "1024"
LETTER_SPACING_2PT = "2048"
LETTER_SPACING_3PT = "3072"

# Cursors
MOVE_CURSOR = gtk.gdk.FLEUR
SELECT_CURSOR = gtk.gdk.HAND1
CREATION_CURSOR = gtk.gdk.CROSS


MAX_VALUE_LABEL_TEXT_LENGTH = 7

BORDER_WIDTH_ROOT_STATE = 5.
BORDER_WIDTH_HIERARCHY_SCALE_FACTOR = 2.


MAIN_WINDOW_BORDER_WIDTH = 3
BORDER_WIDTH = 5
BORDER_WIDTH_TEXTVIEW = 10
BUTTON_BORDER_WIDTH = 5
BUTTON_MIN_WIDTH = 90
BUTTON_MIN_HEIGHT = 30

PADDING = 5

PANE_MARGIN = 46

ICON_SIZE_IN_PIXEL = 20
ICON_MARGIN = 10

# The codes written down here are the codes provided on the font_awesome website
BUTTON_EXP = "f065"
BUTTON_NEW = "f016"
BUTTON_OPEN = "f115"
BUTTON_SAVE = "f0c7"
BUTTON_PROP = "f0ad"
BUTTON_REFR = "f021"
BUTTON_CLOSE = "f00d"
BUTTON_QUIT = "f08b"
BUTTON_CUT = "f0c4"
BUTTON_COPY = "f0c5"
BUTTON_PASTE = "f0ea"
BUTTON_ADD = "f067"
BUTTON_GROUP = "f090"
BUTTON_UNGR = "f08b"
BUTTON_DEL = "f1f8"
BUTTON_UNDO = "f0e2"
BUTTON_REDO = "f01e"
BUTTON_VIEW = "f06e"
BUTTON_START = "f04b"
BUTTON_START_FROM_SELECTED_STATE = "f074"
BUTTON_PAUSE = "f04c"
BUTTON_STOP = "f04d"
BUTTON_STEPM = "f050"
BUTTON_STEP = "f051"
BUTTON_BACKW = "f048"
BUTTON_ABOUT = "f0a3"
BUTTON_LEFTA = "f0d9"
BUTTON_RIGHTA = "f0da"
BUTTON_UPA = "f0d8"
BUTTON_DOWNA = "f0d7"

SIGN_LIB = "f02d"
SIGN_ARROW = "f047"

ICON_SOURCE = "f121"
ICON_DLINK = "f0c1"
ICON_LLINK = "f1e0"
ICON_OVERV = "f160"
ICON_DESC = "f036"

ICON_TREE = "f0e8"
ICON_GLOB = "f0ac"
ICON_HIST = "f254"
ICON_EHIST = "f1b3"
ICON_NET = "f0ec"

ICON_STICKY = "f08d"

# MAXIMUM_MESSAGE_LENGTH = 460    # in characters
CHECKSUM_LENGTH = 39
ACK_INDICATOR_LENGTH = 1
FLAG_LENGTH = 3
HEADER_LENGTH = CHECKSUM_LENGTH + ACK_INDICATOR_LENGTH + FLAG_LENGTH

BROWSER_SIZE_MULTIPLIER = 10

import random
import string
import time
import datetime
import os
ts = time.time()
datetime_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d%H_%M_%S')

GLOBAL_STORAGE_BASE_PATH = "/tmp/rafcon_"+\
                           os.environ.get('USER', 'anonymous')+"_"+\
                           str(datetime_ts)+"_"+\
                           ''.join(random.choice(string.ascii_uppercase) for x in range(10))