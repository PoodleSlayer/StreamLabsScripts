import sys
import time
import ctypes

# DirectInput scan codes
# reference: https://gist.github.com/tracend/912308
DIKeys = {
    'W' : 0x11,
    'A' : 0x1E,
    'S' : 0x1F,
    'D' : 0x20,
    'Q' : 0x10,
    'E' : 0x12,
    'R' : 0x13,
    'T' : 0x14,
    'Y' : 0x15,
    'U' : 0x16,
    'I' : 0x17,
    'O' : 0x18,
    'P' : 0x19,
    'F' : 0x21,
    'G' : 0x22,
    'H' : 0x23,
    'J' : 0x24,
    'K' : 0x25,
    'L' : 0x26,
    'Z' : 0x2C,
    'X' : 0x2D,
    'C' : 0x2E,
    'V' : 0x2F,
    'B' : 0x30,
    'N' : 0x31,
    'M' : 0x32,
    ' ' : 0x39,
    '`' : 0x29,
    '0' : 0x0B,
    '1' : 0x02,
    '2' : 0x03,
    '3' : 0x04,
    '4' : 0x05,
    '5' : 0x06,
    '6' : 0x07,
    '7' : 0x08,
    '8' : 0x09,
    '9' : 0x0A,
    '.' : 0x34
}

DIK_ENTER = 0x1C

def InputCommands(inputString):
    type_keys(inputString)

def type_keys(inputString):
    # this seems scary to block input from user, but the docs say if this thread crashes it should return control anyway.
    # this does NOT block ctrl+alt+del so users can still safely kill this if needed
    noKeys = ctypes.windll.user32.BlockInput(True)
    ReleaseAllKeys()
    time.sleep(0.1)
    for c in inputString.upper():
        if c in DIKeys:
            PressKey(DIKeys[c])
            time.sleep(0.025)
            ReleaseKey(DIKeys[c])
            time.sleep(0.01)
    time.sleep(0.1)
    ReleaseAllKeys()
    noKeys = ctypes.windll.user32.BlockInput(False)

# helper method to hopefully prevent buffered keyboard presses from interfering with automated input
def ReleaseAllKeys():
    for c in DIKeys:
        ReleaseKey(DIKeys[c])

# C struct redefinitions
# as per SerpentAI
# https://github.com/SerpentAI/SerpentAI/blob/dev/serpent/input_controllers/native_win32_input_controller.py
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

#InputCommands(sys.argv[1])
InputCommands(' '.join(sys.argv[1:]))
#ReleaseAllKeys()
### debugging
#InputCommands("player.additem f 100")
