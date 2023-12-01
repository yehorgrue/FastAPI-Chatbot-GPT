from dotenv import load_dotenv
import os

load_dotenv()

API_VERSION_STR: str = "/api/v1"
RASA_URL = os.getenv("RASA_URL", "http://localhost:5005")
ZEP_URL = os.getenv("ZEP_URL", "http://localhost:8000")
PROJECT_NAME = os.getenv("PROJECT_NAME", "AI Assistant")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PG_DB_HOST = os.getenv("PG_DB_HOST", "localhost")
PG_DB_USERNAME = os.getenv("PG_DB_USERNAME", "postgres")
PG_DB_PASSWORD = os.getenv("PG_DB_PASSWORD", "1234")
PG_DB_PORT = os.getenv("PG_DB_PORT", "5432")
PG_DB_NAME = os.getenv("PG_DB_NAME", "postgres")

# SSO config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID", "")
FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET", "")


# HOSTNAME used to build google redirect uri
SSO_CALLBACK_HOSTNAME = os.getenv("SSO_CALLBACK_HOSTNAME", "http://localhost:8001")
SSO_LOGIN_CALLBACK_URL = os.getenv(
    "SSO_LOGIN_CALLBACK_URL", "http://localhost:8001/sso-login-callback/"
)


DB_URL = os.getenv("DB_URL")

ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

SECRET_KEY: str = "temporarysecretkey"

OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
