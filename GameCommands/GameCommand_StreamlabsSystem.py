import json
import os
import codecs
import ctypes
import time

# StreamLabs info
ScriptName = "Game Commands"
Website = "https://github.com/poodleslayer"
Description = "Attempts to input keys to the current application being used."
Creator = "PoodleSlayer"
Version = "1.0.0"

settings = {}
commandList = {}
commandName = ""

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
}

def Init():
    SendInput = ctypes.windll.user32.SendInput
    
    global settings, commandName, commandList
    work_dir = os.path.dirname(__file__)

    # load UI settings
    try:
        with codecs.open(os.path.join(work_dir, "config.json"), encoding='utf-8-sig') as json_file1:
            settings = json.load(json_file1, encoding='utf-8-sig')
    except:
        settings = {
            "commandName" : "!command",
            "cooldown" : 0,
            "permission" : "Everyone"
            }

    # load commands
    try:
        with codecs.open(os.path.join(work_dir, "command_list.json"), encoding='utf-8-sig') as json_file2:
            commandList = json.load(json_file2, encoding='utf-8-sig')
    except:
        print str(e)
        commandList = {
            "cheat1" : "CHEATONE"
            }
    
    commandName = settings["commandName"]
    return

def Execute(data):
    if data.IsChatMessage() and (data.GetParam(0).lower() == commandName) and Parent.HasPermission(data.User, settings["permission"], "") and not Parent.IsOnUserCooldown(ScriptName, commandName, data.User):
        countdown()
        Parent.AddUserCooldown(ScriptName, commandName, data.User, settings["cooldown"])
    return

def Tick():
    return

def sendGameCommand():
    # send key inputs to active window
    type_keys(commandList["cheat3"])
    return

def type_keys(inputString):
    for c in inputString.upper():
        if c in DIKeys:
            PressKey(DIKeys[c])
            ReleaseKey(DIKeys[c])

def send_message(message):
    #Parent.SendStreamMessage(message)
    print message #this is for debugging
    return

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

Init()
sendGameCommand()
