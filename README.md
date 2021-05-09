# Utsushi's charm

This repo contains code that will allow you to extract all of your charms in Monster Hunter Rise from recordings taking with the switch's "save clip" feature.

It's called Utsushi's charm because I thought it would be funny to make a complementary "Utsushi's Armor Search System", but ["this armor set searcher exists"](https://mhrise.wiki-db.com/sim/?hl=en). I might still try to port Athena's ASS for MHW to MHR, but for now this works for me.

# Usage

## Requirements
- A computer (Windows) 
  - Linux and Mac might work too
- A usb cable to connect your switch to transfer files
- **Google Tesseract** installed and in path
  - Version 3 and Version 4 are confirmed working
    - Version 4 works much better
  - [Installer here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe) [License (Apache 2.0)](https://github.com/tesseract-ocr/tesseract/blob/master/LICENSE)
    - Just run the installer, no extra packages needed
    - Other Versions available on the [UB-Mannheim Github](https://github.com/UB-Mannheim/tesseract/wiki) page
  - Should add itself to path, you might have to reboot.
    - Potential Locations:
      -  `C:\Users\<USERNAME>\AppData\Local\Tesseract-OCR` (Version 3)
      -  `C:\Program Files\Tesseract-OCR` (Version 4)
      -  `C:\Program Files (x86)\Tesseract-OCR` (Version 4, less likely)
- **Python 3** (in path)
  - I used 3.9, but most above 3 should word
  - [Here](https://www.python.org/downloads/)
  - Check the box to add to path
- This repository downloaded to your computer
  - Installing everything in the requirements.txt with `pip install -r requirements.txt`. You might have to use `pip3` instead of `pip`
- Some knowledge of how to type things in the terminal
- Being able to read
- The understanding that this might take you longer to setup than it would have taken you to enter the dozen charms you like.

### Adding something to the path (Windows)

1. Copy the path to the executable (Where the program was installed)
   - Don't put the executable file in the path, only where it is located
2. type `env` in the windows serch bar
   - Alternatively type `Edit environment variables for your account`
3. Press Enter
4. Click on `Environment Variables`
5. In `User Variables`, select `Path`
6. Click `Edit`
7. Click `New`
8. Paste the path you copied previously in the new spot.
9. Click `Ok/Apply` for every window you opened.
10. Restart every terminal/command line, or reboot to make sure you'll have access to the new commands

## Steps

0. Unequip all jewels. You will create "fake" charms otherwise.
   - Don't ask, this is way out of scope for something that takes you 30 seconds to do.
1. Record clips similar to the following of you going through your charms. Try placing the UI in front of something that is very "flat" in color and doesn't have NPCs walking in front. 
   - I can easily go through 2-3 pages of charms in 30 seconds. 
   - Use a stopwatch on your phone if you have trouble timing the 30 seconds. I saved a clip every ~25 seconds
   - Don't worry about passing over a charm multiple times. Duplicates will be removed at the end.

![Example Clip](./media/example_clip.gif)

2. Transfer the clips to your computer.
3. Put the files in the "inputs" directory in this repository.
   - It does not matter how many you have 
   - I haven't tried to see what would happen if there are clips that are not of the charm UI
3. Open a terminal/command line in the same directory as the "main.py" file.
4. type `python main.py` and press Enter. You might have to run `python3 main.py`
5. The first 2 steps of the program do no require any attention
   - They can take a while
6. The third step might ask for your input, depending on how well the image recognition works.
   - Follow the instructions on screen and correct any invalid skill names.
   - If a skill has to be corrected, a window with the skill should open, you might have to alt-tab to it, windows likes to hide it.
   - Sometimes tesseract is absolutely unable to read text, those charms will be logged in [`app.log`](app.log) and you can add them manually.
7. Congrats, you now have your charms under two different forms, 
   - `charms.json`: JSON (You probably don't care about that)
   - `charms.encoded.txt`: This is the one you want
8. Open the `charms.encoded.txt` file and copy the contents in the import box of 
    


# How does this work

Using a combination of coding and algorithms, the developer was able to make drones fly without them crashing into each other. 

In all seriousness, the work is done in a couple broad steps:
1. Masking and cropping the videos to keep only important sections
2. Using OpenCV, I use the charm window to find "new" charms being hovered over and keep only one image per charm
3. Using OpenCV once again, I apply filters to clean up the images, identify slots and skill levels and extract a smaller image that has the skill name
4. The skill name image is passed to Google Tesseract that struggles to identify what is written
5. Based on a list of corrections, simple spellchecking and potential user inputs, a charm is rebuilt

# Contribute

- If you ran everything and got new corrections in the [`skill_corrections.csv`](skill_corrections.csv) file, consider creating a pull request to add them for others.
- If you feel like contributing anything, go ahead and submit a pull request I'll be happy to take a look and decide if it's something worth adding. 

# TODOS: 
- Throw out Google Tesseract/Try newer version
  - Version 4 works great, this is going on the backburner for a while
  - Version 3 has trouble with quite a few words (Slugger, Recovery, Earplugs, Counterstrike, Maestro, etc)
  - I'm seriously considering going full monkey brain and having one "mask" per skill like I'm doing for the slots and skill levels.
  - The monkey brain approach would probably make it so this can be ran completely unattended, at the cost of some extra storage space.
  - Monkey brain results:
    - Monkey brain is less accurate, might need to train an image classifier/custom OCR 
    - Tesseract 4 works great
    - Need to do some "pixel poking" to make sure everything is lined up the same
- Solution for people that don't want to bother with the hassle
- Make the code not a mess
- Use the page number in the "Is the last frame the same" check. (Low priority, charms still seem to get detected on page swap)
- Docker image for deployment?
