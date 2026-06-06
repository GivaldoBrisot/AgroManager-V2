from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthCredentials
from database import get_db
from schemas import LoginRequest, LoginResponse, UsuarioCreate, UsuarioResponse
from auth import hash_password, verify_password, create_access_token, security
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UsuarioResponse)
async def registrar(
    usuario: UsuarioCreate
):
    """Registra um novo usuário"""
    supabase = get_db()
    
    try:
        # Verifica se email já existe
        existing = supabase.table("usuarios").select("*").eq("email", usuario.email).execute()
        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já registrado"
            )
        
        # Cria novo usuário
        usuario_dict = {
            "email": usuario.email,
            "role": usuario.role,
            "password_hash": hash_password(usuario.password)
        }
        
        response = supabase.table("usuarios").insert(usuario_dict).execute()
        user_data = response.data[0]
        
        return UsuarioResponse(
            id=user_data["id"],
            email=user_data["email"],
            role=user_data["role"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao registrar: {str(e)}"
        )

@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest
):
    """Faz login e retorna JWT token"""
    supabase = get_db()
    
    try:
        # Busca usuário por email
        response = supabase.table("usuarios").select("*").eq("email", credentials.email).single().execute()
        user = response.data
        
        # Verifica senha
        if not verify_password(credentials.password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        # Cria token JWT
        access_token_expires = timedelta(days=7)
        access_token = create_access_token(
            data={"sub": user["id"]},
            expires_delta=access_token_expires
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UsuarioResponse(
                id=user["id"],
                email=user["email"],
                role=user["role"]
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )

@router.post("/logout")
async def logout(
    credentials: HTTPAuthCredentials = Depends(security)
):
    """Logout (no backend, apenas informativo)"""
    return {"message": "Desconectado com sucesso. Remova o token no frontend."}
