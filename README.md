# DMXIS macro generator

## Description

Helper utilities to generate python macros for the Entech DMXIS USB DMX controller

http://www.enttec.com/index.php?main_menu=Products&pn=70570

## Whats the problem?

Enttech offers a powerful python API for creating macros for the DMX controller. This works really well with small amount of fixtures, but gets problematic when fixture channels must be changed and when you're using hundreds of DMX channel.

In my scenario I'm using the DMX unit to control digital LED pixel tubes along with reqular DMX fixtures - one LED pixel has R,G and B channel and each tube has 16 pixels -> one LED tube requires 48 DMX channels. ...And I'm using  up to 30 tubes (3 rows of 10 tubes each). Each row of tubes use close to 500 DMX channels. These scripts might be useful if you're trying to do something similar.

### What I'm trying to resolve:

- When you have multiple banks (one for each song) there is now way to edit similar presets in different banks at the same time. You have to manually go trough every bank to do modifications to each. I have over 20 banks so this would be very painful.
- If you ever change the fixture configurations (add lights etc) and the DMX channels change -> all of your presets are unusable and require manual tweaking to bring them back.
- If you do any changes to you fixture/channel setup, you might break your macros and have to rewrite them.
- In order to control a lot of LED pixels, a lot of macros are needed. If you end up having to update macros, it'll be a lot of work
- Building complicated animations using the DMXIS oscillator would be a real pain manually.

### Solututions

1) Have one generic preset bank where you edit all presets, then use some of those presets in each songs (bascially copy them to other banks when needed)
 -> Now write a script which copies the settings from the generic bank to ALL banks if there is a preset with a same name in it. For example if you edit a preset named "Blue wash, red accents" in the generic bank, the script will then copy the changes to any bank which has this preset. This way there is only one bank you have to edits. This script is located at /scripts/updateallbanks.py


2) Because the high number of DMX channels in use (400 - 500 channels for the LED pixel tubes), even the powerful macros are a pain to work with. To get around these limitations, following steps are made:
  - Instead of generating a 'LED tube' fixture and assigning them manually in the DMXIS show editor, have a macro configuration file which which holds the fixture parameters as variables (tube count, pixel count, starting DMX channel etc). If the fixture setup changes, only one minor change is needed.
  - Have a separate util macro file which has the tools for every macro. Easy to update the macro behavior in one place.
  - Instead of manually creating and upating the macro files, have a property file where you can add/modify new colours, andimations etc (basically these are new presets) as a simple python dictionary which has the RGB, oscillator setting and channel settings

### Examples

```sh
# Walks trough all files in your 'generic preset' bank, and checks if the preset is used in any other bank. If yes, the generic version will be copied to this bank.
/scripts/updateallbanks.py
```

```sh
# This reads the FX table in /Macros/TubeControl/imports folder and
# creates / updates all macro python files dynamically. These macros
# Can then be used to build presets in the preset manager.
/scripts/createdmxispresets.py
```

### folders structure

the FX tables are under:
/Macros/TubeControl/imports

The scripts are under
/scripts
