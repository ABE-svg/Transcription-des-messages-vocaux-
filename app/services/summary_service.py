from transformers import pipeline
import spacy
import pytextrank

# Version 1 : résumé génératif avec Transformers (BART)
# Cette version utilise un modèle pré-entraîné assez lourd, qui reformule le texte
# pour produire un résumé plus naturel. Les résultats sont en général meilleurs,
# mais le chargement du modèle prend du temps et nécessite plus de ressources.
# Utile si on veut un résumé “propre” et fluide.


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    if len(text.split()) < 30:
        return text  # Pas pertinent de résumer un texte très court (à décider avec l'équipe)

    summary = summarizer(
        text,
        max_length=100,
        min_length=30,
        do_sample=False
    )

    return summary[0]["summary_text"]


# Version 2 : résumé extractif avec spaCy + PyTextRank
# Cette approche est plus légère : elle sélectionne les phrases les plus importantes
# du texte sans vraiment réécrire le contenu. Ça fonctionne vite, ça ne demande pas
# de modèle lourd, mais le résultat ressemble plus à une liste de phrases clés.
# Pratique pour comparer une méthode simple avec une méthode plus avancée.

# (à installer avec : python -m spacy download fr_core_news_md, voir comment rajouter cette commande directement lors de la création du venv)
""" nlp = spacy.load("fr_core_news_md")
nlp.add_pipe("textrank")

def summarize_text(text: str) -> str:
    if len(text.strip()) == 0:
        return ""
    doc = nlp(text)
    key_sentences = []
    for sent in doc._.textrank.summary(limit_phrases=10, limit_sentences=3):
        key_sentences.append(str(sent))

    if not key_sentences:
        return text

    return " ".join(key_sentences)
    """