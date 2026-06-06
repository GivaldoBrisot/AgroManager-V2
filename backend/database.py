from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Inicializa cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_supabase():
    return supabase

def get_db():
    return supabase
