set -e

# Détection de python en fonction de l'OS
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
elif command -v py &>/dev/null; then
    PYTHON="py -3"
else
    echo "Aucun interpréteur Python trouvé."
    exit 1
fi

$PYTHON -m venv .venv

source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install -r requirements.txt


echo "Environnement prêt. Pour l'activer exécute : source .venv/Scripts/activate"
