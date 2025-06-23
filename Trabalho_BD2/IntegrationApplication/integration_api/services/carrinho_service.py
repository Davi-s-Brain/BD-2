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
            data_atualizacao=carrinho.data_atualizacao
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