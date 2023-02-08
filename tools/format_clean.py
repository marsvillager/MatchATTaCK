import re


def replace_dots(text):
    try:
        ind = text.index('.')
        while ind < len(text) - 1:
            if not text[ind + 1:ind + 2] == ' ' and not text[ind +
                                                             1:ind + 2] == '"' and not text[ind + 1:ind + 2] == '\'':
                text = text[:ind] + '_' + text[ind + 1:]
            try:
                ind = ind + 1 + text[ind + 1:].index('.')
            except BaseException:
                break
        return text
    except BaseException:
        return text


def remove_urls(text):
    text = re.sub(r'\[?\S+\]?\(?https?://\S+\)?', '', text)
    return text


def remove_citations(text):
    text = re.sub(r'\(Citations?: \S+\)', '', text)
    return text


def remove_chars(text):
    to_remove = "This technique has been deprecated. Please see ATT&CK's Initial Access and Execution tactics for " \
                "replacement techniques. "
    text = text.replace(to_remove, '')
    text = re.sub('<[^>]*>', '', text.lower()).strip()
    text = re.sub(r'[^a-zA-Z\'\_]', ' ', text.lower())
    return text


def clean_text(text):
    clean = remove_citations(text)
    clean = remove_urls(clean)
    clean = replace_dots(clean)
    clean = remove_chars(clean)
    return clean
