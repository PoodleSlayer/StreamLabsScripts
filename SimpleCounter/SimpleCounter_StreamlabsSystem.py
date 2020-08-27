import datetime
import json
import os
import codecs

# StreamLabs info
ScriptName = "Simple Counter"
Website = "https://github.com/poodleslayer"
Description = "Counter to be used by chat"
Creator = "PoodleSlayer"
Version = "1.0.0"

settings = {}
commandName = ""
totalCount = 0

def Init():
    global settings, commandName
    work_dir = os.path.dirname(__file__)
    try:
        with codecs.open(os.path.join(work_dir, "config.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    except:
        settings = {
            "counterMessage" : "Puns told in chat: $count",
            "commandName" : "!count",
            "cooldown" : 15,
            "permission" : "Everyone"
            }
    commandName = settings["commandName"]
    global totalCount
    totalCount = 0
    log("totalCount is now " + str(totalCount))
    return

def Execute(data):
    if data.IsChatMessage() and (data.GetParam(0).lower() == commandName) and Parent.HasPermission(data.User, settings["permission"], "") and not Parent.IsOnCooldown(ScriptName, commandName):
        global totalCount
        totalCount += 1
        responseMessage = settings["counterMessage"].replace("$count", str(totalCount))
        send_message(responseMessage)
        Parent.AddCooldown(ScriptName, commandName, settings["cooldown"])
    return

def Tick():
    return

def ReloadSettings(jsonData):
    # when user saves settings, reload and save the new settings
    return

def Unload():
    # this gets called when the chatbot is closed, so maybe save the totalCount here?
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    #print message #this is for debugging
    return

def log(message):
    Parent.Log(ScriptName, message)
    #print message
    return

#Init()
#countdown()
