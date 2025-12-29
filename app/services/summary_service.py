from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

MAX_WORDS = 400  


def chunk_text(text, max_words=MAX_WORDS):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])


def summarize_text(text: str) -> str:
    if len(text.split()) < 30:
        return text

    summaries = []

    for chunk in chunk_text(text):
        summary = summarizer(
            chunk,
            max_length=120,
            min_length=40,
            do_sample=False
        )
        summaries.append(summary[0]["summary_text"])

    return " ".join(summaries)


