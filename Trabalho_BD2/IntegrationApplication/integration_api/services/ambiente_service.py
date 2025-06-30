from typing import List, Dict, Optional, Tuple

from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess
from Trabalho_BD2.IntegrationApplication.integration_api.models.ambiente_model import AmbienteModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.ambiente import (
    AmbienteCreateSchema,
    AmbienteOutSchema, AmbienteUpdateSchema
)


def _converter_para_schema(ambiente_data: Tuple) -> AmbienteOutSchema | None:
    """Converte a tupla de dados do ambiente para o schema de saída"""
    if not ambiente_data:
        print("Dados do ambiente vazios ou não encontrados")
        return None

    try:
        return AmbienteOutSchema(
            Id_Amb=ambiente_data[0],
            Id_franquia=ambiente_data[1],
            Tamanho_ambiente=ambiente_data[2],
            Quantidade_desse_ambiente=ambiente_data[3],
            Nivel_limpeza=ambiente_data[4],
            Detetizado=bool(ambiente_data[5]),
            Salao=bool(ambiente_data[6]) if ambiente_data[6] is not None else None,
            Cozinha=bool(ambiente_data[7]) if ambiente_data[7] is not None else None
        )
    except Exception as e:
        print(f"Erro crítico ao converter ambiente: {str(e)}")
        raise


class AmbienteService:
    def __init__(self, db_access: DatabaseAccess):
        self.model = AmbienteModel(db_access)

    def criar_ambiente(self, ambiente_data: AmbienteCreateSchema) -> AmbienteOutSchema:
        """Cria um novo ambiente"""
        ambiente_dict = ambiente_data.model_dump()
        id_ambiente = self.model.criar_ambiente(ambiente_dict)
        ambiente = self.model.buscar_por_id(id_ambiente)
        return _converter_para_schema(ambiente)

    def listar_todos_os_ambientes(self) -> List[Dict]:
        """
        Retorna todos os ambientes do sistema.

        Returns:
            List[Dict]: Lista de ambientes em formato de dicionário.
        """
        return self.model.get_all()

    def obter_ambiente(self, id_ambiente: int) -> Optional[AmbienteOutSchema]:
        """Obtém um ambiente pelo ID"""
        ambiente_data = self.model.buscar_por_id(id_ambiente)
        return _converter_para_schema(ambiente_data)

    def obter_ambientes_por_franquia(self, id_franquia: int) -> List[AmbienteOutSchema]:
        """Obtém todos os ambientes de uma franquia"""
        ambientes_data = self.model.buscar_por_franquia(id_franquia)
        return [_converter_para_schema(amb) for amb in ambientes_data if amb]

    def atualizar_ambiente(self, id_ambiente: int, update_data: AmbienteUpdateSchema) -> Optional[AmbienteOutSchema]:
        """Atualiza um ambiente existente"""
        update_dict = update_data.model_dump(exclude_unset=True)
        success = self.model.atualizar_ambiente(id_ambiente, update_dict)
        if not success:
            return None
        return self.obter_ambiente(id_ambiente)

    def remover_ambiente(self, id_ambiente: int) -> bool:
        """Remove um ambiente"""
        return self.model.remover_ambiente(id_ambiente)

    def atualizar_limpeza(self, id_ambiente: int, nivel_limpeza: str, detetizado: bool) -> Optional[AmbienteOutSchema]:
        """Atualiza informações de limpeza do ambiente"""
        update_data = {
            "Nivel_limpeza": nivel_limpeza,
            "Detetizado": detetizado
        }
        success = self.model.atualizar_ambiente(id_ambiente, update_data)
        if not success:
            return None
        return self.obter_ambiente(id_ambiente)

    def contar_ambientes_por_tipo(self, id_franquia: int) -> Dict[str, int]:
        """Conta ambientes por tipo (Salão/Cozinha)"""
        ambientes = self.obter_ambientes_por_franquia(id_franquia)
        contagem = {
            "Salão": 0,
            "Cozinha": 0,
            "Outros": 0
        }

        for amb in ambientes:
            if amb.Salao:
                contagem["Salão"] += 1
            elif amb.Cozinha:
                contagem["Cozinha"] += 1
            else:
                contagem["Outros"] += 1

        return contagem