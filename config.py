import os
from dotenv import load_dotenv

def load_token_from_env():
    load_dotenv()
    return os.getenv("GITHUB_TOKEN", "")
<<<<<<< HEAD
=======

>>>>>>> 67d32e25915453c87537ab1f1af2714db8b4588e
