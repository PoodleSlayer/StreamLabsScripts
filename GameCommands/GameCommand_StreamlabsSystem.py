import json
import os
import codecs
import ctypes
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.Modules.dll")
#import subprocess
from System.Diagnostics import Process

# StreamLabs info
ScriptName = "Game Commands"
Website = "https://github.com/poodleslayer"
Description = "Attempts to input keys to the current application being used."
Creator = "PoodleSlayer"
Version = "1.0.1"

settings = {}
commandList = {}
commandName = ""
pythonPath = ""
scriptPath = ""

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
            "cost" : 0,
            "cooldown" : 30,
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
    pythonPath = os.path.join(os.__file__.split("Lib\\")[0], "python.exe")
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    scriptPath = os.path.join(scriptPath, "keys.py")
    return

def Execute(data):
    if Parent.IsOnUserCooldown(ScriptName, commandName, data.User):
        send_message("HOL' UP")
    if data.IsChatMessage() and (data.GetParam(0) == commandName) and Parent.HasPermission(data.User, settings["permission"], "") and not Parent.IsOnUserCooldown(ScriptName, commandName, data.User):
        chatMessage = ""
        commandToUse = ""
        userId = data.User
        username = data.UserName
        #points = Parent.GetPoints(userId)
        points = 10

        try:
            commandToUse = str(data.GetParam(1))
            #log(data.User + " used the command: " + data.Message)
        except Exception, e:
            chatMessage = "Please specify a valid command"
            send_message(chatMessage)
            return
        
        ### TODO - get costs and stuff working correctly
        #if settings["cost"] > points:
        #    chatMessage = "Not enough points!"
        #    send_message(chatMessage)
        #    log("not enough currency")
        #    return
        #if (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
        #    chatMessage = "Still on cooldown!"
        #    send_message(chatMessage)
        #    log("command on cooldown")
        #    return
        #log("attempting to send inputs...")
        #Parent.RemovePoints(userId, username, settings["cost"])
        Parent.AddUserCooldown(ScriptName, commandName, data.User, settings["cooldown"])
        chatMessage = username + " has used command " + commandToUse + "!"
        # useful for debugging
        #time.sleep(10)

        #log("Python is located at: " + pythonPath + " and script is " + scriptPath)
        #log("running external process...")
        p = Process()
        p.StartInfo.FileName = pythonPath
        # oh my gosh why does the chatbot folder have a space in it
        p.StartInfo.Arguments = "\"" + scriptPath + "\"" + " " + commandList[commandToUse]
        p.StartInfo.UseShellExecute = False
        p.StartInfo.CreateNoWindow = True
        p.Start()
        #log("process started: " + p.StartInfo.FileName + p.StartInfo.Arguments)
        p.WaitForExit()
        #log("process exited with " + str(p.ExitCode))

        send_message(chatMessage)
    return

def Tick():
    return

def sendGameCommand():
    # used for debugging since the Execute event isn't called
    time.sleep(5)
    # need way to call python without IronPython like in StreamLabs context :c
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    #print message #this is for debugging
    return

def log(message):
    Parent.Log(ScriptName, message)
    #print message
    return

### debugging
#Init()
#sendGameCommand()
