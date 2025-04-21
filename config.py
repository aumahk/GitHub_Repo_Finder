import os
from dotenv import load_dotenv

load_dotenv()

def get_github_token():
    # Local token if available (for developer only)
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token

    # Prompt user for token
    import tkinter.simpledialog as simpledialog
    return simpledialog.askstring("GitHub Token", "Enter your GitHub Personal Access Token:")
