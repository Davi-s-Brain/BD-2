from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess, logger


def resumo_balanco_geral(db: DatabaseAccess, data_inicio: str = None, data_fim: str = None) -> dict:
    """
    Retorna um resumo do balanço geral com total de pedidos, total de vendas e ticket médio.
    """
    try:
        query = """
        SELECT 
            COUNT(*) AS total_pedidos,
            COALESCE(SUM(Valor_total_pedido), 0) AS total_vendas,
            CASE 
                WHEN COUNT(*) = 0 THEN 0
                ELSE ROUND((COALESCE(SUM(Valor_total_pedido), 0) / COUNT(*)), 2)
            END AS ticket_medio
        FROM Pedido
        """

        params = {}

        if data_inicio or data_fim:
            where_clauses = []

            if data_inicio:
                where_clauses.append("Data_pedido >= :data_inicio")
                params['data_inicio'] = data_inicio

            if data_fim:
                where_clauses.append("Data_pedido <= :data_fim")
                params['data_fim'] = data_fim

            query += " WHERE " + " AND ".join(where_clauses)

        logger.info(f"Executando consulta de resumo do balanço geral: {query} com params={params}")

        result = db._execute_query(query, params=params, fetch=True)

        if not result:
            return {
                'total_pedidos': 0,
                'total_vendas': 0,
                'ticket_medio': 0
            }

        return dict(result[0])

    except Exception as e:
        logger.error(f"Erro ao calcular resumo do balanço geral: {str(e)}")
        raise ValueError(f"Falha na consulta do balanço geral: {str(e)}")
