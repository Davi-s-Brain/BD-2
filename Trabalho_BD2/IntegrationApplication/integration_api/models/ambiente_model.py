from typing import List, Dict, Optional
from datetime import datetime

from numpy.f2py.auxfuncs import throw_error

from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess


class AmbienteModel:
    def __init__(self, db_access: DatabaseAccess):
        self.db = db_access
    def get_all(self) -> List[Dict]:
        """
        Retorna todos os ambientes cadastrados no sistema.

        Returns:
            List[Dict]: Lista de dicionários com dados de todos os ambientes.
        """
        ambientes = self.db.get("Ambiente")
        return ambientes
    def criar_ambiente(self, ambiente_data: Dict) -> int:
        """
        Creates a new ambiente in the database.

        Args:
            ambiente_data: Dictionary with ambiente data following AmbienteBase schema

        Returns:
            int: The ID of the created ambiente
        """
        ambiente_data['Id_Amb'] = self._gerar_id_ambiente()

        self.db.add("Ambiente", ambiente_data)
        return self._gerar_id_ambiente()
    def _gerar_id_ambiente(self) -> int:
        resultado = self.db._execute_query("SELECT MAX(Id_Amb) AS max_id FROM Ambiente", fetch=True)
        max_id_str = resultado[0]['max_id'] if resultado and resultado[0]['max_id'] is not None else 0
        return int(max_id_str) + 1
    def buscar_por_id(self, id_ambiente: int) -> Optional[tuple]:
        """
        Retrieves an ambiente by its ID.

        Args:
            id_ambiente: The ID of the ambiente to retrieve

        Returns:
            Optional[tuple]: A tuple with all ambiente data, or None if not found
        """
        ambiente = self.db.get_one("Ambiente", {"Id_Amb": id_ambiente})

        if not ambiente:

            return None

        # Return a tuple with all the data in a consistent order
        return (
            ambiente['Id_Amb'],
            ambiente['Id_franquia'],
            ambiente['Tamanho_ambiente'],
            ambiente['Quantidade_desse_ambiente'],
            ambiente['Nivel_limpeza'],
            ambiente['Detetizado'],
            ambiente['Salao'],
            ambiente['Cozinha']
        )

    def buscar_por_franquia(self, id_franquia: int) -> List[tuple]:
        """
        Retrieves all ambientes for a specific franquia.

        Args:
            id_franquia: The ID of the franquia

        Returns:
            List[tuple]: List of tuples with ambiente data
        """
        ambientes = self.db.get("Ambiente", {"Id_franquia": str(id_franquia)})

        result = []
        for ambiente in ambientes:
            result.append((
                ambiente['Id_Amb'],
                ambiente['Id_franquia'],
                ambiente['Tamanho_ambiente'],
                ambiente['Quantidade_desse_ambiente'],
                ambiente['Nivel_limpeza'],
                ambiente['Detetizado'],
                ambiente['Salao'],
                ambiente['Cozinha']
            ))

        return result

    def atualizar_ambiente(self, id_ambiente: int, update_data: Dict) -> bool:
        """
        Updates an existing ambiente.

        Args:
            id_ambiente: The ID of the ambiente to update
            update_data: Dictionary with fields to update

        Returns:
            bool: True if successful, False otherwise
        """

        updated = self.db.update(
            "Ambiente",
            update_data,
            {"Id_Amb": id_ambiente}
        )

        return updated

    def remover_ambiente(self, id_ambiente: int) -> bool:
        """
        Removes an ambiente from the database.

        Args:
            id_ambiente: The ID of the ambiente to remove

        Returns:
            bool: True if successful, False otherwise
        """
        deleted = self.db.delete("Ambiente", {"Id_Amb": id_ambiente})
        return deleted