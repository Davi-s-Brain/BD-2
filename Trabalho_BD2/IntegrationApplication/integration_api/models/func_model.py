from __future__ import annotations

from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection


class Funcionario:
    def __init__(
        self,
        Id_func: int,
        Nome_func: str,
        CPF: str,
        Data_nasc_func: str,
        Cargo: str,
        Salario: float,
        Data_admissao: str,
        Turno: str,
        Tipo_de_contrato: str,
        Status_func: str,
        Id_franquia: int | None
    ):
        self.Id_func = Id_func
        self.Nome_func = Nome_func
        self.CPF = CPF
        self.Data_nasc_func = Data_nasc_func
        self.Cargo = Cargo
        self.Salario = Salario
        self.Data_admissao = Data_admissao
        self.Turno = Turno
        self.Tipo_de_contrato = Tipo_de_contrato
        self.Status_func = Status_func
        self.Id_franquia = Id_franquia

    @staticmethod
    def create(
        Nome_func: str,
        CPF: str,
        Data_nasc_func: str,
        Cargo: str,
        Salario: float,
        Data_admissao: str,
        Turno: str,
        Tipo_de_contrato: str,
        Status_func: str,
        Id_franquia: int | None = None
    ) -> int:
        """Insere um novo funcionário e retorna o id gerado."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO funcionario (
                    Nome_func, CPF, Data_nasc_func, Cargo, Salario,
                    Data_admissao, Turno, Tipo_de_contrato, Status_func, Id_franquia
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                Nome_func, CPF, Data_nasc_func, Cargo, Salario,
                Data_admissao, Turno, Tipo_de_contrato, Status_func, Id_franquia
            ))
            return cursor.lastrowid

    @staticmethod
    def get_all() -> list["Funcionario"]:
        """Retorna todos os funcionários."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM funcionario")
            rows = cursor.fetchall()
            return [Funcionario(*row) for row in rows]

    @staticmethod
    def get_by_id(Id_func: int) -> Funcionario | None:
        """Busca um funcionário pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM funcionario WHERE Id_func = ?", (Id_func,))
            row = cursor.fetchone()
            return Funcionario(*row) if row else None

    def update(self) -> None:
        """Atualiza os dados deste funcionário."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE funcionario SET
                    Nome_func = ?, CPF = ?, Data_nasc_func = ?, Cargo = ?,
                    Salario = ?, Data_admissao = ?, Turno = ?, Tipo_de_contrato = ?,
                    Status_func = ?, Id_franquia = ?
                WHERE Id_func = ?
            """, (
                self.Nome_func, self.CPF, self.Data_nasc_func, self.Cargo,
                self.Salario, self.Data_admissao, self.Turno,
                self.Tipo_de_contrato, self.Status_func, self.Id_franquia,
                self.Id_func
            ))
            conn.commit()

    def delete(self) -> None:
        """Remove este funcionário."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM funcionario WHERE Id_func = ?", (self.Id_func,))
            conn.commit()