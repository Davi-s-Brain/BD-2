from typing import List

from fastapi import HTTPException, status

from Trabalho_BD2.IntegrationApplication.integration_api.models.model import ClienteModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.cliente_schemas import ClienteCreate, ClienteUpdate


class ClienteService:
    @staticmethod
    def criar_cliente(cliente_data: ClienteCreate) -> ClienteModel:
        if ClienteModel.buscar_por_email(str(cliente_data.E_mail_client)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        if ClienteModel.buscar_por_cpf(cliente_data.CPF_client):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado"
            )

        cliente_id = ClienteModel.criar_cliente(cliente_data.dict())
        cliente = ClienteModel.buscar_por_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=500, detail="Erro ao criar cliente")
        return cliente

    @staticmethod
    def obter_cliente(cliente_id: int) -> ClienteModel:
        cliente = ClienteModel.buscar_por_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        return cliente

    @staticmethod
    def obter_cliente_por_email(email: str) -> ClienteModel:
        cliente = ClienteModel.buscar_por_email(email)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        return cliente

    @staticmethod
    def listar_clientes() -> List[ClienteModel]:
        return ClienteModel.listar_clientes()

    @staticmethod
    def atualizar_cliente(cliente_id: int, cliente_data: ClienteUpdate) -> ClienteModel:
        cliente_atual = ClienteModel.buscar_por_id(cliente_id)
        if not cliente_atual:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )

        if cliente_data.E_mail_client and cliente_data.E_mail_client != cliente_atual.E_mail_client:
            if ClienteModel.buscar_por_email(str(cliente_data.E_mail_client)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado"
                )

        update_data = cliente_data.dict(exclude_unset=True)
        update_data.pop('CPF_client', None)  # CPF não pode ser alterado

        ClienteModel.atualizar_cliente(cliente_id, update_data)
        return ClienteModel.buscar_por_id(cliente_id)

    @staticmethod
    def remover_cliente(cliente_id: int) -> dict:
        if not ClienteModel.buscar_por_id(cliente_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        ClienteModel.remover_cliente(cliente_id)
        return {"message": "Cliente removido com sucesso"}
