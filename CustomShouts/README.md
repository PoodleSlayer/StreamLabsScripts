# Custom Shoutouts Script

Simple little script that lets you create custom shoutouts for people with a default fallback response message. There are already ways to accomplish this in StreamLabs with the use of the `readline` command and creating a separate file for each custom shoutout, but this script will let you organize everything all in one place and avoids reading a bunch of files. The other solutions I have seen also require sending two messages, since the message in the file does not get interpreted and can't use any parameters.

## Command Usage

After importing the above files to StreamLabs chatbot, open the `shouts.json` file in your [preferred text editor](https://code.visualstudio.com/). This file is structured as a simple json file in the format:
```json
{
    "username1" : "cool custom shoutout for username1",
    "username2" : "A Very Different Yet Also Cool shoutout for username2, who you can check out at their channel: $channel",
    "PoodleSlayer" : "\"Fancy\" shoutout with a url - I don't stream but if I did it would be at https://www.twitch.tv/PoodleSlayer"
}
```

etc. etc. etc.! Note that the parameters `$user` and `$channel` are both supported here to display the username and channel name if so desired.

Because this is json, special characters (such as the double quotes in the last example above) [must be escaped](https://www.freeformatter.com/json-escape.html). After you have set up all the different username-shoutout combinations you want, simply save the file and reload your scripts in StreamLabs chatbot. Now you can call the command in chat as such:
```
!shout PoodleSlayer
```

To simplify things, all usernames are converted to lower case before comparison - this allows the command to be case-insensitive. The script will also remove any `@` symbols in case the calling user uses the target's `@username` instead of just `username`.

## User Settings

This script supports a few settings via the StreamLabs Scripts tab:

- **Command Name** - the name of this command as it will be used in chat. Defaults to `!shout`
- **Default Message** - default shoutout message for any usernames not covered by custom shoutouts. Supports the `$user` and `$channel` parameters for displaying the target username and channel name, respectively.
- **Global Cooldown** - global cooldown (in seconds) to be applied to this command. The cooldown is **global** meaning it is independent of whoever uses the command. Defaults to 5 seconds.
- **Permission Level** - the required permission level to use this command. Defaults to `Moderator` to avoid chat spam and also to only let trusted users shout people out c:

## Possible Future Features

This was a quick little script for a friend but I would like to expand on it after getting some feedback from people. One thing this doesn't support that I would like to add is a parameter for displaying whatever the user was last streaming. I know StreamLabs has a parameter for this but I don't think I can use those parameters in my own messages from the script... There is also probably some other fun info I could get with the Twitch API!

Also I realize this script is basically a glorified key/value pairing, but it solves a common problem. I'm sure there are other uses for a dynamic command with different responses for different parameter values, so I'll try to think of some way to make this more useful.
