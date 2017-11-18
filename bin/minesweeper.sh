BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MINESWEEPER_DIR=$(dirname $BIN_DIR)

python $MINESWEEPER_DIR/minesweeper/main.py
