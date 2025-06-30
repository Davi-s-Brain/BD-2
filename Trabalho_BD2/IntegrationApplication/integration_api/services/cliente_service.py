from fastapi import HTTPException, status
from typing import List
from Trabalho_BD2.IntegrationApplication.integration_api.models.cliente_model import ClienteModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.cliente_schemas import ClienteCreate, ClienteUpdate, \
    ClienteOut, ClientePass


class ClienteService:
    def __init__(self, cliente_model: ClienteModel = None):
        self.model = cliente_model or ClienteModel()

    def criar_cliente(self, cliente_data: ClienteCreate) -> ClienteOut:
        """
        Cria um novo cliente com validações de email e CPF

        Args:
            cliente_data: Dados do cliente a ser criado

        Returns:
            ClienteOut: Cliente criado

        Raises:
            HTTPException: Se email ou CPF já estiverem cadastrados
        """
        # Verifica se email já existe
        if self.model.buscar_por_email(str(cliente_data.E_mail_client)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

        # Verifica se CPF já existe
        if self.model.buscar_por_cpf(cliente_data.CPF_client):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado"
            )

        # Cria o cliente
        cliente = self.model.criar_cliente(cliente_data)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar cliente"
            )

        return cliente

    def obter_cliente(self, cliente_id: int) -> ClienteOut:
        """
        Obtém um cliente pelo ID

        Args:
            cliente_id: ID do cliente

        Returns:
            ClienteOut: Cliente encontrado

        Raises:
            HTTPException: Se cliente não for encontrado
        """
        cliente = self.model.buscar_por_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        return cliente

    def obter_cliente_por_email(self, email: str) -> ClienteOut:
        """
        Obtém um cliente pelo email

        Args:
            email: Email do cliente

        Returns:
            ClienteOut: Cliente encontrado

        Raises:
            HTTPException: Se cliente não for encontrado
        """
        cliente = self.model.buscar_por_email(email)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        return cliente

    def listar_clientes(self) -> List[ClienteOut]:
        """
        Lista todos os clientes cadastrados

        Returns:
            Lista de ClienteOut
        """
        return self.model.listar_clientes()

    def atualizar_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> ClienteOut:
        """
        Atualiza os dados de um cliente

        Args:
            cliente_id: ID do cliente a ser atualizado
            cliente_data: Dados parciais para atualização

        Returns:
            ClienteOut: Cliente atualizado

        Raises:
            HTTPException: Se cliente não for encontrado ou email já existir
        """
        # Verifica se o cliente existe
        cliente_atual = self.model.buscar_por_id(cliente_id)
        if not cliente_atual:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )

        # Verifica se o novo email já está em uso por outro cliente
        if cliente_data.E_mail_client and cliente_data.E_mail_client != cliente_atual.E_mail_client:
            if self.model.buscar_por_email(str(cliente_data.E_mail_client)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado"
                )

        # Remove campos que não podem ser atualizados
        update_data = cliente_data.dict(exclude_unset=True)
        update_data.pop('CPF_client', None)  # CPF não pode ser alterado

        # Atualiza o cliente
        cliente_atualizado = self.model.atualizar_cliente(cliente_id, ClienteUpdate(**update_data))
        if not cliente_atualizado:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar cliente"
            )

        return cliente_atualizado

    def remover_cliente(self, cliente_id: int) -> dict:
        """
        Remove um cliente do sistema

        Args:
            cliente_id: ID do cliente a ser removido

        Returns:
            dict: Mensagem de confirmação

        Raises:
            HTTPException: Se cliente não for encontrado
        """
        # Verifica se o cliente existe
        if not self.model.buscar_por_id(cliente_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )

        # Remove o cliente
        if not self.model.remover_cliente(cliente_id):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao remover cliente"
            )

        return {"message": "Cliente removido com sucesso"}