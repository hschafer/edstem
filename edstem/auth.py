import os

AUTH_TOKEN = None

def auth_token(token_or_file: str) -> str:
    if os.path.exists(token_or_file):
        with open(token_or_file) as f:
            return f.read().strip()
    else:  # Just a token
        return token_or_file


def set_token(token_or_file: str) -> None:
    AUTH_TOKEN = auth_token(token_or_file)
    # Check valid token?