import json
import os
import codecs

# StreamLabs info
ScriptName = "Custom Shoutouts"
Website = "https://github.com/poodleslayer"
Description = "Customize Shoutouts for different people!"
Creator = "PoodleSlayer"
Version = "1.1.0"

settings = {}
shouts = {}
commandName = ""

Settings_CommandName = "commandName"
Settings_DefaultMessage = "defaultMessage"
Settings_TargetMessage = "targetMessage"
Settings_UseCooldown = "useCooldown"
Settings_Cooldown = "cooldown"
Settings_CooldownMessage = "cooldownMessage"
Settings_Permission = "permission"

def Init():
    global settings, shouts, commandName
    work_dir = os.path.dirname(__file__)
    # load the user settings
    try:
        with codecs.open(os.path.join(work_dir, "config.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    except:
        settings = {
            "commandName" : "!shout",
            "defaultMessage" : "Everyone go check out $name over at their channel! $channel",
            "targetMessage" : "Please specify a target for the command!",
            "useCooldown" : False,
            "cooldown" : 5,
            "cooldownMessage" : "Please wait $cd more seconds to use this command!",
            "permission" : "Moderator"
            }
    # load the custom shoutouts
    try:
        with codecs.open(os.path.join(work_dir, "shouts.json"), encoding='utf-8-sig') as json_file:
            shouts = json.load(json_file, encoding='utf-8-sig')
    except:
        shouts = {
            "PoodleSlayer" : "Don't check me out please D:",
            "AdamCYounis" : "Go watch some incredible GAME DEV and PIXEL ART over at https://www.twitch.tv/adamcyounis"
            }
    # convert shoutout dict keys to lower case for case-insensitive matching
    shouts =  {k.lower(): v for k, v in shouts.items()}
    commandName = settings[Settings_CommandName]
    return

def Execute(data):
    if data.IsChatMessage() and (data.GetParam(0).lower() == commandName) and Parent.HasPermission(data.User, settings["permission"], ""):
        if settings[Settings_Cooldown] and (Parent.IsOnUserCooldown(ScriptName, commandName, data.User) or Parent.IsOnCooldown(ScriptName, commandName)):
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, commandName)
            if cooldownDuration < 1:
                cooldownDuration = 1
            cooldownMessage = settings[Settings_CooldownMessage]
            cooldownMessage = cooldownMessage.replace("$cd", str(cooldownDuration))
            send_message(cooldownMessage)
            return

        paramCount = data.GetParamCount()
        if paramCount < 2:
            #log("not enough parameters!")
            send_message(settings[Settings_TargetMessage])
            return

        targetUser = data.GetParam(1)
        # in case the calling user used @username instead of just username
        targetUser = targetUser.replace("@", "")
        targetUserLower = targetUser.lower()
        responseMessage = ""

        if targetUserLower in shouts:
            responseMessage = shouts[targetUserLower]
        else:
            responseMessage = settings[Settings_DefaultMessage]
        responseMessage = responseMessage.replace("$name", targetUser)
        responseMessage = responseMessage.replace("$channel", "https://www.twitch.tv/" + targetUser)

        send_message(responseMessage)
        if settings[Settings_UseCooldown]:
            Parent.AddCooldown(ScriptName, commandName, settings[Settings_Cooldown])
    return

def Tick():
    return

def ReloadSettings(jsonData):
    # called when the user saves the settings in the Scripts tab
    Init()
    return

def Unload():
    # this gets called when the chatbot is closed
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
