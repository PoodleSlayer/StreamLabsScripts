import json
import os
import codecs
import time
import math
import re

# StreamLabs metadata, will be displayed in the StreamLabs chatbot's Scripts tab
ScriptName = "Chat Timers"
Website = "https://github.com/poodleslayer"
Description = "Script for creating timers in chat."
Creator = "PoodleSlayer"
Version = "1.0.0"

settings = {}
commandName = ""
timers = {}

Settings_CommandName = "commandName"
Settings_AddMessage = "addMessage"
Settings_UpdateMessage = "updateMessage"
Settings_DeleteMessage = "deleteMessage"
Settings_ClearMessage = "clearMessage"
Settings_ErrorMessage = "errorMessage"
Settings_InvalidMessage = "invalidMessage"
Settings_ExistsMessage = "existsMessage"
Settings_NotFoundMessage = "notFoundMessage"
Settings_TimerList = "timerList"
Settings_TimerMessage = "timerMessage"
Settings_UseCooldown = "useCooldown"
Settings_Cooldown = "cooldown"
Settings_CooldownMessage = "cooldownMessage"
Settings_Permission = "permission"

def Init():
    global settings, commandName
    work_dir = os.path.dirname(__file__)
    try:
        with codecs.open(os.path.join(work_dir, "config.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    except:
        settings = {
            "commandName" : "!timers",
            "addMessage" : "timer \'$timer\' successfully added!",
            "updateMessage" : "timer \'$timer\' successfully updated!",
            "deleteMessage" : "timer \'$timer\' successfully removed!",
            "clearMessage" : "all timers have been deleted!",
            "errorMessage" : "incorrect usage - please try again",
            "invalidMessage" : "invalid time format! please specify time as XXhYYmZZs",
            "existsMessage" : "timer \'$timer\' already exists!",
            "notFoundMessage" : "timer \'$timer\' not found",
            "timerList" : "Active timers: ",
            "timerMessage" : "$name the timer for \'$timer\' has ended!",
            "useCooldown" : False,
            "cooldown" : 5,
            "cooldownMessage" : "Please wait $cd seconds before modifying the timers!",
            "permission" : "Moderator"
            }
    commandName = settings["commandName"]
    return

def Execute(data):
    if data.IsChatMessage() and (data.GetParam(0).lower() == commandName) and Parent.HasPermission(data.User, settings["permission"], ""):
        # check cooldowns first
        if settings[Settings_Cooldown] and (Parent.IsOnUserCooldown(ScriptName, commandName, data.User) or Parent.IsOnCooldown(ScriptName, commandName)):
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, commandName)
            if cooldownDuration < 1:
                cooldownDuration = 1
            responseMessage = settings[Settings_CooldownMessage]
            responseMessage = responseMessage.replace("$cd", str(cooldownDuration))
            send_message(responseMessage)
            return

        username = data.UserName
        points = Parent.GetPoints(data.User)
        currency = Parent.GetCurrencyName()
        responseMessage = ""
        
        flag = data.GetParam(1)
        # add time in format 1h2m3s
        # add new timer
        if flag == "add" or flag == "-a":
            addTimer(data.GetParam(2), data.GetParam(3))

        # update existing timer
        elif flag == "update" or flag == "-u":
            updateTimer(data.GetParam(2), data.GetParam(3))

        # delete existing timer
        elif flag == "delete" or flag == "-d":
            removeTimer(data.GetParam(2))
        
        elif flag == "clear" or flag == "-c":
            clearTimers()
        
        # list timers
        elif flag == "list" or flag == "-l":
            listTimers()

        else:
            responseMessage = settings[Settings_ErrorMessage]
            send_message(responseMessage)

        if settings[Settings_UseCooldown]:
            Parent.AddCooldown(ScriptName, commandName, settings["cooldown"])
    return

def addTimer(timerName, timeToAdd):
    global timers
    responseMessage = ""

    if validateTime(timeToAdd) is False:
        send_message(settings[Settings_InvalidMessage])
        return

    endTime = time.time() + convertTime(timeToAdd)

    if timerName not in timers:
        timers[timerName] = endTime
        responseMessage = settings[Settings_AddMessage]
        responseMessage = responseMessage.replace("$timer", timerName)
        send_message(responseMessage)
    else:
        responseMessage = settings[Settings_ExistsMessage]
        responseMessage = responseMessage.replace("$timer", timerName)
        send_message(responseMessage)

    return

def updateTimer(timerName, timeToAdd):
    global timers
    responseMessage = ""

    if validateTime(timeToAdd) is False:
        send_message(settings[Settings_InvalidMessage])
        return

    if timerName not in timers:
        responseMessage = settings[Settings_NotFoundMessage]
        responseMessage = responseMessage.replace("$timer", timerName)
        send_message(responseMessage)
    else:
        timers[timerName] = timers[timerName] + convertTime(timeToAdd)
        responseMessage = settings[Settings_UpdateMessage]
        responseMessage = responseMessage.replace("$timer", timerName)
        send_message(responseMessage)

    return

def removeTimer(timerName):
    global timers
    responseMessage = ""
    if timerName not in timers:
        responseMessage = settings[Settings_NotFoundMessage]
        responseMessage = responseMessage.replace("$timer", timerName)
        send_message(responseMessage)
    else:
        timers.pop(timerName, None)
        responseMessage = settings[Settings_DeleteMessage]
        responseMessage = responseMessage.replace("$timer", timerName)
        send_message(responseMessage)
    return

def clearTimers():
    global timers
    for timer in timers.keys():
        timers.pop(timer, None)
    send_message(settings[Settings_ClearMessage])
    return

def listTimers():
    global timers
    timerList = settings[Settings_TimerList]
    i = 0
    if len(timers) == 0:
        timerList += "none"
    for timer in timers:
        timerList += timer + " - " + convertText((int)(timers[timer] - time.time()))
        if i < len(timers) - 1:
            timerList += ", "
        i += 1
    send_message(timerList)
    return

def validateTime(timeToCheck):
    # regex to see if the time is in the format XXhYYmZZs
    pattern = r'^([0-9]+[h]{1})?([0-9]+[m]{1})?([0-9]+[s]{1})?$'
    #log(timeToCheck + " matches: " + str(re.match(pattern, timeToCheck) is not None))
    return (re.match(pattern, timeToCheck) is not None)

def convertTime(timeToAdd):
    hours = 0
    tempTime = timeToAdd.split('h')
    if len(tempTime) == 2:
        hours = tempTime[0]
        timeToAdd = tempTime[1]
    minutes = 0
    tempTime = timeToAdd.split('m')
    if len(tempTime) == 2:
        minutes = tempTime[0]
        timeToAdd = tempTime[1]
    seconds = 0
    tempTime = timeToAdd.split('s')
    if len(tempTime) == 2:
        seconds = tempTime[0]
    #log("hours: " + str(hours) + ", minutes: " + str(minutes) + ", seconds: " + str(seconds))
    return int(hours)*60*60 + int(minutes)*60 + int(seconds)

def convertText(timeToText):
    hours = math.floor(timeToText/3600)
    timeToText = timeToText % 3600
    minutes = math.floor(timeToText/60)
    timeToText = timeToText % 60
    seconds = timeToText
    timeString = ""
    if hours != 0:
        timeString += str(int(hours)) + "h"
    if minutes != 0:
        timeString += str(int(minutes)) + "m"
    if seconds != 0:
        timeString += str(int(seconds)) + "s"
    return timeString

def Tick():
    global timers
    currentTime = time.time()
    # update all timers
    # if any timers expire, message the streamer
    for timer in timers.keys():
        if timers[timer] < currentTime:
            timers.pop(timer, None)
            responseMessage = settings[Settings_TimerMessage]
            responseMessage = responseMessage.replace("$name", Parent.GetChannelName())
            responseMessage = responseMessage.replace("$timer", timer)
            send_message(responseMessage)
    
    return

def ReloadSettings(jsonData):
    return

def Unload():
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    #print message #this is for debugging
    return

def log(message):
    Parent.Log(ScriptName, message)
    #print message
    return

# debugging
#Init()
#addTimer("one", "0h2m30s")
#addTimer("two", "10m")
#listTimers()
#updateTimer("two", "5m")
#updateTimer("three", "1m30s")
#removeTimer("four")
#clearTimers()
#print validateTime("1h30m5s")
