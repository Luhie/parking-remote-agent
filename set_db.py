from dotevn import load_dotenv
import os

load_dotenv()
DB_CONFIGS = {
    'default': {
        'host': os.getenv("HOST_NAME"),
        'user': os.getenv("HOST_USER"),
        'password': os.getenv("HOST_PW"),
        'database': os.getenv("HOST_DB")
    }
}