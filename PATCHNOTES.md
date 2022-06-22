# Patch Notes (Updated June 22nd 2022)
- 1.6
  - Added an app language dropdown
  - Version Checker automatically updates language files
    - Other updates (main app, skills and corrections) are still "on demand" when there is an update 
  - App and game language are now stored inside a config file
  - Added a --reset cmd option to clear the config file
  - Languages in language dropdowns should show up in the actual language
    - NOTE: They are probably wrong
  - Added a "Go to Set Searcher" button


# Older patch notes

- 1.5.3 (FEB 3rd 2022)
  - Updated where language packs are downloaded from, 
    - Github changed where "raw" data was fetched from and broke "fresh" installs 
  - Updated the bundle tesseract to be version 5
    - Shouldn't really change anything
  - General update to bundled corrections and others
    - For some reason the PC version of the game has the `Quick Sheath` skill as `Quick Sheathe`, added a correction to map it
- 1.5.2
  - Adds update checking
    - Allows for independent skills/auto-corrections/localization updates
  - Adds initial support for localization (only through command line flags however (`-a` or `--app-language`))
- 1.5.1
  - Resolves issues with local directory creation found in #20
- 1.5
  - Now with a User Interface
  - Support for [Multiple Game languages](#supported-game-language)