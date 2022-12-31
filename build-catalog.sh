set -e
python3 catalog.py ../game-database/game-database.csv --artwork ../game-database/artwork --update-csv

echo "Generated gamelist.pdf :)"
