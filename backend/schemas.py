from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# ============ SCHEMAS ROMANEIOS ============
class RomaneioBase(BaseModel):
    id_safra: Optional[str] = None
    id_cereal: Optional[str] = None
    id_fazenda: Optional[str] = None
    id_talhao: Optional[str] = None
    id_empresa: Optional[str] = None
    id_caminhao: Optional[str] = None
    peso_entrada: Optional[float] = None
    peso_saida: Optional[float] = None
    peso_bruto: Optional[float] = None
    umidade_p: Optional[float] = None
    impureza_p: Optional[float] = None
    avariados_p: Optional[float] = None
    outros_descontos_p: Optional[float] = None
    peso_umidade: Optional[float] = None
    peso_impureza: Optional[float] = None
    peso_avariados: Optional[float] = None
    peso_outros_descontos: Optional[float] = None
    peso_liquido: Optional[float] = None
    ticket_balanca: Optional[str] = None
    nf: Optional[str] = None
    observacoes: Optional[str] = None
    data: Optional[str] = None
    hora: Optional[str] = None
    modificado_por: Optional[str] = None
    active: Optional[bool] = True

class RomaneioCreate(RomaneioBase):
    pass

class RomaneioUpdate(RomaneioBase):
    pass

class RomaneioResponse(RomaneioBase):
    id: str
    created_at: Optional[datetime] = None

class RomaneioCalculoRequest(BaseModel):
    id_empresa: str
    id_cereal: str
    peso_entrada: float
    peso_saida: float
    umidade_p: float
    impureza_p: float
    avariados_p: float
    outros_descontos_p: float

class RomaneioCalculoResponse(BaseModel):
    peso_bruto: float
    peso_umidade: float
    peso_impureza: float
    peso_avariados: float
    peso_outros_descontos: float
    peso_liquido: float

# ============ SCHEMAS FAZENDAS ============
class FazendaBase(BaseModel):
    nome: str
    area: Optional[float] = None
    ie: Optional[str] = None
    active: Optional[bool] = True

class FazendaCreate(FazendaBase):
    pass

class FazendaUpdate(FazendaBase):
    pass

class FazendaResponse(FazendaBase):
    id: str

# ============ SCHEMAS TALHOES ============
class TalhaoBase(BaseModel):
    id_fazenda: Optional[str] = None
    numero: Optional[int] = None
    nome: Optional[str] = None
    area: Optional[float] = None
    active: Optional[bool] = True

class TalhaoCreate(TalhaoBase):
    pass

class TalhaoUpdate(TalhaoBase):
    pass

class TalhaoResponse(TalhaoBase):
    id: str

# ============ SCHEMAS SAFRAS ============
class SafraBase(BaseModel):
    safra: str
    active: Optional[bool] = True

class SafraCreate(SafraBase):
    pass

class SafraUpdate(SafraBase):
    pass

class SafraResponse(SafraBase):
    id: str

# ============ SCHEMAS CEREAIS ============
class CerealBase(BaseModel):
    cereal: str
    active: Optional[bool] = True

class CerealCreate(CerealBase):
    pass

class CerealUpdate(CerealBase):
    pass

class CerealResponse(CerealBase):
    id: str

# ============ SCHEMAS CAMINHOES ============
class CaminhaoBase(BaseModel):
    placa: str
    motorista: Optional[str] = None
    marca_modelo: Optional[str] = None
    active: Optional[bool] = True

class CaminhaoCreate(CaminhaoBase):
    pass

class CaminhaoUpdate(CaminhaoBase):
    pass

class CaminhaoResponse(CaminhaoBase):
    id: str

# ============ SCHEMAS EMPRESAS ============
class EmpresaBase(BaseModel):
    nome: str
    cnpj: Optional[str] = None
    contato: Optional[str] = None
    descontos: Optional[Dict[str, Any]] = None
    active: Optional[bool] = True

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: str

# ============ SCHEMAS USUARIOS ============
class UsuarioBase(BaseModel):
    email: str
    role: str  # admin, editor, creator, viewer

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    role: str

class UsuarioResponse(UsuarioBase):
    id: str

# ============ SCHEMAS AUTH ============
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UsuarioResponse
