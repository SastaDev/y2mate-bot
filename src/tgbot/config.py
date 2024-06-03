import os

class Config:
    API_ID = int(os.environ.get("API_ID", None))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    OWNER_ID = int(os.environ.get("OWNER_ID", None))