import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# YouTube Settings
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "token.pickle"

# Upload Settings
UPLOAD_SCHEDULE = os.getenv("UPLOAD_SCHEDULE", "daily")
UPLOAD_TIME = os.getenv("UPLOAD_TIME", "18:00")
LANGUAGE = os.getenv("LANGUAGE", "id")

# Video Settings
VIDEO_DURATION = 60  # seconds
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30

# Database
DB_FILE = "topics.db"

# Topics for Indonesian content
TOPICS = [
    "Fakta Menarik Tentang Hewan",
    "Tips Kesehatan Harian",
    "Sejarah Dunia yang Jarang Diketahui",
    "Teknologi Terbaru",
    "Motivasi Hidup",
    "Tips Produktivitas",
    "Fenomena Alam yang Menakjubkan",
    "Kisah Inspiratif",
    "Tips Keuangan Pribadi",
    "Psikologi Manusia"
]
