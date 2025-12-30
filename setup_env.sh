set -e

#use only  Python 3.11 (mac,windowd)
if command -v python3.11 &>/dev/null; then
    PYTHON=python3.11
elif command -v py &>/dev/null && py -3.11 --version &>/dev/null; then
    PYTHON="py -3.11"
else
    echo "Python 3.11 not found. Install Python 3.11 and retry."
    exit 1
fi

echo "Using Python: $PYTHON"

#create virtual environmen tin which we store libraries
$PYTHON -m venv .venv

#activate venv mac or windows 
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

#install libraries 
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt
#make sure for pytest that bot package can be imported , the path will be TGBOT/
python -m pip install -e .

pytest || {
  echo "Tests failed"
  deactivate
  exit 1
}

echo "Environment ready."
echo "Activate with:"
echo "source .venv/Scripts/activate    # Windows Git Bash"
echo "source .venv/bin/activate        # Linux / Mac / WSL"
echo "py -3.11 -m bot.main       # run tg bot "