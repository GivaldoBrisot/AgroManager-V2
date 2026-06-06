from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import CerealCreate, CerealUpdate, CerealResponse
from auth import get_current_user, get_current_editor

router = APIRouter(prefix="/api/cereais", tags=["cereais"])

@router.post("/", response_model=CerealResponse)
async def criar_cereal(
    cereal: CerealCreate,
    current_user = Depends(get_current_editor)
):
    """Cria um novo cereal"""
    supabase = get_db()
    
    try:
        cereal_dict = cereal.dict()
        response = supabase.table("cereais").insert(cereal_dict).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar cereal: {str(e)}")

@router.get("/", response_model=list)
async def listar_cereais(
    current_user = Depends(get_current_user)
):
    """Lista todos os cereais ativos"""
    supabase = get_db()
    
    try:
        response = supabase.table("cereais").select("*").eq("active", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao listar cereais: {str(e)}")

@router.get("/{cereal_id}", response_model=CerealResponse)
async def obter_cereal(
    cereal_id: str,
    current_user = Depends(get_current_user)
):
    """Obtém um cereal específico"""
    supabase = get_db()
    
    try:
        response = supabase.table("cereais").select("*").eq("id", cereal_id).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cereal não encontrado: {str(e)}")

@router.put("/{cereal_id}", response_model=CerealResponse)
async def atualizar_cereal(
    cereal_id: str,
    cereal: CerealUpdate,
    current_user = Depends(get_current_editor)
):
    """Atualiza um cereal existente"""
    supabase = get_db()
    
    try:
        cereal_dict = cereal.dict(exclude_unset=True)
        response = supabase.table("cereais").update(cereal_dict).eq("id", cereal_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar cereal: {str(e)}")

@router.delete("/{cereal_id}")
async def deletar_cereal(
    cereal_id: str,
    current_user = Depends(get_current_editor)
):
    """Desativa um cereal (soft delete)"""
    supabase = get_db()
    
    try:
        supabase.table("cereais").update({"active": False}).eq("id", cereal_id).execute()
        return {"message": "Cereal desativado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar cereal: {str(e)}")
