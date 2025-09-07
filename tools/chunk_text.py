

MAX_LEN = 4096

def chunk_text(text, max_len=MAX_LEN):
    for i in range(0, len(text), max_len):
        yield text[i:i + max_len]