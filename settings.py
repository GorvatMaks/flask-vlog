import os


PAHT_DIRNAME = os.path.dirname(__file__)

STATIC_URL = os.path.join(PAHT_DIRNAME, "static")
TEMPLATES_URL = os.path.join(PAHT_DIRNAME, "templates")
DB_URL = os.path.join(PAHT_DIRNAME, "vlog.db")
