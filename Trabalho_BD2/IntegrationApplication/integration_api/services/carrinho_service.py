from collections import defaultdict
from typing import List, Dict, Optional
from Trabalho_BD2.IntegrationApplication.integration_api.models.carrinho_model import CarrinhoModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.carrinho_schemas import CarrinhoOutSchema


class CarrinhoService:
    def obter_carrinho(self, id_usuario: int) -> Optional[CarrinhoOutSchema]:
        carrinho = CarrinhoModel.buscar_por_usuario(id_usuario)
        if not carrinho:
            id_carrinho = CarrinhoModel.criar_carrinho(id_usuario)
            carrinho = CarrinhoModel.buscar_por_usuario(id_carrinho)

        return CarrinhoOutSchema(
            id_carrinho=carrinho.id_carrinho,
            id_usuario=carrinho.id_usuario,
            itens=carrinho.itens,
            data_criacao=carrinho.data_criacao,
            data_atualizacao=carrinho.data_atualizacao,
        )

    def adicionar_item(self, id_usuario: int, item_data: Dict) -> CarrinhoOutSchema:
        carrinho = CarrinhoModel.buscar_por_usuario(id_usuario)
        if not carrinho:
            id_carrinho = CarrinhoModel.criar_carrinho(id_usuario)
            carrinho = CarrinhoModel.buscar_por_usuario(id_carrinho)

        # Verifica se o item já existe no carrinho
        item_existente = next(
            (i for i in carrinho.itens if i['id_item'] == item_data['id_item']),
            None
        )

        if item_existente:
            item_existente['quantidade'] += item_data.get('quantidade', 1)
        else:
            carrinho.itens.append(item_data)

        CarrinhoModel.atualizar_carrinho(carrinho.id_carrinho, carrinho.itens)
        return self.obter_carrinho(id_usuario)

    def remover_item(self, id_usuario: int, id_item: int) -> CarrinhoOutSchema:
        carrinho = CarrinhoModel.buscar_por_usuario(id_usuario)
        if not carrinho:
            raise ValueError("Carrinho não encontrado")

        carrinho.itens = [item for item in carrinho.itens if item['id_item'] != id_item]
        CarrinhoModel.atualizar_carrinho(carrinho.id_carrinho, carrinho.itens)
        return self.obter_carrinho(id_usuario)

    def atualizar_item(self, id_usuario: int, id_item: int, quantidade: int) -> CarrinhoOutSchema:
        carrinho = CarrinhoModel.buscar_por_usuario(id_usuario)
        if not carrinho:
            raise ValueError("Carrinho não encontrado")

        for item in carrinho.itens:
            if item['id_item'] == id_item:
                item['quantidade'] = quantidade
                break

        CarrinhoModel.atualizar_carrinho(carrinho.id_carrinho, carrinho.itens)
        return self.obter_carrinho(id_usuario)

    def atualizar_carrinho_completo(self, id_usuario: int, itens: List[Dict]) -> CarrinhoOutSchema:
        carrinho = CarrinhoModel.buscar_por_usuario(id_usuario)
        if not carrinho:
            raise ValueError("Carrinho não encontrado")

        CarrinhoModel.atualizar_carrinho(carrinho.id_carrinho, itens)
        return self.obter_carrinho(id_usuario)

    def limpar_carrinho(self, id_usuario: int) -> bool:
        return CarrinhoModel.limpar_carrinho(id_usuario)

    def contar_itens_por_categoria(self, id_usuario: int) -> Dict[str, int]:
        """
        Obtém o carrinho atual do usuário e conta a quantidade de itens por categoria.

        Args:
            id_usuario: ID do usuário para buscar o carrinho

        Returns:
            Um dicionário onde as chaves são os nomes das categorias e os valores
            são as quantidades totais de itens em cada categoria
        """
        carrinho = self.obter_carrinho(id_usuario)
        if not carrinho or not carrinho.itens:
            return {}

        contagem_categorias = defaultdict(int)

        for item in carrinho.itens:
            # Convertemos o item para dicionário se for um modelo Pydantic
            item_dict = item if isinstance(item, dict) else item.dict()
            categoria = item_dict.get('categoria', 'Sem categoria')
            quantidade = item_dict.get('quantidade', 1)
            contagem_categorias[categoria] += quantidade

        return dict(contagem_categorias)
    def contar_itens_por_categoria_global(self) -> Dict[str, int]:
        """
        Conta os itens por categoria em todos os carrinhos.
        """
        carrinhos = CarrinhoModel.buscar_todos()
        contagem_categorias = defaultdict(int)

        for carrinho in carrinhos:
            carrinho_out = self.obter_carrinho(carrinho.id_usuario)
            if not carrinho_out or not carrinho_out.itens:
                continue

            for item in carrinho_out.itens:
                item_dict = item if isinstance(item, dict) else item.dict()
                categoria = item_dict.get('categoria', 'Sem categoria')
                quantidade = item_dict.get('quantidade', 1)
                contagem_categorias[categoria] += quantidade

        return dict(contagem_categorias)