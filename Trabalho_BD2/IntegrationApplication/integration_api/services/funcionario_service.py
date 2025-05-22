from datetime import date
from typing import List, Optional

from Trabalho_BD2.IntegrationApplication.integration_api.models.func_model import Funcionario
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.funcionario import (
    FuncionarioCreate,
    FuncionarioUpdate,
)

class FuncionarioService:
    def create(self, data: FuncionarioCreate) -> int:
        """Insere um novo funcionário e retorna o id gerado."""
        return Funcionario.create(
            Id_func = data.Id_func,
            Nome_func=data.Nome_func,
            CPF=data.CPF,
            Data_nasc_func=data.Data_nasc_func.isoformat(),
            Cargo=data.Cargo,
            Salario=data.Salario,
            Data_admissao=data.Data_admissao.isoformat(),
            Turno=data.Turno,
            Tipo_de_contrato=data.Tipo_de_contrato,
            Status_func=data.Status_func,
            Id_franquia=data.Id_franquia,
        )

    def get_all(self) -> List[Funcionario]:
        """Retorna todos os funcionários."""
        return Funcionario.get_all()

    def get_by_id(self, func_id: int) -> Optional[Funcionario]:
        """Retorna um funcionário por ID ou None."""
        return Funcionario.get_by_id(func_id)

    def update(self, func_id: int, data: FuncionarioUpdate) -> bool:
        """Atualiza campos informados de um funcionário; retorna True se encontrado."""
        func = Funcionario.get_by_id(func_id)
        if not func:
            return False

        # Atualiza apenas os campos não nulos
        update_fields = data.dict(exclude_unset=True)
        for field, value in update_fields.items():
            # converter date em string ISO se necessário
            if isinstance(value, date):
                value = value.isoformat()
            setattr(func, field, value)

        func.update()
        return True

    def delete(self, func_id: int) -> bool:
        """Remove funcionário; retorna True se encontrado."""
        func = Funcionario.get_by_id(func_id)
        if not func:
            return False
        func.delete()
        return True