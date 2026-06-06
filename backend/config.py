import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://zxccohjkjhijwujgpkhs.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4Y2NvaGpramhpand1amdwa2hzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkyMjkxMjMsImV4cCI6MjA5NDgwNTEyM30.M8BEHTt0gYStCh0Sh2agVlEOukIAd-KutGsZg6oLP_s")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "your-super-secret-jwt-token-change-this")

DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://postgres:postgres@localhost:5432/agromanager")

# CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
