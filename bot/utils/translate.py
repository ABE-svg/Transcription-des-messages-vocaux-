

import os
from openai import AsyncOpenAI

from dotenv import load_dotenv
LANG_NAME_TO_CODE = {
    "english": "en",
    "french": "fr",
    "german": "de",
    "spanish": "es",
    "italian": "it",
    "russian": "ru",
    
}

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def translator(message: str, target_lang: str) -> str:
    """
    Asynchronously translate `message` into `target_lang`.
    target_lang may be as in LANG_NAME_TO_CODE
    """

    prompt = (
        f"ONLY Translate the following text into {target_lang}. "
        f"Return ONLY the translated text, nothing else:\n\n{message} "
    )

    response = await client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()

