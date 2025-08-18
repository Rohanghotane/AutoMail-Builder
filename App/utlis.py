import re

def clean_text(text):

    text = re.sub(r'<[^>]*?>', '', text)

    text = re.sub(r'https[s]?://(?:[a-zA-Z]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F]))+', '', text)

    text = re.sub(r'[^a-zA0-9]', '', text)

    text = re.sub(r'\s{2,}', '', text)

    text = text.strip()

    text = ' '.join(text.strip())

    return text
