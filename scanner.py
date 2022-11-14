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
    "NEOGEO": "/media/fat/games/NEOGEO/",
    "ARCADE": "/media/fat/_Arcade/",
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
      barcode = input("> ")
      game_db = pd.read_csv(GAME_DB_FILENAME, dtype=str)
      found = game_db.loc[game_db.BARCODE == barcode]
      if len(found) == 1:
        load_game(found.reset_index(drop=True))
      elif len(found) == 0:
        print("No matching game for", barcode)
      elif len(found) >1 :
        print("Error: Multiple games have the same barcode:",
            found)
      else:
        print("This is an uncaught error. Here is what I found when I searched for your barcode:", found)

def load_game(game):
    MISTER_USER="root"
    path = os.path.join(GAMES_PATH[game.CORE[0]],
      game.GAME_PATH[0].replace(" ", "\\ ").replace("(","\(").replace(")","\)"))
    cmd_core = "!direct" if game.CORE[0].upper() == "ARCADE" else game.CORE[0]
    cmd=f"/media/fat/Scripts/.barcoderattler/mbc load_rom {game.CORE[0]} {path}"
    sh_cmd=f"ssh {MISTER_USER}@{MISTER_IP_ADDRESS} '{cmd}'"
    #print(sh_cmd)
    # Launch the game over SSH
    subprocess.Popen(sh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
