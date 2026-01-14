import re

def clean_text(text: str) -> str:
    """
    Basic NLP preprocessing:
    - lowercase
    - remove URLs
    - remove special characters
    - remove extra spaces
    """
    if not text:
        return ""

    text = text.lower()

    # remove urls
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # keep only alphabets + numbers + spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text
