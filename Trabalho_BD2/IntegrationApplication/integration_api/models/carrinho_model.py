from typing import List, Dict, Optional
from datetime import datetime
from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess

class CarrinhoModel:
    def __init__(self, db_access: DatabaseAccess):
        self.db = db_access

    def criar_carrinho(self, id_usuario: int) -> int:
        now = datetime.now().isoformat()
        carrinho = self.db.add("Carrinho", {
            "id_usuario": id_usuario,
            "id_carrinho": id_usuario,
            "data_criacao": now,
            "data_atualizacao": now
        })
        return carrinho

    def buscar_por_usuario(self, id_carrinho: int) -> Optional[tuple]:
        carrinho = self.db.get_one("Carrinho", {"id_carrinho": id_carrinho})
        print(f"O id do user era {id_carrinho}")
        print(carrinho)
        if not carrinho:
            return None

        itens = self.db.get("Carrinho_Item", {"id_carrinho": id_carrinho})

        # Retorna uma tupla com todos os dados
        return (
            carrinho['id_carrinho'],
            carrinho['id_usuario'],
            datetime.fromisoformat(carrinho['data_criacao']),
            datetime.fromisoformat(carrinho['data_atualizacao']),
            itens  # lista de itens (cada item é um dicionário)
        )

    def atualizar_carrinho(self, id_carrinho: int, itens: List[Dict]) -> bool:
        now = datetime.now().isoformat()

        # Remove os itens antigos
        self.db.delete("Carrinho_Item", {"id_carrinho": id_carrinho})

        # Insere os novos itens
        for item in itens:
            self.db.add("Carrinho_Item", {
                "id_carrinho": id_carrinho,
                "id_item": item.get('id_item'),
                "nome": item.get('nome'),
                "preco": item.get('preco'),
                "quantidade": item.get('quantidade', 1),
                "observacoes": item.get('observacoes', ''),
                "categoria": item.get('categoria', 'outros')
            })

        # Atualiza data de atualização do carrinho
        self.db.update("Carrinho",
                      {"data_atualizacao": now},
                      {"id_carrinho": id_carrinho})
        return True