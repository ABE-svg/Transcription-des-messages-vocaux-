set -e

# Vérification obligatoire de Python 3.11 (tous OS)

if command -v python3.11 >/dev/null 2>&1; then
    PYTHON=python3.11
elif command -v py >/dev/null 2>&1 && py -3.11 --version >/dev/null 2>&1; then
    PYTHON="py -3.11"
else
    echo "Erreur : Python 3.11 est requis."
    echo "Veuillez installer Python 3.11 puis relancer le script."
    exit 1
fi

echo "Python utilisé : $PYTHON"

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

echo "tous les tests sont excecutés "
echo "Environnement prêt. Pour l'activer exécutez : "
echo "Vous ne pourrez par lancer le bot, car il est déjà lancé sur VPS  "
echo "source .venv/Scripts/activate    # Windows Git Bash"
echo "source .venv/bin/activate        # Linux / Mac / WSL"

