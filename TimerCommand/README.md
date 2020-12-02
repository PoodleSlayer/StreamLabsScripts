# Timer Command

This script can be used for creating timers in chat. Instead of a countdown on-screen, this will simply message the streamer when the time is up. Useful for things like "wear a hat for 5 minutes" or other such timed activities on stream. To avoid spam this is currently only allowed to be used by mods and editors, with the default permission level being mods.

## Command Usage

This command is set up a bit like a command line tool to give it more flexibility. By default the command name is `!timers` so I will be using that for these examples.

### Adding a new timer

To create a new timer, add the flag `add` or `-a` after the `!timers` command, followed by a name and a duration. The format for the time duration is `XXhYYmZZs` for hours, minutes, and seconds respectively. An example of both ways to add a new timer would be:
```
!timers add stretch 1h10m30s
!timers -a stretch 1h10m30s
```
The above example creates a new timer named 'stretch' that will end in 1 hour, 10 minutes, and 30 seconds. Note that each chunk of time in the format is _optional_, so you can simply specify what you need. For example:
```
!timers add hat 5m
!timers -a hat 5m
```
Here, both commands add a timer called 'hat' that lasts 5 minutes so we only need to specify the time we care about.

### Updating an existing timer

To add time to an existing timer use the `update` or `-u` flag, followed by the name of the timer to update and duration of time to add to the timer. If the timer does not exist, the bot will respond with a message indicating so.
```
!timers update hat 30s
!timers -u hat 30s
```
This will add 30 seconds to a timer named 'hat' if it exists.

### Deleting an existing timer

To delete a timer use the `delete` or `-d` flag, followed by the name of the timer to delete. If the timer does not exist, the bot will let you know.
```
!timers delete hat
!timers -d hat
```

### Clearing all timers

If you wish to delete all timers you can use the `clear` or `-c` flags. No other parameters are needed.
```
!timers clear
!timers -c
```

### Listing all active timers

To view the current running timers, use the `list` or `-l` flags. No other parameters are needed.
```
!timers list
!timers -l
```

## User Settings

This script supports a variety of user settings via the StreamLabs Chatbot Script UI:

- **Command Name** - the name of the command to be used in chat. Defaults to `!timers` (**Note:** StreamLabs chatbot already has a `!timer` command so don't name them the same!).
- **Add Message** - message to be displayed when a timer has been added. Supports the `$timer` variable to show the name of the timer created.
- **Update Message** - message to be displayed when a timer has been updated. Supports the `$timer` variable to show the name of the timer updated.
- **Delete Message** - message to be displayed when  timer has been deleted. Supports the `$timer` variable to show the name of the timer deleted.
- **Clear Message** - message to be displayed when all timers are cleared.
- **Error Message** - message to be displayed when the command is used incorrectly.
- **Invalid Message** - message to be displayed when the add or update commands are given an invalid time format.
- **Exists Message** - message to be displayed when a user tries adding a timer that already exists. Supports the `$timer` variable to show the name of the timer.
- **Not Found Message** - message to be displayed when a user tried to update or delete a timer that does not exist. Supports the `$timer` variable to show the name of the timer.
- **Timer List** - text to be displayed at the start of the timer list. Defaults to `Active timers: `
- **Timer Message** - message to be displayed when a timer finishes. Supports the `$name` variable for the streamer's name and `$timer` variable for name of the timer that finished. 
- **Use Cooldown** - whether or not to use a global cooldown. Defaults to `false`.
- **Cooldown** - global cooldown to use, in seconds.
- **Cooldown Message** - message to be displayed when the command is used while still on cooldown. Supports the `$cd` variable for remaining cooldown duration in seconds.
- **Permission** - which user levels can use this command. Defaults to `Moderator`, and currently only supports `Moderator` and `Editor` to help avoid spam.
