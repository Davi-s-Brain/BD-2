from typing import List, Dict, Optional, Tuple

from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess
from Trabalho_BD2.IntegrationApplication.integration_api.models.carrinho_model import CarrinhoModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.carrinho_schemas import CarrinhoOutSchema, \
    ItemCarrinhoSchema as ItemCarrinho, ItemCarrinhoSchema


def _converter_para_schema(carrinho_data: Tuple) -> CarrinhoOutSchema | None:
    """Converte a tupla de dados do carrinho para o schema de saída"""
    if not carrinho_data:
        print("Dados do carrinho vazios ou não encontrados")
        return None

    try:
        # Debug: mostrar estrutura completa recebida
        print(f"Estrutura completa do carrinho_data: {carrinho_data}")

        # Verifica se temos itens (assumindo que estão na posição 4)
        itens_data = carrinho_data[4] if len(carrinho_data) > 4 else []

        # Converter itens
        itens_schema = []
        for item in itens_data:
            try:
                # Agora usando os nomes dos campos conforme seu dicionário
                itens_schema.append(
                    ItemCarrinhoSchema(
                        id_item=item['id_item'],
                        nome=item['nome'],
                        preco=float(item['preco']),
                        quantidade=int(item['quantidade']),
                        observacoes=item['observacoes'],
                        categoria=item['categoria']
                    )
                )
            except Exception as item_error:
                print(f"Erro ao converter item {item}: {item_error}")
                continue

        print(f"Itens convertidos: {itens_schema}")

        # Criar schema principal
        return CarrinhoOutSchema(
            id_carrinho=int(carrinho_data[0]),
            id_usuario=int(carrinho_data[1]),
            data_criacao=carrinho_data[2],
            data_atualizacao=carrinho_data[3],
            itens=itens_schema,
        )

    except Exception as e:
        print(f"Erro crítico ao converter carrinho: {str(e)}")
        raise  # Re-lança a exceção para tratamento superior


def _extrair_itens(carrinho_data: Tuple) -> List[Dict]:
    """Extrai os itens do carrinho como dicionários"""
    return [
        {
            "id_item": item[0],
            "id_carrinho": item[1],
            "nome": item[2],
            "preco": item[3],
            "quantidade": item[4],
            "observacoes": item[5],
            "categoria": item[6]
        } for item in carrinho_data[4]
    ]


class CarrinhoService:
    def __init__(self, db_access: DatabaseAccess):
        self.model = CarrinhoModel(db_access)

    def obter_carrinho(self, id_usuario: int) -> CarrinhoOutSchema:
        """Obtém ou cria um carrinho para o usuário"""
        carrinho_data = self._buscar_carrinho_por_usuario(id_usuario)
        if not carrinho_data:
            id_carrinho = self.model.criar_carrinho(id_usuario)
            if not id_carrinho:
                print("Carrinho nao foi criado")
            carrinho_data = self.model.buscar_por_usuario(id_usuario)

        return _converter_para_schema(carrinho_data)

    def adicionar_item(self, id_usuario: int, item: ItemCarrinho) -> CarrinhoOutSchema:
        """Adiciona um item ao carrinho do usuário"""
        carrinho_data = self._buscar_carrinho_por_usuario(id_usuario)

        print(f"os dados do carrinho encontrado foram {carrinho_data}")
        if not carrinho_data:
            id_carrinho = self.model.criar_carrinho(id_usuario)
            carrinho_data = self.model.buscar_por_usuario(id_usuario)
            if not carrinho_data:
                carrinho_data = self.model.criar_carrinho(id_usuario=id_usuario)
        print(carrinho_data)
        itens = carrinho_data[4]
        novo_item = item

        # Verifica se o item já existe
        item_existente = next(
            (i for i in itens if i.get('id_item') == item['id_item']),
            None
        )

        if item_existente:
            item_existente ['quantidade'] += item['quantidade']
        else:
            itens.append(novo_item)

        self.model.atualizar_carrinho(carrinho_data[0], itens)
        return self.obter_carrinho(id_usuario)

    def remover_item(self, id_usuario: int, id_item: int) -> CarrinhoOutSchema:
        """Remove um item do carrinho do usuário"""
        carrinho_data = self._buscar_carrinho_por_usuario(id_usuario)
        if not carrinho_data:
            raise ValueError("Carrinho não encontrado")

        itens = [item for item in carrinho_data.get("itens", [])
                 if item.get('id_item') != id_item]

        self.model.atualizar_carrinho(carrinho_data["id_carrinho"], itens)
        return self.obter_carrinho(id_usuario)

    def atualizar_item(self, id_usuario: int, id_item: int, quantidade: int) -> CarrinhoOutSchema:
        """Atualiza a quantidade de um item no carrinho"""
        carrinho_data = self._buscar_carrinho_por_usuario(id_usuario)
        if not carrinho_data:
            raise ValueError("Carrinho não encontrado")

        itens = []
        for item in carrinho_data.get("itens", []):
            if item.get('id_item') == id_item:
                item['quantidade'] = quantidade
            itens.append(item)

        self.model.atualizar_carrinho(carrinho_data["id_carrinho"], itens)
        return self.obter_carrinho(id_usuario)

    def atualizar_carrinho_completo(self, id_usuario: int, novos_itens: List[ItemCarrinho]) -> CarrinhoOutSchema:
        """Atualiza todos os itens do carrinho"""
        carrinho_data = self._buscar_carrinho_por_usuario(id_usuario)
        if not carrinho_data:
            raise ValueError("Carrinho não encontrado")

        itens = [item.model_dump() for item in novos_itens]
        self.model.atualizar_carrinho(id_usuario, itens)
        return self.obter_carrinho(id_usuario)

    def limpar_carrinho(self, id_usuario: int) -> bool:
        """Remove todos os itens do carrinho"""
        carrinho_data = self._buscar_carrinho_por_usuario(id_usuario)
        if not carrinho_data:
            return False

        return self.model.atualizar_carrinho(carrinho_data["id_carrinho"], [])

    def contar_itens_por_categoria(self, id_usuario: int) -> Dict[str, int]:
        """Conta itens por categoria no carrinho do usuário"""
        carrinho = self.obter_carrinho(id_usuario)
        if not carrinho.itens:
            return {}

        contagem = {}
        for item in carrinho.itens:
            categoria = item.categoria or "Sem categoria"
            contagem[categoria] = contagem.get(categoria, 0) + item.quantidade

        return contagem

    def _buscar_carrinho_por_usuario(self, id_usuario: int) -> Optional[Dict]:
        return self.model.buscar_por_usuario(id_usuario)

