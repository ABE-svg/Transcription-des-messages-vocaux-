
# Transcription de messages vocaux

---
- ABE Kevin                 .(https://github.com/ABE-svg)
- ALUCH Yasmine             .(https://github.com/Yasmxne)
- AYRAPETYAN Artur          .(https://github.com/aayrapet)
- GHORAFI Manal             .(https://github.com/Manalghorafi)
- MAKAMWE Pierrette Josiane .(https://github.com/josiepierr)
---

## Objectif
Ce projet a pour objectif de **convertir un message vocal en texte** avec **résumé automatique** et **traduction**.  
Il vise à faciliter l’analyse et la synthèse de conversations, réunions ou messages vocaux grâce à une interface API simple et efficace.

---

## Technologies utilisées
- **Flask** — Framework web pour créer l’API REST  
- **OpenAI Whisper API** / **SpeechRecognition** — Transcription vocale (speech-to-text)  
- **Transformer (BART via Hugging Face)** — Résumé automatique du texte  
- **Pytest** — Tests unitaires  
- **Docker** — Conteneurisation et déploiement reproductible
- `Python-telegram-bot` package 

---

## Architecture du projet

La structure arborescente du projet est la suivante :

```plaintext

                Transcription-des-messages-vocaux-/
                ├─ app/
                │  ├─ __init__.py
                │  ├─ api.py                 
                │  │
                │  ├─ docs/                       
                │  │  └─ swagger.yaml
                │  │
                │  ├─ services/                  
                │  │  ├─summary_service.py
                │  │  └─ transcribe_service.py   
                │  │
                │  ├─ static/ 
                │  │  └─ style.css
                │  │
                │  ├─ templates/ 
                │  │  ├─ base.html
                │  │  └─ index.html
                │  │
                │  └─ utils/                     
                │     └─ audio_utils.py
                │
                ├─ bot/
                │  ├─ __init__.py
                │  ├─ main.py                 
                │  │
                │  │
                │  └─ utils/
                │     ├─__init__.py 
                │     ├─translate.py                    
                │     └─ transcribe.py
                │
                ├─ tests/
                │  ├─ test_api.py
                │  ├─ test_bot.py  
                │  ├─ test_summary.py              
                │  └─ test_transcription.py
                │
                ├─ Fichiers audios/
                ├─ .dockerignore
                ├─ .gitignore
                ├─ LICENSE
                ├─ README.md
                ├─ docker-compose.yml     
                ├─ dockerfile   
                ├─ requirements.txt
                ├─ pyproject.toml
                └─ setup_env.sh
```

---
## Résultats

### Chatbot Telegram
On accède au Chatbot Telegram via le lien: https://t.me/VoiceToMessage_Bot
Ce Chatbot prend en entrée des messages vocaux  et retourne la version transcrite, avec option de traduction automatique dans la langue par défaut de l'appareil utilisé (Si l'audio est en français, anglais, allemand,espagnol,italien, russe). Cette transcription est sensible à l'accent de l'utilisateur. 
Note: Ces spécificités sont intrinsèquement liées à la version de Whisper API utilisée. 

Exemple de rendu sur Telegram:

 ### Application Web

## Prérequis

### Option 1 — Exécution locale
- Python **3.11** installé
- Git Bash (Windows)

### Option 2 — Exécution via Docker
- Docker installé
- Docker Compose installé

---

## Lancement du projet

### 1️⃣ Option 1 — Exécution locale 

À la racine du projet, exécuter dans **Git Bash** :

```bash
bash ./setup_env.sh
```

### 2️⃣ Option 2 — Lancement avec Docker

```bash
git clone https://github.com/ABE-svg/Transcription-des-messages-vocaux-
cd Transcription-des-messages-vocaux-
docker compose up --build
```

Accès à l'interface web : http://localhost:5000

Accès à la documentation Swagger : http://localhost:5000/apidocs/

⚠️ Le premier build Docker ainsi que le chargement initial de l’interface peuvent prendre plusieurs minutes, notamment en raison du téléchargement des modèles de transcription.

Cette application prend en entrée tout type de fichier (audio, vidéo), détecte les messages audios et fait la transcription avec une option "summary", qui renvoit un résumé du message (400 mots maximum).
L'application présente différents niveaux de perfection selon la version de Whisper API utilisée: 
- tiny: Très rapide, précision limitée
- base: Bon compromis vitesse/précision
- small: Plus lent, meilleure précision (Nécessite un GPU)

Le dossier **Fichiers audios** contient des audios qui permettent à l'utilisateur de tester l'application.
 
## À propos du bot Telegram

Le bot **ne sera pas lancé localement** par ce projet.

- Une instance du bot est **déjà déployée et en cours d’exécution sur un VPS**.
- Le lancement local nécessite :
  - des clés API **payantes**
  - une configuration spécifique via **BotFather**
  - une infrastructure déjà préparée côté serveur sur Linux

Pour ces raisons, le démarrage automatique du bot Telegram est volontairement désactivé dans ce projet. Le code du bot est présent pour référence technique.

