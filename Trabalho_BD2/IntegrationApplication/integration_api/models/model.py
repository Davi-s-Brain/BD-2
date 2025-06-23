from typing import Optional, List
from datetime import datetime
import hashlib
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection


class ClienteModel:
    def __init__(self, Id_cliente: int, Primeiro_nome_client: str, Ultimo_nome_client: str,
                 Data_nascimento_client: datetime, CPF_client: str, Telefone_client: str,
                 E_mail_client: str, Data_cadastro_client: datetime, Genero_client: str,
                 E_intolerante_lactose: bool, E_celiaco: bool, E_vegetariano: bool,
                 E_vegano: bool, Senha_cliente: str):
        self.Id_cliente = Id_cliente
        self.Primeiro_nome_client = Primeiro_nome_client
        self.Ultimo_nome_client = Ultimo_nome_client
        self.Data_nascimento_client = Data_nascimento_client
        self.CPF_client = CPF_client
        self.Telefone_client = Telefone_client
        self.E_mail_client = E_mail_client
        self.Data_cadastro_client = Data_cadastro_client
        self.Genero_client = Genero_client
        self.E_intolerante_lactose = E_intolerante_lactose
        self.E_celiaco = E_celiaco
        self.E_vegetariano = E_vegetariano
        self.E_vegano = E_vegano
        self.Senha_cliente = Senha_cliente

    @classmethod
    def criar_cliente(cls, cliente_data: dict) -> int:
        """Cria um novo cliente no banco de dados"""
        hashed_password = hashlib.sha256(cliente_data['Senha_cliente'].encode()).hexdigest()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Cliente (
                    Primeiro_nome_client, Ultimo_nome_client, Data_nascimento_client,
                    CPF_client, Telefone_client, E_mail_client, Genero_client,
                    E_intolerante_lactose, E_celiaco, E_vegetariano, E_vegano,
                    Senha_cliente, Data_cadastro_client
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cliente_data['Primeiro_nome_client'],
                cliente_data['Ultimo_nome_client'],
                cliente_data['Data_nascimento_client'],
                cliente_data['CPF_client'],
                cliente_data['Telefone_client'],
                cliente_data['E_mail_client'],
                cliente_data['Genero_client'],
                cliente_data['E_intolerante_lactose'],
                cliente_data['E_celiaco'],
                cliente_data['E_vegetariano'],
                cliente_data['E_vegano'],
                hashed_password,
                datetime.now()
            ))
            conn.commit()
            return cursor.lastrowid

    @classmethod
    def buscar_por_id(cls, Id_cliente: int) -> Optional['ClienteModel']:
        """Busca um cliente pelo ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM Cliente WHERE Id_cliente = ?
            """, (Id_cliente,))
            row = cursor.fetchone()

            if row:
                return cls(
                    Id_cliente=row[0],
                    Primeiro_nome_client=row[1],
                    Ultimo_nome_client=row[2],
                    Data_nascimento_client=datetime.fromisoformat(row[3]),
                    CPF_client=row[4],
                    Telefone_client=row[5],
                    E_mail_client=row[6],
                    Data_cadastro_client=datetime.fromisoformat(row[7]),
                    Genero_client=row[8],
                    E_intolerante_lactose=bool(row[9]),
                    E_celiaco=bool(row[10]),
                    E_vegetariano=bool(row[11]),
                    E_vegano=bool(row[12]),
                    Senha_cliente=row[13]
                )
            return row

    @classmethod
    def buscar_por_email(cls, E_mail_client: str) -> Optional['ClienteModel']:
        """Busca um cliente pelo email"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM Cliente WHERE E_mail_client = ?
            """, (E_mail_client,))
            row = cursor.fetchone()

            if row:
                return cls(
                    Id_cliente=row[0],
                    Primeiro_nome_client=row[1],
                    Ultimo_nome_client=row[2],
                    Data_nascimento_client=datetime.fromisoformat(row[3]),
                    CPF_client=row[4],
                    Telefone_client=row[5],
                    E_mail_client=row[6],
                    Data_cadastro_client=datetime.fromisoformat(row[7]),
                    Genero_client=row[8],
                    E_intolerante_lactose=bool(row[9]),
                    E_celiaco=bool(row[10]),
                    E_vegetariano=bool(row[11]),
                    E_vegano=bool(row[12]),
                    Senha_cliente=row[13]
                )
            return row

    @classmethod
    def buscar_por_cpf(cls, CPF_client: str) -> Optional['ClienteModel']:
        """Busca um cliente pelo CPF"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM Cliente WHERE CPF_client = ?
            """, (CPF_client,))
            row = cursor.fetchone()

            if row:
                return cls(
                    Id_cliente=row[0],
                    Primeiro_nome_client=row[1],
                    Ultimo_nome_client=row[2],
                    Data_nascimento_client=datetime.fromisoformat(row[3]),
                    CPF_client=row[4],
                    Telefone_client=row[5],
                    E_mail_client=row[6],
                    Data_cadastro_client=datetime.fromisoformat(row[7]),
                    Genero_client=row[8],
                    E_intolerante_lactose=bool(row[9]),
                    E_celiaco=bool(row[10]),
                    E_vegetariano=bool(row[11]),
                    E_vegano=bool(row[12]),
                    Senha_cliente=row[13]
                )
            return row

    @classmethod
    def listar_clientes(cls) -> List['ClienteModel']:
        """Lista todos os clientes"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente")
            rows = cursor.fetchall()

            return [
                cls(
                    Id_cliente=row[0],
                    Primeiro_nome_client=row[1],
                    Ultimo_nome_client=row[2],
                    Data_nascimento_client=datetime.fromisoformat(row[3]),
                    CPF_client=row[4],
                    Telefone_client=row[5],
                    E_mail_client=row[6],
                    Data_cadastro_client=datetime.fromisoformat(row[7]),
                    Genero_client=row[8],
                    E_intolerante_lactose=bool(row[9]),
                    E_celiaco=bool(row[10]),
                    E_vegetariano=bool(row[11]),
                    E_vegano=bool(row[12]),
                    Senha_cliente=row[13]
                ) for row in rows
            ]

    @classmethod
    def atualizar_cliente(cls, Id_cliente: int, update_data: dict) -> bool:
        """Atualiza os dados de um cliente"""
        if 'Senha_cliente' in update_data:
            update_data['Senha_cliente'] = hashlib.sha256(update_data['Senha_cliente'].encode()).hexdigest()

        if not update_data:
            return False

        set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
        values = list(update_data.values())
        values.append(Id_cliente)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE Cliente
                SET {set_clause}
                WHERE Id_cliente = ?
            """, values)
            conn.commit()
            return cursor.rowcount > 0

    @classmethod
    def remover_cliente(cls, Id_cliente: int) -> bool:
        """Remove um cliente do banco de dados"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM Cliente WHERE Id_cliente = ?
            """, (Id_cliente,))
            conn.commit()
            return cursor.rowcount > 0