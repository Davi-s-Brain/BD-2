from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess


def verificar_disponibilidade_combo_mensagem(db: DatabaseAccess,
                                             p_id_lanche: int = None,
                                             p_id_bebida: int = None,
                                             p_id_sobremesa: int = None,
                                             p_id_acompanhamento: int = None):
    """
    Adaptação da função PostgreSQL para SQLite que verifica disponibilidade de combo

    Retorna uma lista de dicionários com:
    - item: nome do item
    - quantidade_estoque: quantidade disponível
    - mensagem: status de disponibilidade
    """

    # Parte 1: Coletar todos os itens do combo
    itens_combo = []

    # 1.1 Ingredientes do lanche
    if p_id_lanche is not None:
        query_lanche = """
        SELECT
            lci.Indice_prod,
            i.Nome_ingred,
            i.Indice_estoq
        FROM L_Contem_I lci
        JOIN Ingrediente i ON i.Id_ingred = lci.Id_ingred
        WHERE lci.Indice_prod = ?
        """
        ingredientes = db.execute_raw_query(query_lanche, (p_id_lanche,))
        itens_combo.extend([{'Indice_prod': item['Indice_prod'],
                             'Nome_ingred': item['Nome_ingred']}
                            for item in ingredientes])

    # 1.2 Bebida
    if p_id_bebida is not None:
        query_bebida = """
        SELECT 
            Indice_prod,
            Nome_prod AS Nome_ingred
        FROM Produto
        WHERE Indice_prod = ?
        """
        bebida = db.execute_raw_query(query_bebida, (p_id_bebida,))
        if bebida:
            itens_combo.append({'Indice_prod': bebida[0]['Indice_prod'],
                                'Nome_ingred': bebida[0]['Nome_ingred']})

    # 1.3 Sobremesa
    if p_id_sobremesa is not None:
        query_sobremesa = """
        SELECT 
            Indice_prod,
            Nome_prod AS Nome_ingred
        FROM Produto
        WHERE Indice_prod = ?
        """
        sobremesa = db.execute_raw_query(query_sobremesa, (p_id_sobremesa,))
        if sobremesa:
            itens_combo.append({'Indice_prod': sobremesa[0]['Indice_prod'],
                                'Nome_ingred': sobremesa[0]['Nome_ingred']})

    # 1.4 Acompanhamento
    if p_id_acompanhamento is not None:
        query_acompanhamento = """
        SELECT 
            Indice_prod,
            Nome_prod AS Nome_ingred
        FROM Produto
        WHERE Indice_prod = ?
        """
        acompanhamento = db.execute_raw_query(query_acompanhamento, (p_id_acompanhamento,))
        if acompanhamento:
            itens_combo.append({'Indice_prod': acompanhamento[0]['Indice_prod'],
                                'Nome_ingred': acompanhamento[0]['Nome_ingred']})

    # Parte 2: Verificar disponibilidade no estoque
    resultados = []
    itens_faltando = []

    for item in itens_combo:
        query_estoque = """
        SELECT Quantidade 
        FROM Estoque
        WHERE Nome_produto = ?
        """
        estoque = db.execute_raw_query(query_estoque, (item['Nome_ingred'],))

        quantidade = float(estoque[0]['Quantidade']) if estoque and estoque[0]['Quantidade'] is not None else 0.0

        resultados.append({
            'item': item['Nome_ingred'],
            'quantidade_estoque': quantidade
        })

        if quantidade <= 0:
            itens_faltando.append(item['Nome_ingred'])

    # Parte 3: Gerar mensagem de status
    if itens_faltando:
        mensagem = 'Faltam: ' + ', '.join(itens_faltando)
    else:
        mensagem = 'Combo disponível'

    # Adicionar mensagem a todos os resultados
    for resultado in resultados:
        resultado['mensagem'] = mensagem

    return resultados