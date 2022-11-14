#!/usr/bin/env python3
"""
Launch a MisTER FPGA game from a barcode
"""

__author__ = "Felix Leger"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import sys
import pandas as pd
import subprocess

# The game folder name doesn't have always the same capitalization as
# the Core name, so we create this mapping here to avoid having to
# rewrite the path to the game folder in the game database over and over
GAMES_PATH = {
    "GENESIS": "/media/fat/games/Genesis/",
    "NES": "/media/fat/games/NES/",
    "PSX": "/media/fat/games/PSX/",
    "TGFX16": "/media/fat/games/TGFX16/",
    "TGFX16-CD": "/media/fat/games/TGFX16-CD/",
    "NEOGEO": "/media/fat/games/NEOGEO/",
    "ARCADE": "/media/fat/_Arcade/",
    "SMS": "/media/fat/games/SMS/Master\ System/",
    "SMS.GG": "/media/fat/games/SMS/Game\ Gear/",
    "SNES": "/media/fat/games/SNES/",
    "GAMEBOY": "/media/fat/games/GAMEBOY/",
    "GAMEBOY.COL": "/media/fat/games/GAMEBOY/",
    }
MISTER_IP_ADDRESS=sys.argv[2]

def main():
    """ Main loop
    Reads keyboard input (possibly the keyboard is a barcode scanner).
    When the 'enter' key is read, the keys pressed previously (which we
    assume to be the barcode) will be used to launch the game.

    Launching the game will be done by running an SSH connection to the
    MiSTer FPGA.

    Before attempting the SSH connection, we first validate the barcode
    is present in our game database file.

    We do not attempt to pass a password in the SSH connection, we want
    to use SSH keys (for simplicity)."""

    GAME_DB_FILENAME = sys.argv[1]
    while True:
      try:
        barcode = input("> ")
        game_db = pd.read_csv(GAME_DB_FILENAME, dtype=str)
        found = game_db.loc[game_db.BARCODE == barcode]
        if len(found) == 1:
          print(os.path.splitext(os.path.basename(found.GAME_PATH.values[0]))[0])
          load_game(found.reset_index(drop=True))
        elif len(found) == 0:
          # Try once more to find a match, but removing leading zeroes
          # I noticed that my csv edit program very stupidly removes leading
          # zeroes every time I open my csv file. This ensures I don't have to
          # fix missing leading 0 errors.
          found = game_db.loc[game_db.BARCODE == barcode[1:]]
          if len(found) == 1:
            print(os.path.splitext(os.path.basename(found.GAME_PATH.values[0]))[0])
            load_game(found.reset_index(drop=True))

          else:
            print("No matching game for", barcode)
        elif len(found) >1 :
          print("Error: Multiple games have the same barcode:",
              found)
        else:
          print("This is an uncaught error. Here is what I found when I searched for your barcode:", found)
      except Exception as e:
        print("Did you map a directory for this console?")
        print(e)

def load_game(game):
    MISTER_USER="root"
    path = os.path.join(GAMES_PATH[game.CORE[0]],
      game.GAME_PATH[0].replace(" ", "\\ ").replace("(","\(").replace(")","\)"))
    cmd_core = "!direct" if game.CORE[0].upper() == "ARCADE" else game.CORE[0]
    cmd=f"/media/fat/Scripts/.barcoderattler/mbc load_rom {game.CORE[0]} {path}"
    #print("@@@", cmd)
    sh_cmd=f"ssh {MISTER_USER}@{MISTER_IP_ADDRESS} '{cmd}'"
    #print(sh_cmd)
    # Launch the game over SSH
    subprocess.Popen(sh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
