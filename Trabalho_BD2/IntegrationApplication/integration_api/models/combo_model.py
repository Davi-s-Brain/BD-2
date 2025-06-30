from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess


from typing import List, Optional, Dict
from ..core.db import get_connection
from ..db.database_acess import DatabaseAccess
from ..schemas.generics import ItemDisponibilidade


class ComboModel:
    def __init__(self, db_access: DatabaseAccess = None):
        self.db = db_access or DatabaseAccess(get_connection)

    def verificar_disponibilidade(
            self,
            id_lanche: Optional[int] = None,
            id_bebida: Optional[int] = None,
            id_sobremesa: Optional[int] = None,
            id_acompanhamento: Optional[int] = None
    ) -> List[ItemDisponibilidade]:
        """
        Verifica a disponibilidade dos itens de um combo

        Args:
            id_lanche: ID do lanche (opcional)
            id_bebida: ID da bebida (opcional)
            id_sobremesa: ID da sobremesa (opcional)
            id_acompanhamento: ID do acompanhamento (opcional)

        Returns:
            Lista de ItemDisponibilidade com status de cada item
        """
        itens_combo = []

        # 1. Ingredientes do lanche
        if id_lanche:
            ingredientes = self._get_ingredientes_lanche(id_lanche)
            itens_combo.extend(ingredientes)

        # 2. Bebida
        if id_bebida:
            bebida = self._get_item_simples(id_bebida, "bebida")
            itens_combo.append(bebida)

        # 3. Sobremesa
        if id_sobremesa:
            sobremesa = self._get_item_simples(id_sobremesa, "sobremesa")
            itens_combo.append(sobremesa)

        # 4. Acompanhamento
        if id_acompanhamento:
            acompanhamento = self._get_item_simples(id_acompanhamento, "acompanhamento")
            itens_combo.append(acompanhamento)

        # Verifica disponibilidade
        resultados = []

        for item in itens_combo:
            estoque = self._verificar_estoque(item['nome'])
            disponivel = estoque > 0

            resultados.append(ItemDisponibilidade(
                item=item['nome'],
                quantidade_estoque=estoque,
                mensagem="Disponível" if disponivel else "Indisponível"
            ))

        return resultados

    def _get_ingredientes_lanche(self, id_lanche: int) -> List[Dict]:
        """Obtém ingredientes de um lanche"""
        query = """
        SELECT 
            Ingrediente.Nome_ingred AS nome
        FROM L_Contem_I
        JOIN Ingrediente ON Ingrediente.Id_ingred = L_Contem_I.Id_ingred
        WHERE L_Contem_I.Indice_prod = ?
        """
        return self.db.execute_raw_query(query, (id_lanche,))

    def _get_item_simples(self, item_id: int, tipo: str) -> Dict:
        """Obtém um item simples (bebida, sobremesa ou acompanhamento)"""
        query = """
        SELECT 
            Produto.Nome_prod AS nome
        FROM Produto
        WHERE Produto.Indice_prod = ?
        """
        result = self.db.execute_raw_query(query, (item_id,))
        if not result:
            raise ValueError(f"{tipo.capitalize()} com ID {item_id} não encontrado")
        return result[0]

    def _verificar_estoque(self, nome_item: str) -> float:
        """Verifica quantidade em estoque de um item"""
        query = """
        SELECT Quantidade 
        FROM Estoque
        WHERE Nome_produto = ?
        """
        result = self.db.execute_raw_query(query, (nome_item,))
        if not result or result[0]['Quantidade'] is None:
            return 0.0
        try:
            return float(result[0]['Quantidade'])
        except (ValueError, TypeError):
            return 0.0