from typing import List, Dict, Optional
from datetime import datetime
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection


class CarrinhoModel:
    def __init__(self, id_carrinho: int, id_usuario: int, itens: List[Dict],
                 data_criacao: datetime, data_atualizacao: datetime):
        self.id_carrinho = id_carrinho
        self.id_usuario = id_usuario
        self.itens = itens
        self.data_criacao = data_criacao
        self.data_atualizacao = data_atualizacao

    @classmethod
    def criar_carrinho(cls, id_usuario: int) -> int:
        """Cria um novo carrinho vazio para o usuário"""
        now = datetime.now().isoformat()
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Carrinho (id_usuario, data_criacao, data_atualizacao)
                VALUES (?, ?, ?)
            """, (id_usuario, now, now))
            conn.commit()
            return cursor.lastrowid

    @classmethod
    def buscar_por_id(cls, id_carrinho: int) -> Optional['CarrinhoModel']:
        """Busca um carrinho pelo ID, incluindo seus itens"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_carrinho, id_usuario, data_criacao, data_atualizacao
                FROM Carrinho
                WHERE id_carrinho = ?
            """, (id_carrinho,))
            carrinho_row = cursor.fetchone()
            if not carrinho_row:
                return None

            cursor.execute("""
                SELECT id_item, nome, preco, quantidade, observacoes
                FROM Carrinho_Item
                WHERE id_carrinho = ?
            """, (id_carrinho,))
            itens_rows = cursor.fetchall()

            itens = [
                {
                    'id_item': row[0],
                    'nome': row[1],
                    'preco': row[2],
                    'quantidade': row[3],
                    'observacoes': row[4]
                }
                for row in itens_rows
            ]

            return cls(
                id_carrinho=carrinho_row[0],
                id_usuario=carrinho_row[1],
                itens=itens,
                data_criacao=datetime.fromisoformat(carrinho_row[2]),
                data_atualizacao=datetime.fromisoformat(carrinho_row[3])
            )

    @classmethod
    def buscar_por_usuario(cls, id_usuario: int) -> Optional['CarrinhoModel']:
        """Busca o carrinho de um usuário específico"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_carrinho FROM Carrinho WHERE id_usuario = ?
            """, (id_usuario,))
            row = cursor.fetchone()
            if not row:
                return None
            return cls.buscar_por_id(row[0])

    @classmethod
    def atualizar_carrinho(cls, id_carrinho: int, itens: List[Dict]) -> bool:
        """Atualiza os itens do carrinho com base em uma lista de dicionários"""
        now = datetime.now().isoformat()
        with get_connection() as conn:
            cursor = conn.cursor()

            # Remove os itens antigos
            cursor.execute("DELETE FROM Carrinho_Item WHERE id_carrinho = ?", (id_carrinho,))

            # Insere os novos itens
            for item in itens:
                cursor.execute("""
                    INSERT INTO Carrinho_Item (
                        id_carrinho, 
                        id_item, 
                        nome, 
                        preco, 
                        quantidade, 
                        observacoes
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    id_carrinho,
                    item.get('id_item'),
                    item.get('nome'),
                    item.get('preco'),
                    item.get('quantidade', 1),  # Default para 1 se não especificado
                    item.get('observacoes', '')  # Default para string vazia
                ))

            # Atualiza data de atualização do carrinho
            cursor.execute("""
                UPDATE Carrinho 
                SET data_atualizacao = ? 
                WHERE id_carrinho = ?
            """, (now, id_carrinho))

            conn.commit()
            return True

    @classmethod
    def limpar_carrinho(cls, id_usuario: int) -> bool:
        """Remove todos os itens do carrinho de um usuário"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_carrinho FROM Carrinho WHERE id_usuario = ?
            """, (id_usuario,))
            row = cursor.fetchone()
            if not row:
                return False
            id_carrinho = row[0]
            cursor.execute("DELETE FROM Carrinho_Item WHERE id_carrinho = ?", (id_carrinho,))
            cursor.execute("""
                UPDATE Carrinho SET data_atualizacao = ? WHERE id_carrinho = ?
            """, (datetime.now().isoformat(), id_carrinho))
            conn.commit()
            return True