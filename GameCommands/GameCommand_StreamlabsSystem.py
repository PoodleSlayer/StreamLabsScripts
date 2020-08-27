import json
import os
import codecs
import ctypes
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.Modules.dll")
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import SendKeys
from System import Type, Activator
from System.Diagnostics import Process

# this can help with running in Python vs IronPython
#import subprocess

# StreamLabs info
ScriptName = "Game Commands"
Website = "https://github.com/poodleslayer"
Description = "Attempts to input keys to the current application being used."
Creator = "PoodleSlayer"
Version = "1.2.4"

settings = {}
commandList = {}
commandName = ""
pythonPath = ""
scriptPath = ""

# hard-coding these string literals so I can't typo them c':
Settings_CommandName = "commandName"
Settings_InvalidMessage = "invalidMessage"
Settings_UniversalCost = "universalCost"
Settings_Cost = "cost"
Settings_CostMessage = "costMessage"
Settings_Cooldown = "cooldown"
Settings_CooldownMessage = "cooldownMessage"
Settings_Permission = "permission"

Replace_Username = "$user"
Replace_Cooldown = "$cd"
Replace_Currency = "$currency"
Replace_Cost = "$cost"

def Init():
    SendInput = ctypes.windll.user32.SendInput
    
    global settings, commandName, commandList, pythonPath, scriptPath
    work_dir = os.path.dirname(__file__)

    # load UI settings
    try:
        with codecs.open(os.path.join(work_dir, "config.json"), encoding='utf-8-sig') as json_file1:
            settings = json.load(json_file1, encoding='utf-8-sig')
    except:
        settings = {
            "commandName" : "!command",
            "invalidMessage" : "Invalid command value $user, please try again!",
            "universalCost" : False,
            "cost" : 0,
            "costMessage" : "$user does not have enough $currency",
            "cooldown" : 30,
            "cooldownMessage" : "$user still has $cd seconds until ready!",
            "permission" : "Everyone"
            }

    # load commands
    try:
        with codecs.open(os.path.join(work_dir, "command_list.json"), encoding='utf-8-sig') as json_file2:
            commandList = json.load(json_file2, encoding='utf-8-sig')
    except Exception, fe:
        print str(fe)
        log("Could not open command_list.json, " + str(fe))
        commandList = {
            "cheat1" : {
                "value" : "CHEATONE",
                "cost" : 10,
                "message" : "$user used cheat1!"
            }
        }
    
    commandName = settings[Settings_CommandName]
    pythonPath = os.path.join(os.__file__.split("Lib\\")[0], "python.exe")
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    scriptPath = os.path.join(scriptPath, "keys.py")
    return

def Execute(data):
    if data.IsChatMessage() and (data.GetParam(0) == commandName) and Parent.HasPermission(data.User, settings[Settings_Permission], ""):
        # initialize some things
        chatMessage = ""
        commandToUse = ""
        commandValue = ""
        commandMessage = ""
        userId = data.User
        username = data.UserName
        points = Parent.GetPoints(userId)
        #points = 100
        cost = 0
        currency = Parent.GetCurrencyName()

        # check for cooldown first
        if Parent.IsOnUserCooldown(ScriptName, commandName, data.User):
            cooldownDuration = Parent.GetUserCooldownDuration(ScriptName, commandName, userId)
            chatMessage = settings[Settings_CooldownMessage]
            chatMessage = chatMessage.replace(Replace_Username, username)
            chatMessage = chatMessage.replace(Replace_Cooldown, str(cooldownDuration))
            send_message(chatMessage)
            return

        # get the command parameter
        try:
            commandToUse = str(data.GetParam(1))
            #log(data.User + " used the command: " + data.Message)
        except Exception, e:
            chatMessage = settings[Settings_InvalidMessage]
            chatMessage = chatMessage.replace(Replace_Username, username)
            send_message(chatMessage)
            return
        
        # get the nested properties and check for errors in config
        try:
            commandValue = commandList[commandToUse]["value"]
            commandMessage = commandList[commandToUse]["message"]
        except KeyError, ke:
            chatMessage = commandToUse + " has not been set up correctly: " + str(ke.message)
            send_message(chatMessage)
            return

        # get the cost
        if settings[Settings_UniversalCost]:
            cost = settings[Settings_Cost]
            #log("using universal cost, cost is " + str(cost))
        else:
            cost = commandList[commandToUse]["cost"]
            #log("using individual cost, cost is " + str(cost))
        
        if cost > points:
            chatMessage = settings[Settings_CostMessage]
            chatMessage = chatMessage.replace(Replace_Username, username)
            chatMessage = chatMessage.replace(Replace_Currency, currency)
            send_message(chatMessage)
            #log("not enough currency")
            return
        
        #log("attempting to send inputs...")
        Parent.RemovePoints(userId, username, cost)
        Parent.AddUserCooldown(ScriptName, commandName, data.User, settings[Settings_Cooldown])
        chatMessage = commandList[commandToUse]["message"]
        chatMessage = chatMessage.replace(Replace_Username, username)
        chatMessage = chatMessage.replace(Replace_Cost, str(cost) + " " + currency)
        # useful for debugging
        #time.sleep(5)
        #sendGameCommandShell(commandList[commandToUse]["value"])
        #sendGameCommandMsgEv(commandList[commandToUse]["value"])
        # new version will support multiple input methods. for now just do DirectInput
        sendGameCommand(commandList[commandToUse]["value"])
        send_message(chatMessage)
    return

def Tick():
    return

# alternative method for inputting keys using Shell.SendKeys
def sendGameCommandShell(inputString):
    shell = Activator.CreateInstance(Type.GetTypeFromProgID("WScript.Shell"))
    shell.SendKeys(inputString)
    return

# alternative method for inputting keys using Windows Message Events
def sendGameCommandMsgEv(inputString):
    #SendKeys.Send(inputString)    # this will cause an error if the receiving application isn't set up to receive messages
    SendKeys.SendWait(inputString)
    return

# the default method for inputting keys. uses DirectInput and keyboard scan codes
def sendGameCommand(inputString):
    #log("Python is located at: " + pythonPath + " and script is " + scriptPath)
    #log("running external process...")
    p = Process()
    p.StartInfo.FileName = pythonPath
    # oh my gosh why does the chatbot folder have a space in it
    p.StartInfo.Arguments = "\"" + scriptPath + "\"" + " " + inputString
    p.StartInfo.UseShellExecute = False
    p.StartInfo.CreateNoWindow = True
    p.Start()
    #log("process started: " + p.StartInfo.FileName + p.StartInfo.Arguments)
    p.WaitForExit()
    #log("process exited with " + str(p.ExitCode))
    return

def debugStuff():
    log(commandList["cheat2"]["value"])
    log(commandList["cheat2"]["cost"])
    log(commandList["cheat2"]["message"].replace("$user", "PoodleSlayer"))

def send_message(message):
    Parent.SendStreamMessage(message)
    #print message #this is for debugging outside of the StreamLabs context
    return

def log(message):
    Parent.Log(ScriptName, message)
    #print message
    return

### debugging
#Init()
#sendGameCommand()
#debugStuff()
