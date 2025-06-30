import sqlite3
import logging
import time
from typing import List, Dict, Optional, Any, Tuple

logger = logging.getLogger('DatabaseAccess')
logger.setLevel(logging.INFO)


class DatabaseAccess:
    def __init__(self, connection_func):
        """Inicialização com tratamento robusto de conexões"""
        self.get_connection = connection_func
        self._transaction_depth = 0
        self._active_connection = None
        logger.info("DatabaseAccess inicializado")

    def execute_raw_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Executa uma query SQL crua, útil para PRAGMAs e introspecção"""
        logger.info("Executando query crua: %s", query)
        return self._execute_query(query, params, fetch=True)

    def _get_connection(self):
        """Obtém conexão ativa com configurações otimizadas"""
        if self._transaction_depth > 0 and self._active_connection:
            return self._active_connection

        conn = self.get_connection()

        if isinstance(conn, sqlite3.Connection):
            # Configurações essenciais para SQLite
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")
            conn.execute("PRAGMA busy_timeout = 5000;")
            conn.isolation_level = None  # Para controle manual

        if self._transaction_depth > 0:
            self._active_connection = conn

        return conn

    def _get_cursor(self, conn):
        """Retorna cursor configurado adequadamente"""
        try:
            if isinstance(conn, sqlite3.Connection):
                conn.row_factory = sqlite3.Row
            return conn.cursor()
        except Exception as e:
            logger.error("Falha ao criar cursor: %s", str(e), exc_info=True)
            raise

    def begin_transaction(self):
        """Inicia transação com lock imediato"""
        if self._transaction_depth == 0:
            conn = self._get_connection()
            conn.execute("BEGIN IMMEDIATE;")
            self._active_connection = conn
        self._transaction_depth += 1
        logger.debug("Transação iniciada (nível: %d)", self._transaction_depth)

    def commit_transaction(self):
        """Finaliza transação com commit"""
        if self._transaction_depth == 1:
            try:
                if self._active_connection:
                    self._active_connection.commit()
                    logger.debug("Commit realizado")
            finally:
                self._close_active_connection()
        self._transaction_depth = max(0, self._transaction_depth - 1)
        logger.debug("Transação commitada (nível: %d)", self._transaction_depth)

    def rollback_transaction(self):
        """Desfaz transação atual"""
        if self._transaction_depth > 0:
            try:
                if self._active_connection:
                    self._active_connection.rollback()
                    logger.debug("Rollback realizado")
            finally:
                self._close_active_connection()
                self._transaction_depth = 0

    def _close_active_connection(self):
        """Fecha conexão ativa de forma segura"""
        if self._active_connection:
            try:
                self._active_connection.close()
                logger.debug("Conexão de transação fechada")
            except Exception as e:
                logger.error("Erro ao fechar conexão: %s", str(e))
            finally:
                self._active_connection = None

    def _execute_query(self, query: str, params: Tuple = None, fetch: bool = False) -> Optional[Any]:
        """Executa query com tratamento completo"""
        query_type = query.strip().upper().split()[0]
        logger.info("Executando query [%s]", query_type)

        conn = None
        cursor = None
        start_time = time.time()

        try:
            # Validação básica da query
            if not query.strip():
                raise ValueError("Query vazia")

            if ";" in query:
                logger.warning("Query contém múltiplas instruções: %s", query)
                # Pega apenas a primeira instrução para segurança
                query = query.split(";")[0].strip()
            conn = self._get_connection()
            cursor = self._get_cursor(conn)

            # Adaptação para PostgreSQL
            final_query = query
            if not isinstance(conn, sqlite3.Connection):
                final_query = query.replace('?', '%s')

            cursor.execute(final_query, params or ())

            # Tratamento dos resultados
            if fetch:
                result = [dict(row) for row in cursor.fetchall()] if isinstance(conn,
                                                                                sqlite3.Connection) else cursor.fetchall()
                logger.info("[%s] retornou %d registros", query_type, len(result))
                return result

            # Tratamento especial para INSERT
            if query_type == "INSERT":
                result = None
                if isinstance(conn, sqlite3.Connection):
                    result = cursor.lastrowid
                    # Força sincronização para garantir visibilidade
                    if self._transaction_depth == 0:
                        cursor.execute("COMMIT; BEGIN;")
                else:
                    cursor.execute("SELECT LASTVAL();")
                    result = cursor.fetchone()[0]

                logger.info("INSERT concluído com ID: %s", result)
                return result

            return None

        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                logger.warning("Banco travado, tentando novamente...")
                time.sleep(0.1)
                return self._execute_query(query, params, fetch)
            raise
        except Exception as e:
            logger.error("Erro na execução: %s", str(e), exc_info=True)
            raise
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn and self._transaction_depth == 0:
                    conn.close()
            except Exception as e:
                logger.error("Erro ao fechar recursos: %s", str(e))

            duration = (time.time() - start_time) * 1000
            logger.info("Tempo de execução [%s]: %.2f ms", query_type, duration)

    def add(self, table: str, data: Dict) -> int:
        """Insere registro com verificação de consistência

        Args:
            table: Nome da tabela
            data: Dados a serem inseridos

        Returns:
            int: Retorna Id_cliente se existir nos dados, caso contrário retorna o ID gerado
        """
        logger.info("Iniciando ADD na tabela '%s'", table)

        try:
            self.begin_transaction()

            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            inserted_id = self._execute_query(query, tuple(data.values()))

            # Verificação usando a mesma conexão/transação
            verify_query = f"SELECT * FROM {table} WHERE rowid = ?"
            result = self._execute_query(verify_query, (inserted_id,), fetch=True)

            if not result:
                raise ValueError("Registro não encontrado após inserção")

            self.commit_transaction()
            logger.info("ADD concluído com sucesso. ID: %s", inserted_id)
            print(f"O id era {inserted_id}")
            # Retorna Id_cliente se existir, senão retorna o inserted_id
            return inserted_id

        except Exception as e:
            self.rollback_transaction()
            logger.error("Erro durante ADD: %s", str(e))
            raise

    def get(self, table: str, conditions: Optional[Dict] = None) -> List[Dict]:
        """Busca múltiplos registros, aceitando nome de tabela ou SQL completo"""
        logger.info("Iniciando GET para '%s'", table)

        try:
            is_raw_sql = table.strip().upper().startswith("SELECT") or table.strip().upper().startswith("PRAGMA")

            if is_raw_sql:
                # Caso especial: o parâmetro já é uma query completa (ex: PRAGMA)
                query = table.strip()
                params = []
            else:
                # Comportamento padrão: SELECT com condições
                query = f"SELECT * FROM {table}"
                params = []

                if conditions:
                    where_clauses = []
                    for key, value in conditions.items():
                        if value is None:
                            where_clauses.append(f"{key} IS NULL")
                        else:
                            where_clauses.append(f"{key} = ?")
                            params.append(value)

                    if where_clauses:
                        query += " WHERE " + " AND ".join(where_clauses)

            logger.debug("Query final: %s", query)
            logger.debug("Parâmetros: %s", params)

            result = self._execute_query(query, tuple(params), fetch=True) or []
            logger.info("GET retornou %d registros", len(result))
            return result

        except Exception as e:
            logger.error("Falha no GET: %s", str(e), exc_info=True)
            raise ValueError(f"Erro ao buscar registros: {str(e)}")

    def get_one(self, table: str, conditions: Optional[Dict] = None) -> Optional[Dict]:
        """Busca um único registro com tratamento de erro aprimorado"""
        logger.info("Iniciando GET_ONE na tabela '%s'", table)

        try:
            # Usa LIMIT 1 para otimizar a busca
            base_query = f"SELECT * FROM {table}"
            params = []

            if conditions:
                where_clauses = []
                for key, value in conditions.items():
                    if value is None:
                        where_clauses.append(f"{key} IS NULL")
                    else:
                        where_clauses.append(f"{key} = ?")
                        params.append(value)

                if where_clauses:
                    base_query += " WHERE " + " AND ".join(where_clauses)

            query = base_query + " LIMIT 1"
            logger.debug("Query GET_ONE: %s", query)

            results = self._execute_query(query, tuple(params), fetch=True) or []
            return results[0] if results else None

        except Exception as e:
            logger.error("Falha no GET_ONE: %s", str(e), exc_info=True)
            raise ValueError(f"Erro ao buscar registro único: {str(e)}")

    def update(self, table: str, data: Dict, conditions: Dict) -> bool:
        """Atualiza registros com verificação de consistência"""
        logger.info("Iniciando UPDATE na tabela '%s'", table)
        logger.debug("Dados: %s", data)
        logger.debug("Condições: %s", conditions)

        try:
            self.begin_transaction()

            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            params = tuple(data.values()) + tuple(conditions.values())

            self._execute_query(query, params)

            # Verificação de que pelo menos um registro foi atualizado
            verify_query = f"SELECT changes() AS count"
            changes = self._execute_query(verify_query, fetch=True)

            if not changes or changes[0]['count'] == 0:
                logger.warning("Nenhum registro atualizado")

            self.commit_transaction()
            logger.info("UPDATE concluído com sucesso")
            return True

        except Exception as e:
            self.rollback_transaction()
            logger.error("Falha no UPDATE: %s", str(e), exc_info=True)
            raise

    def delete(self, table: str, conditions: Dict) -> bool:
        """Remove registros com verificação"""
        logger.info("Iniciando DELETE na tabela '%s'", table)
        logger.debug("Condições: %s", conditions)

        try:
            self.begin_transaction()

            where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
            query = f"DELETE FROM {table} WHERE {where_clause}"

            self._execute_query(query, tuple(conditions.values()))

            # Verificação de que pelo menos um registro foi removido
            verify_query = f"SELECT changes() AS count"
            changes = self._execute_query(verify_query, fetch=True)

            if not changes or changes[0]['count'] == 0:
                logger.warning("Nenhum registro removido")

            self.commit_transaction()
            logger.info("DELETE concluído com sucesso")
            return True

        except Exception as e:
            self.rollback_transaction()
            logger.error("Falha no DELETE: %s", str(e), exc_info=True)
            raise