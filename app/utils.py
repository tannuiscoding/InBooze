import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def combine_threads(email_results):
    return "\n\n".join([f"From: {e['metadata']['sender']}\nSubject: {e['metadata']['subject']}\n\n{e['content']}" for e in email_results])
