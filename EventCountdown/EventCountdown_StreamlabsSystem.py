import datetime
import json
import os
import codecs

# StreamLabs info
ScriptName = "Event Countdown"
Website = "https://github.com/poodleslayer"
Description = "Counts down days to the next occurence of the specified date"
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
            "eventMonth" : 1,
            "eventDay" : 1,
            "countdownMessage" : "$days until $event",
            "eventName" : "something cool happens!",
            "eventMessage" : "TODAY IS THE DAY!!!",
            "commandName" : "!birthday",
            "cooldown" : 0,
            "permission" : "Everyone"
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

def countdown():
    # find difference between today and target date
    today = datetime.date.today()
    futureMonth = settings["eventMonth"]
    futureDay = settings["eventDay"]
    try:
        future = datetime.date(today.year, futureMonth, futureDay)
    except: 
        future = datetime.date.today()
        send_message("Invalid date! Please specify a valid date")
        return
    
    diff = future - today
    daysString = ""
    outputMessage = ""
    
    # if past the event date, assume it's next year
    if diff.days < 0:
        try:
            future = datetime.date(today.year+1, futureMonth, futureDay)
            diff = future - today
        except:
            send_message("Invalid date next year! Please specify a valide date")
            return
    
    # correct the output message grammar for day vs days
    if diff.days > 1:
        daysString = "days"
    else:
        daysString = "day"

    # if today is the event
    if diff.days == 0:
        outputMessage = settings["eventMessage"]
        send_message(outputMessage)
        return

    # create the output message from the user settings
    outputMessage = settings["countdownMessage"]
    daysString = str(diff.days) + " " + daysString
    outputMessage = outputMessage.replace("$days", daysString)
    outputMessage = outputMessage.replace("$event", settings["eventName"])
    send_message(outputMessage)
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    #print message #this is for debugging
    return

#Init()
#countdown()
