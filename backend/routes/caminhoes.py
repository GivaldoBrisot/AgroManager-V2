from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import CaminhaoCreate, CaminhaoUpdate, CaminhaoResponse
from auth import get_current_user, get_current_editor

router = APIRouter(prefix="/api/caminhoes", tags=["caminhoes"])

@router.post("/", response_model=CaminhaoResponse)
async def criar_caminhao(
    caminhao: CaminhaoCreate,
    current_user = Depends(get_current_editor)
):
    """Cria um novo caminhão"""
    supabase = get_db()
    
    try:
        caminhao_dict = caminhao.dict()
        response = supabase.table("caminhoes").insert(caminhao_dict).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar caminhão: {str(e)}")

@router.get("/", response_model=list)
async def listar_caminhoes(
    current_user = Depends(get_current_user)
):
    """Lista todos os caminhões ativos"""
    supabase = get_db()
    
    try:
        response = supabase.table("caminhoes").select("*").eq("active", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao listar caminhões: {str(e)}")

@router.get("/{caminhao_id}", response_model=CaminhaoResponse)
async def obter_caminhao(
    caminhao_id: str,
    current_user = Depends(get_current_user)
):
    """Obtém um caminhão específico"""
    supabase = get_db()
    
    try:
        response = supabase.table("caminhoes").select("*").eq("id", caminhao_id).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Caminhão não encontrado: {str(e)}")

@router.put("/{caminhao_id}", response_model=CaminhaoResponse)
async def atualizar_caminhao(
    caminhao_id: str,
    caminhao: CaminhaoUpdate,
    current_user = Depends(get_current_editor)
):
    """Atualiza um caminhão existente"""
    supabase = get_db()
    
    try:
        caminhao_dict = caminhao.dict(exclude_unset=True)
        response = supabase.table("caminhoes").update(caminhao_dict).eq("id", caminhao_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar caminhão: {str(e)}")

@router.delete("/{caminhao_id}")
async def deletar_caminhao(
    caminhao_id: str,
    current_user = Depends(get_current_editor)
):
    """Desativa um caminhão (soft delete)"""
    supabase = get_db()
    
    try:
        supabase.table("caminhoes").update({"active": False}).eq("id", caminhao_id).execute()
        return {"message": "Caminhão desativado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar caminhão: {str(e)}")
