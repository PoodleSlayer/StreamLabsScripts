import json
import os
import codecs
# always want at least those three imports for reading the settings json files ^

# StreamLabs metadata, will be displayed in the StreamLabs chatbot's Scripts tab
ScriptName = "Template Script"
Website = "https://github.com/poodleslayer"
Description = "Template Script for anyone wanting to learn StreamLabs chatbot scripting"
Creator = "PoodleSlayer"
Version = "0.0.1"

settings = {}
commandName = ""

def Init():
    # this is called when the user reloads the Scripts tab.
    # use this as the starting point/setup for everything your script might need
    global settings, commandName
    work_dir = os.path.dirname(__file__)
    try:
        # try to open the config.json file specified in UI_Config.json
        with codecs.open(os.path.join(work_dir, "config.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    except:
        # if the config.json file failed to load for any reason, manually create some default settings
        settings = {
            "commandName" : "!test",
            "responseMessage" : "Command was used by $user",
            "cooldown" : 15,
            "permission" : "Everyone"
            }
    commandName = settings["commandName"]
    return

def Execute(data):
    # this gets called every time a message is sent in chat.
    # to make a "command", just check to see if the first word of the message is the command name.
    # check that the user has permission to use the command and that they aren't on cooldown.
    if data.IsChatMessage() and (data.GetParam(0).lower() == commandName) and Parent.HasPermission(data.User, settings["permission"], "") and not Parent.IsOnUserCooldown(ScriptName, commandName, data.User):
        # get some useful info about the user
        username = data.UserName
        points = Parent.GetPoints(data.User)  # note that this uses User, NOT UserName
        currency = Parent.GetCurrencyName()   # useful for response messages sometimes
        
        # I like to do the bulk of the logic in a separate function if possible. this helps
        # keep things more modular and makes debugging easier since you can call the function
        # directly without going through StreamLabs chatbot
        DoStuff()
        
        # load the response message from your user settings
        responseMessage = settings["responseMessage"]
        # replace any parameters. in this case we only have the $user parameter
        responseMessage = responseMessage.replace("$user", data.UserName)
        # finally, send the message to chat via the chatbot
        send_message(responseMessage)

        # add the user cooldown. you can also do Global Cooldowns if needed
        Parent.AddUserCooldown(ScriptName, commandName, data.User, settings["cooldown"])
        # if you want to use a currency cost, you can handle that like this
        #cost = 10
        #Parent.RemovePoints(data.User, username, cost)
    return

def DoStuff():
    # function to handle all the logic separate from the Execute function above. not necessary, but 
    # nice to organize stuff sometimes. also nice for debugging purposes!
    log("stuff has happened!")
    return

def Tick():
    # this gets called constantly as the chatbot runs. use this for keeping track of things
    # that change over time. think of this like the Update event in a game loop.
    return

def ReloadSettings(jsonData):
    # this gets called when the user hits Save Settings in the Scripts settings UI.
    # I've noticed this sometimes doesn't actually run, so it's safer to just reload
    # all scripts if needed. This is nice when it works though!
    return

def Unload():
    # this gets called when the chatbot is closed, so do any cleanup stuff here
    # such as possibly saving some data to a file.
    return

def send_message(message):
    # helper function to route strings through to the chatbot's output. useful for
    # debugging so you can swap between chatbot output and standard output
    Parent.SendStreamMessage(message)
    #print message #this is for debugging
    return

def log(message):
    # helper function to handle logging things. again, this is useful for debugging
    # so you can swap between logging to the chatbot or standard output
    Parent.Log(ScriptName, message)
    #print message
    return

# if you are running this script manually, uncomment the function calls below
# to simulate running from StreamLabs without the lifecycle events. Just be careful
# since all of the StreamLabs variables won't be available!
#Init()
#DoStuff()
