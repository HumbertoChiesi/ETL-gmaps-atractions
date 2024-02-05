from sqlalchemy.types import VARCHAR, INT, TEXT, FLOAT
# ----------------------------------------------------------------------------------------
# CAMINHOS DOS CSV QUE SERAO LIDOS, TRATADOS E SALVOS
# ----------------------------------------------------------------------------------------
caminho_csv_em_tratamento = './arquivos_agrupados_em_tratamento/atraçoes.csv'
caminho_csv_atracoes_tratado = './arquivos_finais/atraçoes_tratadas.csv'
caminho_csv_tabela_horarios = './arquivos_finais/horarios_atracoes.csv'

# ----------------------------------------------------------------------------------------
# NOMES MODELO BERT E SPACY PT
# ----------------------------------------------------------------------------------------
modelo_bert = 'neuralmind/bert-base-portuguese-cased'
spacy_pt = 'pt_core_news_sm'

# ----------------------------------------------------------------------------------------
# NOMES DAS COLUNAS TRATADAS E CRIADAS NO FLUXO DO CHAIN OF RESPONSABILITY
# ----------------------------------------------------------------------------------------
coluna_palavras_chave = 'palavras_chave'
coluna_embedding = 'embeddings'
coluna_url = 'url'
coluna_latitude = 'latitude'
coluna_longitude = 'longitude'
coluna_comentario = 'comentarios'
coluna_avaliacao = 'avaliacao'
coluna_qtd_avaliacao = 'qtd_avaliacao'

coluna_id_atracao = 'atracao_id'
coluna_id_dia_semana = 'dia_semana_id'
coluna_horario = 'horario'
coluna_aberto = 'aberto'

# ----------------------------------------------------------------------------------------
# VARIAVEIS NECESSARIAS PARA INSERCAO NO BANCO DE DADOS
# ----------------------------------------------------------------------------------------
nome_tabela_atracoes = 'atracoes'
nome_tabela_atracoes_horarios = 'horario'

bd_nome_usuario = 'root'
senha_usuario = 'xxxx'
bd_host = '127.0.0.1:3308'
nome_db = 'travel_assistant_db'

schemas = {
    nome_tabela_atracoes: {
        coluna_id_atracao: INT,
        'nome': VARCHAR(100),
        'preco': VARCHAR(50),
        'elemento_mapa': VARCHAR(500),
        'horarios': VARCHAR(200),
        'descricao': VARCHAR(500),
        'imagem_url': VARCHAR(300),
        'endereco': VARCHAR(100),
        coluna_avaliacao: FLOAT,
        coluna_qtd_avaliacao: INT,
        coluna_comentario: TEXT,
        'telefone': VARCHAR(20),
        'lugar_tipo': VARCHAR(45),
        coluna_url: VARCHAR(200),
        coluna_latitude: FLOAT,
        coluna_longitude: FLOAT,
        coluna_palavras_chave: VARCHAR(5000),
        coluna_embedding: TEXT
    }, nome_tabela_atracoes_horarios: {
        coluna_id_atracao: INT,
        coluna_id_dia_semana: INT,
        coluna_aberto: INT,
        coluna_horario: VARCHAR(45)
    }}
