from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import SafraCreate, SafraUpdate, SafraResponse
from auth import get_current_user, get_current_editor

router = APIRouter(prefix="/api/safras", tags=["safras"])

@router.post("/", response_model=SafraResponse)
async def criar_safra(
    safra: SafraCreate,
    current_user = Depends(get_current_editor)
):
    """Cria uma nova safra"""
    supabase = get_db()
    
    try:
        safra_dict = safra.dict()
        response = supabase.table("safras").insert(safra_dict).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar safra: {str(e)}")

@router.get("/", response_model=list)
async def listar_safras(
    current_user = Depends(get_current_user)
):
    """Lista todas as safras ativas"""
    supabase = get_db()
    
    try:
        response = supabase.table("safras").select("*").eq("active", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao listar safras: {str(e)}")

@router.get("/{safra_id}", response_model=SafraResponse)
async def obter_safra(
    safra_id: str,
    current_user = Depends(get_current_user)
):
    """Obtém uma safra específica"""
    supabase = get_db()
    
    try:
        response = supabase.table("safras").select("*").eq("id", safra_id).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Safra não encontrada: {str(e)}")

@router.put("/{safra_id}", response_model=SafraResponse)
async def atualizar_safra(
    safra_id: str,
    safra: SafraUpdate,
    current_user = Depends(get_current_editor)
):
    """Atualiza uma safra existente"""
    supabase = get_db()
    
    try:
        safra_dict = safra.dict(exclude_unset=True)
        response = supabase.table("safras").update(safra_dict).eq("id", safra_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar safra: {str(e)}")

@router.delete("/{safra_id}")
async def deletar_safra(
    safra_id: str,
    current_user = Depends(get_current_editor)
):
    """Desativa uma safra (soft delete)"""
    supabase = get_db()
    
    try:
        supabase.table("safras").update({"active": False}).eq("id", safra_id).execute()
        return {"message": "Safra desativada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar safra: {str(e)}")
