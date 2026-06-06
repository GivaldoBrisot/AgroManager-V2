from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import FazendaCreate, FazendaUpdate, FazendaResponse
from auth import get_current_user, get_current_editor

router = APIRouter(prefix="/api/fazendas", tags=["fazendas"])

@router.post("/", response_model=FazendaResponse)
async def criar_fazenda(
    fazenda: FazendaCreate,
    current_user = Depends(get_current_editor)
):
    """Cria uma nova fazenda"""
    supabase = get_db()
    
    try:
        fazenda_dict = fazenda.dict()
        response = supabase.table("fazendas").insert(fazenda_dict).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar fazenda: {str(e)}")

@router.get("/", response_model=list)
async def listar_fazendas(
    current_user = Depends(get_current_user)
):
    """Lista todas as fazendas ativas"""
    supabase = get_db()
    
    try:
        response = supabase.table("fazendas").select("*").eq("active", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao listar fazendas: {str(e)}")

@router.get("/{fazenda_id}", response_model=FazendaResponse)
async def obter_fazenda(
    fazenda_id: str,
    current_user = Depends(get_current_user)
):
    """Obtém uma fazenda específica"""
    supabase = get_db()
    
    try:
        response = supabase.table("fazendas").select("*").eq("id", fazenda_id).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Fazenda não encontrada: {str(e)}")

@router.put("/{fazenda_id}", response_model=FazendaResponse)
async def atualizar_fazenda(
    fazenda_id: str,
    fazenda: FazendaUpdate,
    current_user = Depends(get_current_editor)
):
    """Atualiza uma fazenda existente"""
    supabase = get_db()
    
    try:
        fazenda_dict = fazenda.dict(exclude_unset=True)
        response = supabase.table("fazendas").update(fazenda_dict).eq("id", fazenda_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar fazenda: {str(e)}")

@router.delete("/{fazenda_id}")
async def deletar_fazenda(
    fazenda_id: str,
    current_user = Depends(get_current_editor)
):
    """Desativa uma fazenda (soft delete)"""
    supabase = get_db()
    
    try:
        supabase.table("fazendas").update({"active": False}).eq("id", fazenda_id).execute()
        return {"message": "Fazenda desativada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar fazenda: {str(e)}")
