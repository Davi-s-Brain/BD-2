from typing import Dict, Any, Optional, List
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection
from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess


class IngredienteModel:
    _db = DatabaseAccess(get_connection)

    def __init__(self, **kwargs):
        self.id_ingred = kwargs.get('Id_ingred')
        self.tipo_ingred = kwargs.get('Tipo_ingred')
        self.nome_ingred = kwargs.get('Nome_ingred')
        self.preco_venda_cliente = kwargs.get('Preco_venda_cliente')
        self.peso_ingred = kwargs.get('Peso_ingred')
        self.indice_estoq = kwargs.get('Indice_estoq')
        self.quantidade = kwargs.get('Quantidade')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Id_ingred': self.id_ingred,
            'Tipo_ingred': self.tipo_ingred,
            'Nome_ingred': self.nome_ingred,
            'Preco_venda_cliente': self.preco_venda_cliente,
            'Peso_ingred': self.peso_ingred,
            'Indice_estoq': self.indice_estoq,
            'Quantidade': self.quantidade
        }

    @classmethod
    def create(cls, **data) -> Optional['IngredienteModel']:
        """Cria novo ingrediente e retorna a instância completa"""
        # Gera o Id_ingred manualmente se não informado
        if data.get('Id_ingred'):
            data['Id_ingred'] = cls._gerar_id_ingred()

        # Garante que todos os campos obrigatórios estejam presentes
        campos_obrigatorios = ['Tipo_ingred', 'Nome_ingred', 'Preco_venda_cliente',
                               'Peso_ingred', 'Indice_estoq', 'Quantidade']
        for campo in campos_obrigatorios:
            if campo not in data or data[campo] is None:
                raise ValueError(f"Campo obrigatório ausente: {campo}")

        try:
            id_inserido = cls._db.add('ingrediente', data)
            return cls.get_by_id(data['Id_ingred'])  # Usa o ID informado, não o retornado
        except Exception as e:
            raise ValueError(f"Erro ao criar ingrediente: {e}")

    @classmethod
    def get_all(cls) -> List['IngredienteModel']:
        rows = cls._db.get('ingrediente')
        return [cls(**row) for row in rows]

    @classmethod
    def get_by_id(cls, ingrediente_id: int) -> Optional['IngredienteModel']:
        row = cls._db.get_one('ingrediente', {'Id_ingred': ingrediente_id})
        return cls(**row) if row else None

    @classmethod
    def _gerar_id_ingred(cls) -> int:
        """Busca o maior Id_ingred existente e retorna o próximo"""
        try:
            result = cls._db._execute_query("SELECT MAX(Id_ingred) AS max_id FROM ingrediente", fetch=True)
            max_id = result[0]['max_id'] if result and result[0]['max_id'] is not None else 0
            return int(max_id) + 1
        except Exception as e:
            raise ValueError(f"Erro ao gerar novo Id_ingred: {e}")

    @classmethod
    def get_by_name(cls, nome: str) -> Optional['IngredienteModel']:
        row = cls._db.get_one('ingrediente', {'Nome_ingred': nome})
        return cls(**row) if row else None

    @classmethod
    def update(cls, ingrediente_id: int, **dados) -> bool:
        """Atualiza um ingrediente e retorna se foi bem sucedido"""
        # Filtra campos None e converte nomes se necessário
        dados_validos = {
            key: value
            for key, value in dados.items()
            if value is not None
        }

        if not dados_validos:
            return False

        return cls._db.update(
            'ingrediente',
            dados_validos,
            {'Id_ingred': ingrediente_id}
        )

    def delete(self) -> bool:
        """Remove o ingrediente atual do banco"""
        return self._db.delete(
            'ingrediente',
            {'Id_ingred': self.id_ingred}
        )

    @classmethod
    def alterar_estoque(cls, nome_ingrediente: str, quantidade: int) -> bool:
        ingrediente = cls.get_by_name(nome_ingrediente)
        if not ingrediente:
            return False

        nova_quantidade = ingrediente.quantidade + quantidade
        if nova_quantidade < 0:
            return False

        ingrediente.quantidade = nova_quantidade
        return cls.update(ingrediente.id_ingred, Quantidade=nova_quantidade)
