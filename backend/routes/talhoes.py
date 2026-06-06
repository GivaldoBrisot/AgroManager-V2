from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import TalhaoCreate, TalhaoUpdate, TalhaoResponse
from auth import get_current_user, get_current_editor

router = APIRouter(prefix="/api/talhoes", tags=["talhoes"])

@router.post("/", response_model=TalhaoResponse)
async def criar_talhao(
    talhao: TalhaoCreate,
    current_user = Depends(get_current_editor)
):
    """Cria um novo talhão"""
    supabase = get_db()
    
    try:
        talhao_dict = talhao.dict()
        response = supabase.table("talhoes").insert(talhao_dict).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar talhão: {str(e)}")

@router.get("/", response_model=list)
async def listar_talhoes(
    current_user = Depends(get_current_user)
):
    """Lista todos os talhões ativos"""
    supabase = get_db()
    
    try:
        response = supabase.table("talhoes").select("*").eq("active", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao listar talhões: {str(e)}")

@router.get("/fazenda/{fazenda_id}", response_model=list)
async def listar_talhoes_por_fazenda(
    fazenda_id: str,
    current_user = Depends(get_current_user)
):
    """Lista talhões de uma fazenda específica"""
    supabase = get_db()
    
    try:
        response = supabase.table("talhoes").select("*").eq("id_fazenda", fazenda_id).eq("active", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao listar talhões: {str(e)}")

@router.get("/{talhao_id}", response_model=TalhaoResponse)
async def obter_talhao(
    talhao_id: str,
    current_user = Depends(get_current_user)
):
    """Obtém um talhão específico"""
    supabase = get_db()
    
    try:
        response = supabase.table("talhoes").select("*").eq("id", talhao_id).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Talhão não encontrado: {str(e)}")

@router.put("/{talhao_id}", response_model=TalhaoResponse)
async def atualizar_talhao(
    talhao_id: str,
    talhao: TalhaoUpdate,
    current_user = Depends(get_current_editor)
):
    """Atualiza um talhão existente"""
    supabase = get_db()
    
    try:
        talhao_dict = talhao.dict(exclude_unset=True)
        response = supabase.table("talhoes").update(talhao_dict).eq("id", talhao_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar talhão: {str(e)}")

@router.delete("/{talhao_id}")
async def deletar_talhao(
    talhao_id: str,
    current_user = Depends(get_current_editor)
):
    """Desativa um talhão (soft delete)"""
    supabase = get_db()
    
    try:
        supabase.table("talhoes").update({"active": False}).eq("id", talhao_id).execute()
        return {"message": "Talhão desativado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar talhão: {str(e)}")
