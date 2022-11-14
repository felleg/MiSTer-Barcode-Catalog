# MiSTer-Barcode-Catalog

This project was inspired by this video: https://www.youtube.com/watch?v=zJPx2u2e5IM

You will find two programs in this repository:
- `scanner.py`: The program accepts barcode numbers (e.g. UPC, EAN) as an input, looks up the matching game, and launches an instruction to a MiSTer connected on the same network to launch that game.
- `catalog.py`: The program generates a pdf of games with their matching barcode, so the user can print it and put it in a binder for convenience.

# Dependencies

## Local machine
On your local machine (e.g. PC, Raspberry Pi, etc.), install dependencies by running:

```bash
sudo apt update && sudo apt install python3 python3-pip pandoc
sudo apt install texlive-latex-base texlive-latex-recommended texlive-fonts-recommended
pip3 install argparse python-barcode pandas pillow
```

## MiSTer
On your MiSTer, install these dependencies by running (through an SSH connection or directly on the MiSTer by pressing an F-key that I can't remember nor test right now):
```bash
# MiSTer Batch Control (mbc), allows to launch a game from the command line interface
curl -L -k "https://raw.githubusercontent.com/pocomane/MiSTer_misc/master/MiSTer_misc.sh" | bash -s update
```

Also, setup an SSH key on your MiSTer. Currently, `scanner.py` doesn't support connecting via password.
```bash
# On the MiSTer, make sure /root/.ssh has the right permissions
chmod 600 /root/.ssh

# On your computer, create an ssh key if you don't have one already
ssh-keygen -t rsa

# Copy your key to the MiSTer
ssh-copy-id root@<MISTER_IP_ADDRESS>
```

# Setup

You must write a csv file (e.g. my-games.csv) that will match UPC codes and game metadata. This csv file can be used by both `scanner.py` and `catalog.py`.
The format must match the following example:

```csv
CATEGORY,CORE,GAME_PATH,GAME_NAME,ARTWORK_PATH,BARCODE,METADATA
Data East,GENESIS,1 US - A-F/Atomic Runner (USA).md,,atomic-runner.jpg,013252014046,"1992, Run & Gun. Possibly my favorite game on Sega's Genesis."
Shmups,PSX,Einhander (USA).cue,,einhander.jpg,711719424321,"1998, made by famous RPG makers SquareSoft. Possibly my favorite ambiance in a shmup."
```

Here is how to use these fields:
- `CATEGORY`: (Optional) In which section of the catalog this game should appear. If left blank, will be categorized as "Unsorted".
- `CORE`: The MiSTer core that can launch this game. For the list of valid MiSTer cores, run this command on your MiSTer (requires the `mbc` dependency documented above): `mbc list_core`.
  - Note: For `mbc`, the `CORE` value is case-sensitive. Make sure to write it as it appears when you run `mbc list_core`.
- `GAME_PATH`: The path of the game under the `/media/fat/games/XXXX` folder matching the specified `CORE`. For example, if a row has `CORE=GENESIS`, and `GAME_PATH=sonic.md`, the program will reconstruct the full game path as `/media/fat/games/Genesis/sonic.md`.
  - Note: The capitalization of the folder doesn't have to match that of the core, as in the example provided here. This mapping is handled automatically by the program.
  - Note2: Watch out for game paths that contain commas. Make sure to put these paths between `""` quotes. E.g. `"ESWAT (USA, Europe).md"`
 - `GAME_NAME`: (Optional) The game name as it should appear in the catalog. If left blank, `catalog.py` will infer the game name from its `GAME_PATH`.
 - `ARTWORK_PATH`: The path to the image (whitin the `artwork` folder) that represents the game.
 - `BARCODE`: (Optional) A UPC or EAN string of numbers that will be read by a barcode scanner. If left blank, the program will generate a unique dummy barcode for your convenience.
 - `METADATA`: Any additional info or comment that should appear with the game in the catalog.
 
# Usage

## scanner.py
Launch the program by doing:
```bash
GAME_CSV_FILE=#Specify the name of your game csv file here
MISTER_IP_ADDRESS=#Specify the IP address of your MiSTer on the local network
python3 scanner.py $GAME_CSV_FILE $MISTER_IP_ADDRESS

>
```

The program will show a `>` symbol, and will await a barcode scan. Scan a barcode, and the program will look inside your csv for the matching game. It will connect to your MiSTer and run a connect to launch your specified game.

## catalog.py
Launch the program by doing:
```bash
GAME_CSV_FILE=#Specify the name of your game csv file here
OUTPUT_PDF_NAME=#(Optional)Specify the name of the output PDF to generate, e.g. "My-Catalog.pdf". If unspecified, will default to output.pdf
ARTWORK_FOLDER=#(Optional) The folder that contains the artwork for your games. Defaults to "artwork".
BARCODES=#(Optional) The folder that contains the output barcode images. Defaults to "barcodes".
python3 catalog.py $GAME_CSV_FILE --output_pdf $OUTPUT_PDF_NAME --artwork $ARTWORK_FOLDER --barcodes $BARCODES

Generated My-Catalog.pdf ! :)

# Another example of how I usually call the code
python3 catalog.py ../game-database/game-database.csv --artwork ../game-database/artwork/ --update-csv
```

