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

# $PYTHON -m venv .venv

source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt


echo "Environnement prêt. Pour l'activer exécute : source .venv/Scripts/activate"
