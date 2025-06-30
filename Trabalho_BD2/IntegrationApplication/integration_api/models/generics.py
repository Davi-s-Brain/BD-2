from typing import List, Dict

from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess


def verificar_disponibilidade_combo_mensagem(db: DatabaseAccess,
                                             p_id_lanche: int = None,
                                             p_id_bebida: int = None,
                                             p_id_sobremesa: int = None,
                                             p_id_acompanhamento: int = None) -> List[Dict]:
    """
    Verifica a disponibilidade de um combo de produtos no SQLite

    Args:
        db: Instância de DatabaseAccess
        p_id_lanche: ID do lanche
        p_id_bebida: ID da bebida
        p_id_sobremesa: ID da sobremesa
        p_id_acompanhamento: ID do acompanhamento

    Returns:
        Lista de dicionários com os itens, quantidades em estoque e mensagem de status
    """

    # Consulta para ingredientes do lanche
    query_ingredientes_lanche = """
    SELECT 
        lci.Indice_prod,
        i.Nome_ingred,
        i.Indice_estoq
    FROM L_Contem_I lci
    JOIN Ingrediente i ON i.Id_ingred = lci.Id_ingred
    WHERE lci.Indice_prod = ?
    """ if p_id_lanche else None

    # Consultas para os outros itens (bebida, sobremesa, acompanhamento)
    query_itens_simples = """
    SELECT 
        p.Indice_prod,
        p.Nome_prod AS Nome_ingred
    FROM Produto p
    WHERE p.Indice_prod = ?
    """

    # Coletar todos os itens do combo
    itens_combo = []

    # 1. Ingredientes do lanche
    if p_id_lanche and query_ingredientes_lanche:
        ingredientes = db.execute_raw_query(query_ingredientes_lanche, (p_id_lanche,))
        itens_combo.extend(ingredientes)

    # 2. Bebida
    if p_id_bebida:
        bebida = db.execute_raw_query(query_itens_simples, (p_id_bebida,))
        itens_combo.extend(bebida)

    # 3. Sobremesa
    if p_id_sobremesa:
        sobremesa = db.execute_raw_query(query_itens_simples, (p_id_sobremesa,))
        itens_combo.extend(sobremesa)

    # 4. Acompanhamento
    if p_id_acompanhamento:
        acompanhamento = db.execute_raw_query(query_itens_simples, (p_id_acompanhamento,))
        itens_combo.extend(acompanhamento)

    # Verificar disponibilidade no estoque
    resultados = []
    itens_faltando = []

    for item in itens_combo:
        # Consulta o estoque para cada item
        query_estoque = """
        SELECT 
            Quantidade AS quantidade_estoque
        FROM Estoque
        WHERE Nome_produto = ?
        """
        estoque = db.execute_raw_query(query_estoque, (item['Nome_ingred'],))

        qtd_estoque = estoque[0]['quantidade_estoque'] if estoque else 0

        # Adiciona ao resultado
        resultados.append({
            'item': item['Nome_ingred'],
            'quantidade_estoque': qtd_estoque
        })

        # Verifica se está faltando
        if qtd_estoque <= 0:
            itens_faltando.append(item['Nome_ingred'])

    # Cria mensagem de status
    mensagem = 'Faltam: ' + ', '.join(itens_faltando) if itens_faltando else 'Combo disponível'

    # Adiciona a mensagem a todos os resultados
    for resultado in resultados:
        resultado['mensagem'] = mensagem

    return resultados

def buscar_produtos_mais_vendidos_periodo(db: DatabaseAccess, data_inicio: str, data_fim: str) -> List[Dict]:
    """
    Retorna os produtos mais vendidos em um período específico, com nome, tipo e quantidade vendida.

    Args:
        db: Instância de DatabaseAccess
        data_inicio: Data de início no formato 'YYYY-MM-DD'
        data_fim: Data de fim no formato 'YYYY-MM-DD'

    Returns:
        Lista de dicionários com id_produto, nome_produto, tipo_produto e quantidade_vendida
    """
    query = """
        SELECT 
            pr.Indice_prod AS id_produto,
            pr.Nome_prod AS nome_produto,
        CASE 
            WHEN pr.Lanche IS TRUE THEN 'Lanche'
            WHEN pr.Bebida IS TRUE THEN 'Bebida'
            WHEN pr.Sobremesa IS TRUE THEN 'Sobremesa'
            WHEN pr.Acompanhamento IS TRUE THEN 'Acompanhamento'
            ELSE 'Outro'
        END AS tipo_produto,
            COUNT(*) AS quantidade_vendida
        FROM Ped_Escolhe_Prod pe
        JOIN Pedido p ON pe.Id_pedido = p.Id_pedido  
        JOIN Produto pr ON pr.Indice_prod = pe.Indice_prod
        WHERE DATE(p.Data_pedido) BETWEEN DATE(?) AND DATE(?)
        GROUP BY pr.Indice_prod, pr.Nome_prod, pr.Lanche, pr.Bebida, pr.Sobremesa, pr.Acompanhamento
        ORDER BY quantidade_vendida DESC
    """

    resultados = db.execute_raw_query(query, (data_inicio, data_fim))
    return resultados