import os
from typing import Optional

auth_token: Optional[str] = None


def parse_auth_token(token_or_file: str) -> str:
    if os.path.exists(token_or_file):
        with open(token_or_file, "r") as f:
            return f.read().strip()
    else:  # Just a token
        return token_or_file


def set_token(token_or_file: str) -> None:
    global auth_token
    auth_token = parse_auth_token(token_or_file)


def get_token() -> Optional[str]:
    return auth_token
