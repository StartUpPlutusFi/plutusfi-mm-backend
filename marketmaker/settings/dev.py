import os
import sys



import environ

from .base import *

env = environ.Env()

env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env.bool("DEBUB", True)

JWT_SIG_KEY = env("JWT_SIG_KEY")

DATABASES = {"default": env.db()}

print("$$$$$$$$$$$$", DATABASES)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

if "test" in sys.argv:
    DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
