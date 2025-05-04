import os
from dotenv import load_dotenv

def load_token_from_env():
    load_dotenv()
    return os.getenv("GITHUB_TOKEN", "")
