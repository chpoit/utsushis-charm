[![Github All Releases](https://img.shields.io/github/downloads/chpoit/utsushis-charm/total.svg)]() [![Github All Releases](https://img.shields.io/github/downloads/chpoit/utsushis-charm/latest/total.svg)]()

# Utsushi's Charm

> Whenever I look at Utsushi I feel like I can do anything. Unfortunately, when I need to register my charms, I can't lose myself in Utsushi's charm.
> Fortunately, now, with Utsushi's charm, I can lose myself in Utsushi's charm for longer.
>
> \- Utsushi Fan Girl, probably


This repo contains code that will allow you to extract all of your charms in Monster Hunter Rise from recordings taking with the switch's "save clip" feature.

It's called Utsushi's charm because I thought it would be funny to make a complementary "Utsushi's Armor Search System", but ["this armor set searcher exists"](https://mhrise.wiki-db.com/sim/?hl=en). I might still try to port Athena's ASS for MHW to MHR, but for now this works for me.

# Usage

## Requirements
- A computer (Windows)
  - Linux and Mac might work too, you wont be able to run the EXE and will have to run from source in a terminal window. Refer to [Running from source](#Running-from-source)
- A USB cable to connect your switch to transfer files
- [The latest version of this](https://github.com/chpoit/utsushis-charm/releases/latest) downloaded to your computer (Utsushis-Charm_**vx_x**.zip)
  - A [pre-release](https://github.com/chpoit/utsushis-charm/releases/tag/v1.5.0-alpha) with a User Interface is available
- Some knowledge of how to type things in the terminal
- Being able to read

## Steps

0. Unequip all jewels. You will create "fake" charms otherwise.
   - Item Box -> Manage Equipment -> Set Decorations -> Equipment Box -> Remove all (Press '-' on controller)
   - Don't ask, this is way out of scope for something that takes you 30 seconds to do.
1. Download the release bundle and follow the Requirements section  (Utsushis-Charm_**vx_x**.zip)
   - You're free to delete `skill_corrections.csv` if you want. A new empty one will be recreated.
2. Record clips similar to the following of you going through your charms. Try placing the UI in front of something that is very "flat" in color and doesn't have NPCs walking in front.
   - I can easily go through 2-3 pages of charms in 30 seconds.
   - Use a stopwatch on your phone if you have trouble timing the 30 seconds. I saved a clip every ~25 seconds.
   - Don't worry about passing over a charm multiple times. Duplicates will be removed at the end.

![Example Clip](./media/example_clip.gif)

3. Transfer the clips to your computer.
4. Put the files in the "inputs" directory. If it does not exist, create it at the same place you can find `utsushis-charm.exe`.
   - It does not matter how many you have
   - I haven't tried to see what would happen if there are clips that are not of the charm UI
5. Run the `utsushis-charm.exe` (Double-click)
6. A Terminal should pop up
   - Wait a little bit, it need to do extract some data (~5-15s)
7. The first step of the program should take roughly 30 seconds to 1 minute per clip you have in the inputs folder
8. Once that step is done, the second phase starts, normally, it should be done without needing your attention
   - Follow the instructions on screen and correct any invalid skill names.
   - If a skill has to be corrected, a window with the skill should open, you might have to alt-tab to it, Windows likes to hide it.
9. The program is done running. Press Enter and exit.
   - You might see some warnings about memory leaks, you don't have to worry about that, it's cleared upon closing the program.
10. Extra:
    - Sometimes tesseract is absolutely unable to read text, those charms will be logged in `app.log` and you can add them manually.
    - You can see a list of duplicate charms (if they exist) in the `charms.duplicate.txt`
    - If no charm errored, or you don't care about those charms, you should be able to open the `charms.encoded.txt` file and copy the contents into the import box of [MHR-Wiki](https://mhrise.wiki-db.com/sim/?hl=en)


# FAQ
- Q: Can I use a capture card instead?
  - I tested recording in 720p and 1080p with OBS using a Genki Shadowcast and everything worked. (MKV, others should work too)
  - I recommend recording in 30fps to avoid doubling the frames to process
    - 60 fps is fine, half of the frames are skipped.
  - I see no reason other capture cards should not work
  - 1080p adds extra processing due to a downscaling step to 720p (20-30% slower)
  - I also tested using an Mclassic without any issues.

# Troubleshooting

If the program starts and closes without anything happening, open the `app.log` file and use this section to try and fix your issues

## Simple issues:
- 0 charms found
  - Make sure your clips are in the inputs folder
- I had to enter skill by hand but it wont accept it
  - You need to enter them one word at a time, it might only not know what one of the words is.
  - Make sure you are writing it exactly how it is shown on the picture that pops up
- I get through the First phase, but it stops when checking the first frame of
  - This is an issue with Tesseract not being installed. Check the next bullet point.
- Google Tesseract is not installed/not found
  - This should not happen in version 1.4 and above. 
  - Make sure you installed it. You might have to reboot
  - Try adding it manually to the path
    - Potential Locations:
      -  `C:\Program Files\Tesseract-OCR` (Most likely, if you chose "Install for anyone")
      -  `C:\Users\<USERNAME>\AppData\Local\Tesseract-OCR` (If you chose "Install only for me")
      -  `C:\Program Files (x86)\Tesseract-OCR` (Version 4, less likely, would happen if you manually downloaded a 32bit installer)
  -  It seems really random wether it'll add it to path. If there is a request for it, I might add a "bruteforce" method to find the exe so people don't have to worry about this.
- Any other issue:
  - Consider creating a bug report [here](https://github.com/chpoit/utsushis-charm/issues/new)

## Adding something to the path (Windows)

1. Copy the path to the executable (Where the program was installed)
   - Don't put the executable file in the path, only where it is located
2. type `env` in the Windows search bar
   - Alternatively type `Edit environment variables for your account`
3. Press Enter
4. Click on `Environment Variables`
5. In `User Variables`, select `Path`
6. Click `Edit`
7. Click `New`
8. Paste the path you copied previously in the new spot.
9. Click `Ok/Apply` for every window you opened.
10. Restart every terminal/command line, or reboot to make sure you'll have access to the new commands


# How does this work

Using a combination of coding and algorithms, the developer was able to make drones fly without them crashing into each other.

In all seriousness, the work is done in a few broad steps:
1. Take all the videos and apply a filter and crop them to a smaller resolution to keep only the important data, keeping around one frame per charm
2. Out of those frames, get the slots, skills and skill levels
3. Feed the Skills to Google Tesseract to extract the names
   - If it is not a known skill, try using known corrections to get the proper skill
   - If needed, ask the user for input on what the skill is
4. Output the final list of charms

# Contribute

- If you ran everything and got new corrections in the [`skill_corrections.csv`](skill_corrections.csv) file, consider creating a pull request to add them for others.
- If you feel like contributing anything, go ahead and submit a pull request I'll be happy to take a look and decide if it's something worth adding.

# TODOS:
- [ ] Throw out Google Tesseract/Try newer version
  - Version 4 works great, this is going on the back burner for a while
  - Version 3 has trouble with quite a few words (Slugger, Recovery, Earplugs, Counterstrike, Maestro, etc.)
  - I'm considering going full monkey brain and having one "mask" per skill like I'm doing for the slots and skill levels.
  - The monkey brain approach would probably make it so this can be run completely unattended, at the cost of some extra storage space.
  - Monkey brain results:
    - Monkey brain is less accurate
    - Tesseract 4 works great
    - Need to do some "pixel poking" to make sure everything is lined up the same
- [ ] Solution for people that don't want to bother with the hassle
- [ ] Make the code not a mess
- [ ] Use the page number in the "Is the last frame the same" check. (Low priority, charms still seem to get detected on page swap)
- [ ] Docker image for deployment?
- [ ] UI
- [ ] ~~Multithreading for some of that SPEEEEED~~
  - Unfortunately, the joblib 'loky' backend wont work with frozen executables, and the other backends offer no noticeable gain in performance. This is getting shelved until a potential rewrite under a "faster" rewrite. Current execution time is 4-8 minutes so it's really not too bad.

# Building the executable
- Requirements:
  - 7zip in path
  - A virtual env called "env" in this project (I used the `virtualenv` module)
  - Have all the contents of `requirements.txt` installed in said env
- Make sure you are not "currently" in the env (otherwise files do weird things)
- Run the `scripts\build_release.bat` file.

Sometimes windows will lock some files for a while and there is nothing you can do about it other than wait.

# Running from source
Common requirements:
- Python3 installed and in path
- Set up a virtual environment (optional)
- Install pip packages (in virtualenv if you use it.)

Normal instructions apply once the application starts.

## MacOS
- Requirements:
  - have python3 and tesseract installed via brew (or some other way)
  - Virtual env on mac (optional):  `virtualenv -p python3 env`
- Running:
  - switch to the virtualenv `source env/bin/activate` (run at the root of the repository)
  - set TESSDATA_PREFIX: `export TESSDATA_PREFIX=/usr/local/Cellar/tesseract/<version>/share/tessdata`
  - install the project dependencies: `pip3 install .`
  - run with `python3 main.py`

## Linux
- Requirements
  - You will need to install Google tesseract with your package manager of choice.
- Running
  - `python3 main.py`
  - 

## Windows
- Requirements
  - **Google Tesseract** installed and in path
    - A copy of the version 4 is bundled with the release. Just run it, no extra packages needed
      - You can download the installer here version here: [Installer here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe)
    - Make sure it's in path
  - Python3 installed and in path
- Running:
  - `source env/bin/activate` (if you use a virtual env)

# Extra command line options
If you run from source, or call the executable from the terminal you can make use of the following flags/arguments to achieve different functionality

- `-h` or ` --help`: Shows arguments
- `--thirdparty `: Shows 3rd party licenses
- `--skip-frames`: Skips the first frame extraction step. Useful if the second step crashed.
- ` --skip-charms`:`Skips the Tesseract-OCR step. Not sure why you would want that.
- `-i <INPUT_DIR>` or `--input <INPUT_DIR>`: Changes the Input directory for videos
- `-f <FRAME_DIR>` or `--frames <FRAME_DIR>`: Changes the Directory used to store temporary frames
- `-c <FILE_NAME>` or `--charm-json <FILE_NAME>`: Changes the name of the json formatted charms
- `-e <FILE_NAME>` or `--charm-encoded <FILE_NAME>`: Changes the name of the MHR-Wiki formatted charms
