import datetime
import json
import os
import codecs

# StreamLabs info
ScriptName = "Better Uptime"
Website = "https://github.com/poodleslayer"
Description = "Better uptime command that supports time since offline"
Creator = "PoodleSlayer"
Version = "1.0.0"

settings = {}
commandName = ""

def Init():
    global settings, commandName
    work_dir = os.path.dirname(__file__)
    try:
        with codecs.open(os.path.join(work_dir, "config.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    except:
        settings = {
            "offlineMessage" : "Streamer was last seen $time ago",
            "onlineMessage" : "Streamer has been live for $time!",
            "commandName" : "!uptime",
            "cooldown" : 0,
            "permission" : "Everyone"
            }
    commandName = settings["commandName"]
    # maybe check some online API first here? as the "source of truth"
    # for the last uptime/stream time
    return

def Execute(data):
    if data.IsChatMessage() and (data.GetParam(0).lower() == commandName) and Parent.HasPermission(data.User, settings["permission"], "") and not Parent.IsOnUserCooldown(ScriptName, commandName, data.User):
        uptime()
        Parent.AddUserCooldown(ScriptName, commandName, data.User, settings["cooldown"])
    return

def Tick():
    return

def uptime():
    # 
    send_message(outputMessage)
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    #print message #this is for debugging
    return

#Init()
#uptime()
