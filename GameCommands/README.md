# GameCommand Script

This script allows you to (hopefully) let chat interact with the game or app you are using. Keyboard inputs are done via the DirectInput library in Windows using keyboard scan codes which allow the input to happen regardless of what you are currently physically doing with the keyboard. 

## IMPORTANT

Some games will detect automated keyboard inputs and consider this as a cheat or hack. **DO NOT** attempt to use this script with modern games with cheat detection or otherwise exploit automated inputs (like making macros). This is purely meant to be for fun with older games to do things like quickly enter a cheat code or provide some input to mess with the streamer. Be smart about what games you use this with!

Also, if using the delayed input setting, this script attempts to [disable the user's keyboard temporarily](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-blockinput) while the virtual keys are input. This is not ideal but is the only way I could think to get around games that require a slower input (probably based on engine update loop speeds). However, if I am reading Microsoft's documentation correctly, this seems relatively easy to recover from should anything go wrong. Ctrl+Alt+Del will still work so you can just kill the program, and if the script crashes while the input is blocked for some reason then the block should just be released. Regardless: **use at your own discretion!**

## Command Usage

In the included `command_list.json` file you can add commands you wish to use with this script. The example commands included are in the format of cheat codes for a game like GTA Vice City, where the corresponding input to the game is a single string of letters with no spaces. Currently this script supports letters, numbers, spaces, periods, and back-ticks (the thing next to the 1 key) for the virtual key inputs.

Using the example commands provided in the `command_list.json` file we see that a value of `cheat1` corresponds to the string `CHEATONE`. To use the chat command a user simply types:
```
!command cheat1
```
and the script will attempt to send the corresponding text keys `CHEATONE` to the game/app that currently has focus. The keys are **case-insenstive** for convenience, so even if you name the command `cHeAt1` in your `command_list.json` file, a user can just type `cheat1` to use it! Or `CHEAT1`, `CHeaT1` etc.

Feel free to completely modify the `command_list.json` file, just be sure to keep it in the format of:
```json
{
    "value1" : {
        "value" : "text1",
        "cost" : 10,
        "message" : "$user has used value1!"
    },
    "value2" : {
        "value" : "text2",
        "cost" : 100,
        "message" : "value2 was used by $user"
    }
}
```
and so on, where `value` is the series of keys that will be input to the game, `cost` is how many channel points it costs to use, and `message` is the message to show in chat. The message supports the `$user` variable for displaying the calling username as well as the `$currency` variable for showing the amount of points that were used.

## User Settings

This script supports a variety of User Settings via the StreamLabs script UI:

- **Command Name** - defaults to "!command". Allows you to specify a custom command to be used in chat.
- **Invalid Message** - message to display in chat if the user tries to use a command value that doesn't exist. Supports the `$user` variable where `$user` is the username of the person who used the command.
- **Universal Cost** - turn this checkbox ON to use the same cost for all commands, otherwise command costs are individual and must be set in the `command_list.json` file. Defaults to OFF.
- **Cost** - specify an amount of your StreamLabs stream currency to spend to use this command. This will be used as the cost if the `Universal Cost` checkbox is checked. Defaults to 0 for fun c: 
- **Cost Message** - message to display in chat if the user does not have enough points to use the command. Supports the `$user` and `$currency` variables where `$user` is the username and `$currency` is the custom name of your channel currency in StreamLabs.
- **Cooldown** - how long (in seconds) users must wait between successive uses of this command. Defaults to 30 seconds.
- **Cooldown Message** - message to display in chat if the user is still on a cooldown, showing the remaining cooldown duration in seconds. Supports the `$user` and `$cd` variables where `$user` is username and `$cd` is the remaining cooldown duration in seconds.
- **Permission** - who is allowed to use this command. Supports the basic StreamLabs role groups (Everyone, Regular, Subscriber, Moderator, Editor) and defaults to Everyone.

As well as a few Advanced Settings if you need the virtual key inputs to have various delays rather than being input instantly (I recommend keeping these times as small as you can):
- **Use Delays** - checkbox to enable or disable artificial delays in the inputs. When using this, **keyboard events are temporarily disabled by the script**. Ctrl+Alt+Del can still be used if anything goes horribly wrong, and I believe the way I am currently doing this is thread-safe so that if the script crashes then control will be returned to the user anyway. Defaults to OFF.
- **Buffer Delay** - amount of time to wait in seconds after the script has temporarily stopped reading physical keyboard inputs. Useful for games where key presses might be buffered and therefore interfering with the virtual inputs. Defaults to 0.1 seconds.
- **Hold Delay** - amount of time to wait in seconds before releasing a key press. This helps if your key presses are too quick to be captured and need to be slower to simulate a real keypress. Defaults to 0.05 seconds.
- **Press Delay** - amount of time to wait in seconds between each virtual key press. Can be helpful if input requires successive key presses of the same key. Defaults to 0.025 seconds.
- **Use FnKeys** - checkbox that enables treating numeric inputs between 1-9 as Function Keys instead. Currently uses a temporary solution which is why it is limited to F1-F9. **Be careful when using Function Keys** - only use them if you're 100% sure you want them! Requested by a friend to allow quick save/load in games.

## Why Two Script Files?

After a lot of debugging I learned that StreamLabs actually runs IronPython, which is really cool since that means .NET stuff is available but there are some limitations and bugs in IronPython to work around. As a result of this, the DirectInput magic happens in a separate `keys.py` script that runs as plain Python using your selected interpreter for StreamLabs. It is important that this `keys.py` script file stays **in the same folder** as the main `GameCommand_StreamlabsSystem.py` script.
