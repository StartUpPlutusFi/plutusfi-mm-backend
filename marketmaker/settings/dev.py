import os
import environ

from .base import *

env = environ.Env()

env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env.bool("DEBUB", True)

DATABASES = {"default": env.db()}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
