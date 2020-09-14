# Template Script

This script serves as a template for others who would like to make some custom scripts for the StreamLabs chatbot. Further documentation [can be found here](https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate/wiki/Data-Object), such as available variables and functions for use in your scripts. Note the right-hand navigation menu! It's easy to miss, haha.

## Naming Conventions

StreamLabs chatbot scripts must be named in the format of `X_StreamlabsSystem.py`, where `X` is some descriptive name for your script. The important part is it **must end** with `_StreamlabsSystem.py` to be executed as a script.

Also included is an example `UI_Config.json` file. This file **must be named** this way to be picked up by StreamLabs chatbot for the Settings UI. Within the `UI_Config.json` file is the first property `output_file` - this can be set to any value but it **must match** the settings file name you attempt to read in your script's `Init` function. In this template, the `output_file` is just `config.json`.

## Further Resources

This script attempts to be fairly self-documenting, but these links will help you out a lot!

- [Official Ankhbot/StreamLabs Chatbot Documentation](https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate/wiki)
- [Helpful Medium article that I stumbled upon while first messing around with this stuff](https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate/wiki/Creating-UI-Config-File)
