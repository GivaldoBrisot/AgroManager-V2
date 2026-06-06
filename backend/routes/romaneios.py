from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from schemas import RomaneioCalculoRequest, RomaneioCalculoResponse, RomaneioCreate, RomaneioResponse
from auth import get_current_user, get_current_editor
from datetime import datetime

router = APIRouter(prefix="/api/romaneios", tags=["romaneios"])

@router.post("/calcular", response_model=RomaneioCalculoResponse)
async def calcular_romaneio(
    dados: RomaneioCalculoRequest,
    current_user = Depends(get_current_user)
):
    """
    Calcula os descontos e peso líquido de um romaneio com base nas configurações da empresa
    """
    supabase = get_db()
    
    # Busca as configurações de desconto da empresa
    try:
        empresa_response = supabase.table("empresas").select("descontos").eq("id", dados.id_empresa).single().execute()
        empresa = empresa_response.data
        descontos_config = empresa.get("descontos", {})
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Empresa não encontrada: {str(e)}")
    
    # Obtém a configuração para o cereal específico
    cereal_config = descontos_config.get(dados.id_cereal, {})
    
    tolerancia_umidade = cereal_config.get("toleranciaUmidade", 0)
    tolerancia_impureza = cereal_config.get("toleranciaImpureza", 0)
    tolerancia_avariados = cereal_config.get("toleranciaAvariados", 0)
    tabela_umidade = cereal_config.get("tabelaUmidade", [])
    
    # Cálculos
    peso_bruto = dados.peso_entrada - dados.peso_saida
    
    # Desconto de umidade (busca na tabela)
    peso_umidade = 0
    if dados.umidade_p > tolerancia_umidade:
        # Ordena a tabela de forma decrescente e busca a faixa aplicável
        tabela_ordenada = sorted(tabela_umidade, key=lambda x: x["umidade"], reverse=True)
        for faixa in tabela_ordenada:
            if dados.umidade_p >= faixa["umidade"]:
                peso_umidade = peso_bruto * (faixa["desconto"] / 100)
                break
    
    # Descontos de impureza e avariados (direto da fórmula)
    peso_impureza = 0
    if dados.impureza_p > tolerancia_impureza:
        peso_impureza = peso_bruto * ((dados.impureza_p - tolerancia_impureza) / 100)
    
    peso_avariados = 0
    if dados.avariados_p > tolerancia_avariados:
        peso_avariados = peso_bruto * ((dados.avariados_p - tolerancia_avariados) / 100)
    
    # Outros descontos
    peso_outros_descontos = peso_bruto * (dados.outros_descontos_p / 100)
    
    # Peso líquido
    peso_liquido = peso_bruto - (peso_umidade + peso_impureza + peso_avariados + peso_outros_descontos)
    
    return RomaneioCalculoResponse(
        peso_bruto=round(peso_bruto, 2),
        peso_umidade=round(peso_umidade, 2),
        peso_impureza=round(peso_impureza, 2),
        peso_avariados=round(peso_avariados, 2),
        peso_outros_descontos=round(peso_outros_descontos, 2),
        peso_liquido=round(peso_liquido, 2)
    )

@router.post("/", response_model=RomaneioResponse)
async def criar_romaneio(
    romaneio: RomaneioCreate,
    current_user = Depends(get_current_user)
):
    """Cria um novo romaneio"""
    supabase = get_db()
    
    try:
        romaneio_dict = romaneio.dict()
        romaneio_dict["modificado_por"] = current_user.get("email")
        romaneio_dict["created_at"] = datetime.utcnow().isoformat()
        
        response = supabase.table("romaneios").insert(romaneio_dict).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar romaneio: {str(e)}")

@router.get("/{romaneio_id}", response_model=RomaneioResponse)
async def obter_romaneio(
    romaneio_id: str,
    current_user = Depends(get_current_user)
):
    """Obtém um romaneio específico"""
    supabase = get_db()
    
    try:
        response = supabase.table("romaneios").select("*").eq("id", romaneio_id).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Romaneio não encontrado: {str(e)}")

@router.get("/", response_model=list)
async def listar_romaneios(
    current_user = Depends(get_current_user)
):
    """Lista todos os romaneios ativos"""
    supabase = get_db()
    
    try:
        response = supabase.table("romaneios").select("*").eq("active", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao listar romaneios: {str(e)}")

@router.put("/{romaneio_id}", response_model=RomaneioResponse)
async def atualizar_romaneio(
    romaneio_id: str,
    romaneio: RomaneioUpdate,
    current_user = Depends(get_current_editor)
):
    """Atualiza um romaneio existente"""
    supabase = get_db()
    
    try:
        romaneio_dict = romaneio.dict(exclude_unset=True)
        romaneio_dict["modificado_por"] = current_user.get("email")
        
        response = supabase.table("romaneios").update(romaneio_dict).eq("id", romaneio_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar romaneio: {str(e)}")

@router.delete("/{romaneio_id}")
async def deletar_romaneio(
    romaneio_id: str,
    current_user = Depends(get_current_editor)
):
    """Desativa um romaneio (soft delete)"""
    supabase = get_db()
    
    try:
        supabase.table("romaneios").update({"active": False}).eq("id", romaneio_id).execute()
        return {"message": "Romaneio desativado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar romaneio: {str(e)}")
