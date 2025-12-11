import os
from dotenv import load_dotenv

load_dotenv()  # Load env vars

# PostgreSQL URL format:
# postgresql://username:password@hostname:port/dbname

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://aaa:aaa@localhost:5432/testdb"
)

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 7
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "super-secret-key")

print("JWT_SECRET loaded:", JWT_SECRET)


# Whisper settings
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

# CORS
ALLOWED_ORIGINS = ["*"]
